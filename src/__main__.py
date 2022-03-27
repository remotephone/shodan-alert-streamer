import logging
import os

from shodan import Shodan

from sns import send_sns

# Setup the Shodan API connection
try:
    api = Shodan(os.getenv("SHODAN_API_KEY"))
except:
    logging.error("Failed to retrieve Shodan API Key")

# Subscribe to results for all networks:
for alert in api.stream.alert():
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
    logging.info(f"Sending SNS message - {message}")
    try:
        send_sns(message)
    except Exception as e:
        logging.error(f"Failed to post SNS - {e}")
