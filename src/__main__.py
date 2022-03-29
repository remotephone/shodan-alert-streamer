import os

from shodan import Shodan

from shodan_logger import logger
from sns import send_sns

# Setup the Shodan API connection
def get_api():
    try:
        logger.info("Connecting to Shodan API....")
        api = Shodan(os.environ["SHODAN_API_KEY"])
        logger.info("Connected to shodan! Streaming alerts!.")
        return api
    except:
        logger.error("Failed to retrieve Shodan API Key")
        raise SystemExit

def send_alert(message):
    try:
        send_sns(message)
        logger.info(f"SNS Notification sent succesfully")
    except Exception as e:
        logger.error(f"Failed to post SNS - {e}")

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
    logger.info(f"Streaming alerts - \n")
    for alert in api.alerts():
        logger.info(f"  - {alert['id']} monitoring {alert.get('filters', 'None').get('ip', 'None')}")

def main(api):
    try:
        logger.info("Connected to Shodan API! Waiting for alerts...")
        get_alerts(api)
        for alert in api.stream.alert():
            logger.info(f"Got an alert! - {alert}")
            message = get_fields(alert)
            logger.info(f"Sending SNS message - {message}")
            send_alert(message)
    except Exception as e:
        logger.erorr(e)
    

if __name__ == "__main__":
    api = get_api()
    main(api)