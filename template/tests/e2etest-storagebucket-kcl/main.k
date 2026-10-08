import file

import models.com.example.platform.v1alpha1 as platformv1alpha1
import models.io.upbound.gcpm.v1beta1 as gcpmv1beta1
import models.io.upbound.dev.meta.v1alpha1 as metav1alpha1

# The provider authenticates to GCP through Upbound identity federation, so the
# test needs no stored GCP credentials. This only works on an Upbound Cloud
# control plane, whose identity the GCP workload identity pool must trust.
# Override the defaults with these environment variables to use your own GCP
# project, workload identity pool provider, and service account.
gcp_project_id = file.read_env("UP_GCP_PROJECT_ID") or "crossplane-playground"
gcp_wif_provider = file.read_env("UP_GCP_WIF_PROVIDER") or "projects/283222062215/locations/global/workloadIdentityPools/solutions-upbound-oidc-pool/providers/solutions-u5d-oidc-pool"
gcp_service_account = file.read_env("UP_GCP_SERVICE_ACCOUNT") or "solutions-u5d-service-account@crossplane-playground.iam.gserviceaccount.com"

_items = [
    metav1alpha1.E2ETest{
        metadata.name = "e2etest-storagebucket"
        spec = {
            crossplane.autoUpgrade.channel = "Rapid"
            defaultConditions = [
                "Ready"
            ]
            manifests = [
                platformv1alpha1.StorageBucket{
                    metadata.name = "uptest-bucket-xr-kcl"
                    metadata.namespace = "default"
                    spec.parameters = {
                        acl = "private"
                        location = "EU"
                        versioning: True
                    }
                }
            ]
            extraResources = [
                # Namespaced managed resources use the ClusterProviderConfig
                # named "default" unless they set a providerConfigRef.
                gcpmv1beta1.ClusterProviderConfig{
                    metadata.name = "default"
                    spec.projectID = gcp_project_id
                    spec.credentials = {
                        source = "Upbound"
                        upbound.federation = {
                            providerID = gcp_wif_provider
                            serviceAccount = gcp_service_account
                        }
                    }
                }
            ]
            skipDelete = False
            timeoutSeconds = 300 # 5 minutes
        }
    }
]
items = _items
