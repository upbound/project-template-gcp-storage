import base64
import file

import models.com.example.platform.v1alpha1 as platformv1alpha1
import models.io.upbound.gcp.v1beta1 as gcpv1beta1
import models.io.upbound.dev.meta.v1alpha1 as metav1alpha1
import models.io.k8s.api.core.v1 as corev1

gcp_project_id = file.read_env("UP_GCP_PROJECT_ID")
gcp_creds = file.read_env("UP_GCP_CREDS")


_items = [
    metav1alpha1.E2ETest{
        metadata.name = "e2etest-xstoragebucket"
        spec = {
            crossplane.autoUpgrade.channel = "Rapid"
            defaultConditions = [
                "Ready"
            ]
            manifests = [
                platformv1alpha1.XStorageBucket{
                    metadata.name = "uptest-bucket-xr-kcl"
                    spec.parameters = {
                        acl = "private"
                        location = "EU"
                        versioning: True
                    }
                }
            ]
            extraResources = [
                gcpv1beta1.ProviderConfig{
                    metadata.name = "default"
                    spec.projectID = gcp_project_id
                    spec.credentials = {
                        source = "Secret"
                        secretRef = {
                            name = "gcp-credentials"
                            namespace = "crossplane-system"
                            key = "credentials"
                        }
                    }
                },
                corev1.Secret{
                    metadata={
                        name="gcp-credentials",
                        namespace="crossplane-system",
                    },
                    data={
                        "credentials": base64.encode(gcp_creds)
                    }
                }
            ]
            skipDelete = False
            timeoutSeconds = 300 # 5 minutes
        }
    }
]
items = _items