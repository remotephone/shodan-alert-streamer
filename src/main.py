import os



from shodan_logger import logger
from helpers import get_api, get_alerts, get_fields, send_alert


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
