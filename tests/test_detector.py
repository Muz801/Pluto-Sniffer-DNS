# ==============================
# Threshold detection test
# ==============================

def test_threshold_detection():

    packet_count = 5000

    threshold = 1000

    is_anomaly = packet_count > threshold

    assert is_anomaly is True

# ==============================
# DNS flood detection test
# ==============================

def test_dns_flood_detection():

    dns_requests = 120

    dns_threshold = 50

    is_dns_flood = dns_requests > dns_threshold

    assert is_dns_flood is True

# ==============================
# Normal traffic test
# ==============================

def test_normal_traffic():

    packet_count = 100

    threshold = 1000

    is_anomaly = packet_count > threshold

    assert is_anomaly is False

# ==============================
# Z-score spike detection test
# ==============================

def test_zscore_spike_detection():

    z_score = 4.5

    threshold = 3

    spike_detected = z_score > threshold

    assert spike_detected is True