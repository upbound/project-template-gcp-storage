import models.io.upbound.gcp.storage.v1beta1
import models.com.example.platform.v1alpha1.xstoragebucket as xstoragebucketv1alpha1

oxr = xstoragebucketv1alpha1.XStorageBucket{**option("params").oxr}

_metadata = lambda name: str -> any {
  {
    annotations = {
      "krm.kcl.dev/composition-resource-name" = name
    }
  }
}

_items: [any] = [
    v1beta1.Bucket{
        metadata: _metadata("bucket")
        spec = {
            forProvider = {
                location = oxr.spec.parameters.location
                versioning = [
                    {
                        enabled = oxr.spec.parameters.versioning
                    }
                ]
            }
        }
    }
]

ocds = option("params").ocds
bucketExternalName = ocds["bucket"]?.Resource?.metadata?.annotations?["crossplane.io/external-name"]

if bucketExternalName:
    _items += [
        v1beta1.BucketACL{
            metadata: _metadata("acl")
                spec = {
                forProvider = {
                    bucket = bucketExternalName
                    predefinedAcl = oxr.spec.parameters.acl
                }
            }
        }
    ]

items = _items
