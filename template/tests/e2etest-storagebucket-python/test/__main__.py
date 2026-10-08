import os

import yaml
from models.io.upbound.dev.meta.e2etest import v1alpha1 as e2etest
from models.io.k8s.apimachinery.pkg.apis.meta import v1 as k8s
from models.com.example.platform.storagebucket import v1alpha1 as storagebucket
from models.io.upbound.m.gcp.clusterproviderconfig import v1beta1 as clusterproviderconfig

# The provider authenticates to GCP through Upbound identity federation, so the
# test needs no stored GCP credentials. This only works on an Upbound Cloud
# control plane, whose identity the GCP workload identity pool must trust.
# Override the defaults with these environment variables to use your own GCP
# project, workload identity pool provider, and service account.
gcp_project_id = os.environ.get("UP_GCP_PROJECT_ID") or "crossplane-playground"
gcp_wif_provider = os.environ.get("UP_GCP_WIF_PROVIDER") or (
    "projects/283222062215/locations/global/workloadIdentityPools/"
    "solutions-upbound-oidc-pool/providers/solutions-u5d-oidc-pool"
)
gcp_service_account = os.environ.get("UP_GCP_SERVICE_ACCOUNT") or (
    "solutions-u5d-service-account@crossplane-playground.iam.gserviceaccount.com"
)

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

# Namespaced managed resources use the ClusterProviderConfig named "default"
# unless they set a providerConfigRef.
provider_config = clusterproviderconfig.ClusterProviderConfig(
    metadata=k8s.ObjectMeta(
        name="default",
    ),
    spec=clusterproviderconfig.Spec(
        projectID=gcp_project_id,
        credentials=clusterproviderconfig.Credentials(
            source="Upbound",
            upbound=clusterproviderconfig.Upbound(
                federation=clusterproviderconfig.Federation(
                    providerID=gcp_wif_provider,
                    serviceAccount=gcp_service_account,
                ),
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
            provider_config.model_dump(by_alias=True, exclude_none=True),
        ],
        skipDelete=False,
        timeoutSeconds=300,
    )
)

# The test runner expects an "items" array, one entry per test.
output = {"items": [test.model_dump(by_alias=True, exclude_none=True)]}
print(yaml.dump(output))
