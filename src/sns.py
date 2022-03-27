import json
import os
import logger

import boto3

from logger import logger

try:
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
except:
    logger.error("Failed to get AWS Credentials")


def send_sns(message):
    client = boto3.client(
        "sns",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    try:
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps({"default": json.dumps(message)}),
            MessageStructure="json",
        )
    except Exception as e:
        response = e
    return response
