import models.io.upbound.gcpm.storage.v1beta1
import models.com.example.platform.v1alpha1.storagebucket as storagebucketv1alpha1

oxr = option("params").oxr
# Validate only the parameters against the generated schema. Crossplane adds
# fields under spec.crossplane (such as namespaced resourceRefs) that the
# generated StorageBucket schema doesn't model, so don't type the whole XR.
params = storagebucketv1alpha1.PlatformExampleComV1alpha1StorageBucketSpecParameters{**oxr.spec.parameters}

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
                location = params.location
                versioning = {
                    enabled = params.versioning
                }
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
                    predefinedAcl = params.acl
                }
            }
        }
    ]

items = _items
