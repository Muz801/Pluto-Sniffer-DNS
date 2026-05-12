# ==============================
# Packet structure test
# ==============================

def test_packet_structure():

    packet = {
        "src_ip": "192.168.1.1",
        "dst_ip": "8.8.8.8",
        "protocol": "TCP"
    }

    assert packet["protocol"] == "TCP"

# ==============================
# IP existence test
# ==============================

def test_ip_existence():

    packet = {
        "src_ip": "192.168.1.1"
    }

    assert "src_ip" in packet

# ==============================
# DNS packet test
# ==============================

def test_dns_packet():

    packet = {
        "protocol": "DNS"
    }

    assert packet["protocol"] == "DNS"