import base64
import os

import yaml
from pydantic import BaseModel
from models.io.upbound.dev.meta.e2etest import v1alpha1 as e2etest
from models.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from models.com.example.platform.xstoragebucket import v1alpha1 as xstoragebucket
from models.io.upbound.gcp.providerconfig import v1beta1 as providerconfig


class Secret(BaseModel):
    apiVersion: str = "v1"
    kind: str = "Secret"
    metadata: k8s.ObjectMeta
    type: str = "Opaque"
    data: dict[str, str] = {}

bucket_manifest = xstoragebucket.XStorageBucket(
    metadata=k8s.ObjectMeta(
        name="uptest-bucket-xr-python",
    ),
    spec=xstoragebucket.Spec(
        parameters=xstoragebucket.Parameters(
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

provider_config = providerconfig.ProviderConfig(
    metadata=k8s.ObjectMeta(
        name="default",
    ),
    spec=providerconfig.Spec(
        projectID=os.environ.get("UP_GCP_PROJECT_ID", ""),
        credentials=providerconfig.Credentials(
            source="Secret",
            secretRef=providerconfig.SecretRef(
                name="gcp-credentials",
                namespace="crossplane-system",
                key="credentials",
            ),
        ),
    ),
)

test = e2etest.E2ETest(
    metadata=k8s.ObjectMeta(
        name="e2etest-xstoragebucket",
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
