from models.io.upbound.m.gcp.storage.bucket import v1beta1 as bucketv1beta1
from models.io.upbound.m.gcp.storage.bucketacl import v1beta1 as aclv1beta1
from models.com.example.platform.storagebucket import v1alpha1
from models.io.k8s.apimachinery.pkg.apis.meta import v1 as metav1

expected_xr = v1alpha1.StorageBucket(
    apiVersion="platform.example.com/v1alpha1",
    kind="StorageBucket",
    metadata=metav1.ObjectMeta(
        name="example",
        namespace="default",
    ),
    spec = v1alpha1.Spec(
        parameters = v1alpha1.Parameters(
            acl="publicRead",
            location="US",
            versioning=True,
        ),
    ),
)

expected_bucket_before = bucketv1beta1.Bucket(
    apiVersion="storage.gcp.m.upbound.io/v1beta1",
    kind="Bucket",
    metadata=metav1.ObjectMeta(
        annotations={
            "crossplane.io/composition-resource-name": "bucket",
        },
    ),
    spec=bucketv1beta1.Spec(
        forProvider=bucketv1beta1.ForProvider(
            location="US",
            versioning=bucketv1beta1.Versioning(
                enabled=True,
                ),
        ),
    ),
)

observed_bucket = bucketv1beta1.Bucket(
    apiVersion="storage.gcp.m.upbound.io/v1beta1",
    kind="Bucket",
    metadata=metav1.ObjectMeta(
        name="example-bucket",
        namespace="default",
        annotations={
            "crossplane.io/composition-resource-name": "bucket",
            "crossplane.io/external-name": "example-bucket",
        },
    ),
    spec=bucketv1beta1.Spec(
        forProvider=bucketv1beta1.ForProvider(
            location="US",
            versioning=bucketv1beta1.Versioning(
                enabled=True,
                ),
        )
    )
)

expected_bucket_after = bucketv1beta1.Bucket(
    apiVersion="storage.gcp.m.upbound.io/v1beta1",
    kind="Bucket",
    metadata=metav1.ObjectMeta(
        name="example-bucket",
        namespace="default",
        annotations={
            "crossplane.io/composition-resource-name": "bucket",
        },
    ),
    spec=bucketv1beta1.Spec(
        forProvider=bucketv1beta1.ForProvider(
            location="US",
            versioning=bucketv1beta1.Versioning(
                enabled=True,
                ),
        ),
    ),
)

expected_acl = aclv1beta1.BucketACL(
    apiVersion="storage.gcp.m.upbound.io/v1beta1",
    kind="BucketACL",
    metadata=metav1.ObjectMeta(
        annotations={
            "crossplane.io/composition-resource-name": "acl",
        },
    ),
    spec=aclv1beta1.Spec(
        forProvider=aclv1beta1.ForProvider(
            predefinedAcl="publicRead",
            bucket="example-bucket",
        ),
    ),
)
