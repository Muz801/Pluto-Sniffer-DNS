from app.alerts.notifier import slack_alert

test_alert = {
    "timestamp": "2026-01-01",
    "packet_count": 9999,
    "dns_requests": 200,
    "unique_ips": 50,
    "traffic_label": "ANOMALOUS"
}

slack_alert(test_alert)