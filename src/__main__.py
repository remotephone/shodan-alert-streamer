import os

from shodan import Shodan

from logger import logger
from sns import send_sns

# Setup the Shodan API connection
try:
    logger.error("Connecting to Shodan API....")
    api = Shodan(os.environ["SHODAN_API_KEY"])
    logger.error("Connected to shodan! Streaming alerts!.")
except:
    logger.error("Failed to retrieve Shodan API Key")
    raise SystemExit

# Subscribe to results for all networks:
for alert in api.stream.alert():
    logger.info("Got an alert!")
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
    logger.info(f"Sending SNS message - {message}")
    try:
        send_sns(message)
        logger.info(f"SNS Notification sent succesfully")
    except Exception as e:
        logger.error(f"Failed to post SNS - {e}")
