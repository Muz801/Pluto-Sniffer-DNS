from app.alerts.notifier import structured_log

# ==============================
# Structured log test
# ==============================

def test_structured_log():

    anomaly_data = {
        "packet_count": 5000,
        "dns_requests": 100,
        "unique_ips": 20,
        "traffic_label": "ANOMALOUS"
    }

    log = structured_log(anomaly_data)

    assert log["severity"] == "HIGH"

    assert log["event_type"] == "NETWORK_ANOMALY"

# ==============================
# Traffic label test
# ==============================

def test_traffic_label():

    anomaly_data = {
        "traffic_label": "ANOMALOUS"
    }

    assert anomaly_data["traffic_label"] == "ANOMALOUS"