import os

from aws_cdk import (
    Duration,
)
from aws_cdk import (
    aws_lambda as _lambda,
)
from constructs import Construct

RUNTIME_SOURCE_DIR = os.path.join(
    os.path.dirname(__file__),
    "runtime",
)


class EdaProcessor(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        dynamodb_table_name: str,
        processed_bucket_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        self.lambda_handler = _lambda.DockerImageFunction(
            scope=self,
            id="PerformEda",
            function_name="perform_eda",
            code=_lambda.DockerImageCode.from_image_asset(
                directory=RUNTIME_SOURCE_DIR,
            ),
            environment={
                "PROFILE_POOL_SIZE": "1",
                "DYNAMODB_TABLE": dynamodb_table_name,
                "PROCESSED_BUCKET": processed_bucket_name,
                "POWERTOOLS_SERVICE_NAME": "eda-processor",
                "POWERTOOLS_LOGGER_LOG_EVENT": "true",
                "LOG_LEVEL": "info",
                "MPLCONFIGDIR": "/tmp/.config/matplotlib",
            },
            timeout=Duration.seconds(300),
            memory_size=2048,
        )
