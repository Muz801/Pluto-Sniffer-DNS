import json
import requests

from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Slack webhook URL
SLACK_WEBHOOK_URL = ""
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

    print(
        Fore.RED +
        "\n===== ANOMALY ALERT ====="
    )

    print(
        Fore.YELLOW +
        f"Timestamp: {anomaly_data['timestamp']}"
    )

    print(
        Fore.CYAN +
        f"Packet Count: {anomaly_data['packet_count']}"
    )

    print(
        Fore.CYAN +
        f"DNS Requests: {anomaly_data['dns_requests']}"
    )

    print(
        Fore.CYAN +
        f"Unique IPs: {anomaly_data['unique_ips']}"
    )

    print(
        Fore.GREEN +
        f"Traffic Label: {anomaly_data['traffic_label']}"
    )

    print(
        Fore.RED +
        "===========================\n"
    )

# ==============================
# JSON alert
# ==============================

def json_alert(anomaly_data):

    log = structured_log(anomaly_data)

    print(
        Fore.MAGENTA +
        "\n===== JSON ALERT =====\n"
    )

    print(json.dumps(log, indent=4))

    print(
        Fore.MAGENTA +
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

        print(
            Fore.GREEN +
            "Slack alert sent successfully."
        )

    else:

        print(
            Fore.RED +
            f"Slack webhook error: "
            f"{response.status_code}"
        )

