import models.com.example.platform.v1alpha1 as platformv1alpha1
import models.io.upbound.gcp.storage.v1beta1 as v1beta1

_expectedXR =  platformv1alpha1.XStorageBucket{
    metadata.name: "example"
    spec: {
        parameters: {
            acl: "publicRead"
            location: "US"
            versioning: True
        }
    }
}

_expectedBucketBefore = v1beta1.Bucket{
    metadata.annotations: {
        "crossplane.io/composition-resource-name": "bucket"
    }
    spec.forProvider: {
        location: "US"
        versioning: [
            {
                enabled: True
            }
        ]
    }
}

_observedBucket = v1beta1.Bucket{
    metadata.name: "example-bucket"
    metadata.annotations: {
        "crossplane.io/composition-resource-name": "bucket"
        "crossplane.io/external-name": "example-bucket"
    }
    spec.forProvider: {
        location: "US"
        versioning: [
            {
                enabled: True
            }
        ]
    }
}

_expectedBucketAfter = v1beta1.Bucket{
    metadata.name: "example-bucket"
    metadata.annotations: {
        "crossplane.io/composition-resource-name": "bucket"
    }
    spec.forProvider: {
        location: "US"
        versioning: [
            {
                enabled: True
            }
        ]
    }
}

_expectedACL = v1beta1.BucketACL{
    metadata.annotations: {
        "crossplane.io/composition-resource-name": "acl"
    }
    spec.forProvider:{
        predefinedAcl: "publicRead"
        bucket: "example-bucket"
    }
}
