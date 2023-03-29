from aws_cdk import (
    RemovalPolicy,
)
from aws_cdk import (
    aws_s3 as s3,
)
from constructs import Construct


def create_bucket(scope: Construct, label: str):
    return s3.Bucket(
        scope=scope,
        id=f"EdaStorage{label.title()}",
        bucket_name=f"eda-storage-{label.lower()}",
        block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        removal_policy=RemovalPolicy.DESTROY,
        versioned=False,
    )
