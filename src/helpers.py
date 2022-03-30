import json
import os

import boto3
from shodan import Shodan

from shodan_logger import logger


def get_api():
    try:
        logger.info("Connecting to Shodan API....")
        api = Shodan(os.environ["SHODAN_API_KEY"])
        logger.info("Connected to shodan! Streaming alerts!.")
        return api
    except:
        logger.error("Failed to retrieve Shodan API Key")
        raise SystemExit


def get_fields(alert):
    ip = alert.get("ip_str", "Not Found")
    port = alert.get("port", "Not Found")
    hostnames = alert.get("hostnames", "Not Found")
    alert_id = (
        alert.get("_shodan", "Not Found")
        .get("alert", "Not Found")
        .get("id", "Not Found")
    )
    message = f"""Shodan Detected a New Service:
    IP: {ip}
    Port: {port}
    Hostnames: {hostnames}
    Alert ID: {alert_id}
    """
    return message


def get_alerts(api):
    for alert in api.alerts():
        logger.info(
            f"Loaded Alert - {alert['id']} monitoring {alert.get('filters', 'None').get('ip', 'None')}"
        )


def send_alert(message):
    try:
        send_sns(message)
        logger.info(f"SNS Notification sent succesfully")
    except Exception as e:
        logger.error(f"Failed to post SNS - {e}")

def get_env_vars():
    try:
        ACCESS_KEY = os.environ["ACCESS_KEY"]
        SECRET_KEY = os.environ["SECRET_KEY"]
        SNS_TOPIC = os.environ["SNS_TOPIC"]
    except:
        logger.error("Failed to get AWS Credentials from environment")
    return ACCESS_KEY, SECRET_KEY, SNS_TOPIC

def send_sns(message):
    ACCESS_KEY, SECRET_KEY, SNS_TOPIC = get_env_vars()
    client = boto3.client(
        "sns",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=SNS_TOPIC.split(":")[3]
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
