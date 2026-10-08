import base64
import os

import yaml
from pydantic import BaseModel
from models.io.upbound.dev.meta.e2etest import v1alpha1 as e2etest
from models.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from models.com.example.platform.storagebucket import v1alpha1 as storagebucket
from models.io.upbound.m.gcp.clusterproviderconfig import v1beta1 as clusterproviderconfig


class Secret(BaseModel):
    apiVersion: str = "v1"
    kind: str = "Secret"
    metadata: k8s.ObjectMeta
    type: str = "Opaque"
    data: dict[str, str] = {}

bucket_manifest = storagebucket.StorageBucket(
    metadata=k8s.ObjectMeta(
        name="uptest-bucket-xr-python",
        namespace="default",
    ),
    spec=storagebucket.Spec(
        parameters=storagebucket.Parameters(
            acl="private",
            location="EU",
            versioning=True,
        ),
    ),
)

provider_creds = Secret(
    metadata=k8s.ObjectMeta(
        name="gcp-credentials",
        namespace="crossplane-system",
    ),
    data={
        "credentials": base64.b64encode(os.environ.get("UP_GCP_CREDS", "").encode()).decode('ascii')
    }
)

provider_config = clusterproviderconfig.ClusterProviderConfig(
    metadata=k8s.ObjectMeta(
        name="default",
    ),
    spec=clusterproviderconfig.Spec(
        projectID=os.environ.get("UP_GCP_PROJECT_ID", ""),
        credentials=clusterproviderconfig.Credentials(
            source="Secret",
            secretRef=clusterproviderconfig.SecretRef(
                name="gcp-credentials",
                namespace="crossplane-system",
                key="credentials",
            ),
        ),
    ),
)

test = e2etest.E2ETest(
    metadata=k8s.ObjectMeta(
        name="e2etest-storagebucket",
    ),
    spec=e2etest.Spec(
        crossplane=e2etest.Crossplane(
            autoUpgrade=e2etest.AutoUpgrade(
                channel="Rapid",
            ),
        ),
        defaultConditions=[
            "Ready",
        ],
        manifests=[bucket_manifest.model_dump(by_alias=True, exclude_none=True)],
        extraResources=[
            provider_creds.model_dump(by_alias=True, exclude_none=True),
            provider_config.model_dump(by_alias=True, exclude_none=True),
        ],
        skipDelete=False,
        timeoutSeconds=300,
    )
)

# The test runner expects an "items" array, one entry per test.
output = {"items": [test.model_dump(by_alias=True, exclude_none=True)]}
print(yaml.dump(output))
