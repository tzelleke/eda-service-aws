from aws_cdk import (
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk import (
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class Database(Construct):
    def __init__(self, scope: Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)
        self.table = self._build_table()

    def _build_table(self):
        table = dynamodb.Table(
            self,
            "EdaServiceTable",
            partition_key=dynamodb.Attribute(
                name="PK", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            stream=dynamodb.StreamViewType.KEYS_ONLY,
        )
        CfnOutput(self, "DynamoDbTableName", value=table.table_name)
        CfnOutput(self, "DynamoDbTableStream", value=table.table_stream_arn)

        return table
