import json
from datetime import datetime

# ==============================
# Console alert
# ==============================

def console_alert(anomaly_data):

    print("\n===== ANOMALY ALERT =====")

    print(f"Timestamp: {anomaly_data['timestamp']}")
    print(f"Packet Count: {anomaly_data['packet_count']}")
    print(f"DNS Requests: {anomaly_data['dns_requests']}")
    print(f"Unique IPs: {anomaly_data['unique_ips']}")
    print(f"Traffic Label: {anomaly_data['traffic_label']}")

    print("===========================\n")

# ==============================
# JSON alert
# ==============================

def json_alert(anomaly_data):

    alert = {
        "alert_timestamp": datetime.now().isoformat(),
        "anomaly_data": anomaly_data
    }

    print("\n===== JSON ALERT =====\n")

    print(json.dumps(alert, indent=4))

    print("\n======================\n")