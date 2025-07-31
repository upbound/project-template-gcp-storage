from crossplane.function import resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

from .model.io.upbound.gcp.storage.bucket import v1beta1 as bucketv1beta1
from .model.io.upbound.gcp.storage.bucketacl import v1beta1 as aclv1beta1
from .model.com.example.platform.xstoragebucket import v1alpha1


def compose(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse):
    observed_xr = v1alpha1.XStorageBucket(**req.observed.composite.resource)
    params = observed_xr.spec.parameters

    desired_bucket = bucketv1beta1.Bucket(
        spec=bucketv1beta1.Spec(
            forProvider=bucketv1beta1.ForProvider(
                location=params.location,
                versioning=[
                    bucketv1beta1.VersioningItem(
                        enabled=params.versioning,
                    )
                ],
            ),
        ),
    )
    resource.update(rsp.desired.resources["bucket"], desired_bucket)

    # Return early if Crossplane hasn't observed the bucket yet. This means it
    # hasn't been created yet. This function will be called again after it is.
    # We want the bucket to be created so we can refer to its external name.
    if "bucket" not in req.observed.resources:
        return

    observed_bucket = bucketv1beta1.Bucket(**req.observed.resources["bucket"].resource)

    # The desired ACL refers to the bucket by its external name, which is stored
    # in its external name annotation. Return early if the Bucket's
    # external-name annotation isn't set yet.
    if observed_bucket.metadata is None or observed_bucket.metadata.annotations is None:
        return
    if "crossplane.io/external-name" not in observed_bucket.metadata.annotations:
        return

    bucket_external_name = observed_bucket.metadata.annotations[
        "crossplane.io/external-name"
    ]

    desired_acl = aclv1beta1.BucketACL(
        spec=aclv1beta1.Spec(
            forProvider=aclv1beta1.ForProvider(
                bucket=bucket_external_name,
                predefinedAcl=params.acl,
            ),
        ),
    )
    resource.update(rsp.desired.resources["acl"], desired_acl)
