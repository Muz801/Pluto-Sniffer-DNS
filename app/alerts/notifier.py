import json
import requests

from datetime import datetime
from colorama import Fore, Style, init

from config import SLACK_WEBHOOK_URL
from app.utils.logger import logger
# Initialize colorama
init(autoreset=True)

# Slack webhook URL
SLACK_WEBHOOK_URL = SLACK_WEBHOOK_URL
# ==============================
# Structured log
# ==============================

def structured_log(anomaly_data):

    log = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "NETWORK_ANOMALY",
        "severity": "HIGH",
        "data": anomaly_data
    }

    return log

# ==============================
# Console alert
# ==============================

def console_alert(anomaly_data):

    logger.warning(
        "\n===== ANOMALY ALERT ====="
    )

    logger.warning(
        f"Timestamp: {anomaly_data['timestamp']}"
    )

    logger.warning(
        f"Packet Count: {anomaly_data['packet_count']}"
    )

    logger.warning(
        f"DNS Requests: {anomaly_data['dns_requests']}"
    )

    logger.warning(
        f"Unique IPs: {anomaly_data['unique_ips']}"
    )

    logger.warning(
        f"Traffic Label: {anomaly_data['traffic_label']}"
    )

    logger.warning(
        "===========================\n"
    )

# ==============================
# JSON alert
# ==============================

def json_alert(anomaly_data):

    log = structured_log(anomaly_data)

    logger.warning("\n===== JSON ALERT =====\n"
    )

    logger.warning(json.dumps(log, indent=4))

    logger.warning(
        "\n======================\n"
    )

# ==============================
# Slack webhook alert
# ==============================

def slack_alert(anomaly_data):

    payload = {
        "text": (
            "🚨 Network Anomaly Detected\n"
            f"Packet Count: "
            f"{anomaly_data['packet_count']}\n"
            f"DNS Requests: "
            f"{anomaly_data['dns_requests']}\n"
            f"Unique IPs: "
            f"{anomaly_data['unique_ips']}\n"
            f"Traffic Label: "
            f"{anomaly_data['traffic_label']}"
        )
    }

    response = requests.post(
        SLACK_WEBHOOK_URL,
        json=payload
    )

    if response.status_code == 200:

        logger.info(
           "Slack alert sent successfully."
        )

    else:

        logger.error(
            f"Slack webhook error: "
            f"{response.status_code}"
        )

