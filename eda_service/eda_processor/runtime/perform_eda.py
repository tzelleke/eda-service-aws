import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from botocore.exceptions import (
    ClientError,
    ParamValidationError,
)
import jmespath
import pandas as pd
import ydata_profiling

logger = Logger(log_uncaught_exceptions=True)

DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]
PROCESSED_BUCKET = os.environ["PROCESSED_BUCKET"]

VERSION = ydata_profiling.__version__

dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")

get_source_bucket = jmespath.compile("Records[0].s3.bucket.name")
get_key = jmespath.compile("Records[0].s3.object.key")
get_timestamp = jmespath.compile("Records[0].eventTime")


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> None:
    source_bucket = get_source_bucket.search(event)
    key = get_key.search(event)
    timestamp = get_timestamp.search(event)

    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    profile = ydata_profiling.ProfileReport(df, title="Pandas Profiling Report")
    profile_json = profile.to_json()

    try:
        s3.copy({"Bucket": source_bucket, "Key": key}, PROCESSED_BUCKET, key)
        logger.info("File copied to the destination bucket successfully!")

    except ClientError as e:
        logger.exception("Error copying the file to the destination bucket")
        raise RuntimeError("Unable to fulfill request") from e

    except ParamValidationError as e:
        logger.exception("Missing required parameters while calling the API.")
        raise RuntimeError("Unable to fulfill request") from e

    dynamodb.put_item(
        Item={
            "PK": {
                "S": key,
            },
            "version": {
                "S": VERSION,
            },
            "timestamp": {
                "S": timestamp,
            },
            "profile": {
                "S": profile_json,
            },
        },
        ReturnConsumedCapacity="TOTAL",
        TableName=DYNAMODB_TABLE,
    )
