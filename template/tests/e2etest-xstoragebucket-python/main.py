import base64
import os

from .model.io.upbound.dev.meta.e2etest import v1alpha1 as e2etest
from .model.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from .model.com.example.platform.xstoragebucket import v1alpha1 as xstoragebucket
from .model.io.upbound.gcp.providerconfig import v1beta1 as providerconfig
from .model.io.k8s.api.core import v1 as corev1
from .model.io.k8s.apimachinery.pkg.apis.core.meta import v1 as coremetav1

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

provider_creds = corev1.Secret(
    metadata=coremetav1.ObjectMeta(
        name="gcp-credentials",
        namespace="crossplane-system",
    ),
    data={
        "credentials": base64.b64encode(os.environ.get("UP_GCP_CREDS").encode()).decode('ascii')
    }
)

provider_config = providerconfig.ProviderConfig(
    metadata=k8s.ObjectMeta(
        name="default",
    ),
    spec=providerconfig.Spec(
        projectID=os.environ.get("UP_GCP_PROJECT_ID"),
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
        manifests=[bucket_manifest.model_dump()],
        extraResources=[provider_creds.model_dump(), provider_config.model_dump()],
        skipDelete=False,
        timeoutSeconds=300,
    )
)
