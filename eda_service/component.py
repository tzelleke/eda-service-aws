from aws_cdk import (
    Stack,
)
from aws_cdk import (
    aws_s3_notifications as s3_notification,
)
from cdk_dynamo_table_view import TableViewer
from constructs import Construct

from eda_service.database.infrastructure import Database
from eda_service.eda_processor.infrastructure import EdaProcessor
from eda_service.util import create_bucket


class EdaServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ingestion_bucket = create_bucket(self, "ingestion")
        self.processed_bucket = create_bucket(self, "processed")
        self.database = Database(self, "Database")
        self.processor = EdaProcessor(
            self,
            "EdaProcessor",
            self.database.table.table_name,
            self.processed_bucket.bucket_name,
        )
        self.table_viewer = TableViewer(
            self,
            "TableViewer",
            title="EDA Service",
            table=self.database.table,
            sort_by="-PK",
        )

        self.ingestion_bucket.grant_read_write(self.processor.lambda_handler)
        self.ingestion_bucket.add_object_created_notification(
            s3_notification.LambdaDestination(self.processor.lambda_handler)
        )
        self.database.table.grant_read_write_data(self.processor.lambda_handler)
        self.processed_bucket.grant_read_write(self.processor.lambda_handler)
