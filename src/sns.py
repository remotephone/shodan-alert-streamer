import json
import os

import boto3

from shodan_logger import logger

try:
    ACCESS_KEY = os.environ["ACCESS_KEY"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    SNS_TOPIC = os.environ["SNS_TOPIC"]
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
            TargetArn=SNS_TOPIC,
            Message=json.dumps({"default": json.dumps(message)}),
            MessageStructure="json",
        )
    except Exception as e:
        response = e
    return response
