import sqlite3
import pandas as pd
import os
import json
from app.utils.logger import logger
# Ruta DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../storage/network_traffic.db")

# Conexión SQLite
conn = sqlite3.connect(DB_PATH)

# Leer datos
query = "SELECT * FROM metrics"

df = pd.read_sql_query(query, conn)

logger.info("\n===== NETWORK ANOMALY DETECTION =====\n")

# ==============================
# EXTRAER FEATURES NUMÉRICAS
# ==============================

# TCP packets
df["tcp_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("TCP", 0)
)

# UDP packets
df["udp_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("UDP", 0)
)

# ==============================
# THRESHOLD DETECTION
# ==============================

PACKET_THRESHOLD = 1000
DNS_THRESHOLD = 50
UNIQUE_IP_THRESHOLD = 30

threshold_anomalies = df[
    (df["packet_count"] > PACKET_THRESHOLD) |
    (df["dns_requests"] > DNS_THRESHOLD) |
    (df["unique_ips"] > UNIQUE_IP_THRESHOLD)
]

logger.warning("\n===== THRESHOLD ANOMALIES =====\n")

if threshold_anomalies.empty:

    logger.info("No threshold anomalies detected.")

else:

    logger.warning(threshold_anomalies[[
        "timestamp",
        "packet_count",
        "dns_requests",
        "unique_ips"
    ]])

    logger.warning(
        f"\nTotal threshold anomalies: "
        f"{len(threshold_anomalies)}"
    )

# ==============================
# ROLLING AVERAGE
# ==============================

df["rolling_avg"] = (
    df["packet_count"]
    .rolling(window=10)
    .mean()
)

# ==============================
# Z-SCORE
# ==============================

mean_packets = df["packet_count"].mean()

std_packets = df["packet_count"].std()

df["z_score"] = (
    (df["packet_count"] - mean_packets)
    / std_packets
)

# ==============================
# SPIKE DETECTION
# ==============================

Z_THRESHOLD = 3

spikes = df[
    df["z_score"] > Z_THRESHOLD
]

logger.warning("\n===== TRAFFIC SPIKES =====\n")

if spikes.empty:

    logger.info("No traffic spikes detected.")

else:

    logger.warning(spikes[[
        "timestamp",
        "packet_count",
        "rolling_avg",
        "z_score"
    ]])

    logger.warning(f"\nTotal spikes detected: {len(spikes)}")

# ==============================
# DNS FLOOD DETECTION
# ==============================

DNS_FLOOD_THRESHOLD = 50

dns_floods = df[
    df["dns_requests"] > DNS_FLOOD_THRESHOLD
]

logger.warning("\n===== DNS FLOODS =====\n")

if dns_floods.empty:

    logger.info("No DNS floods detected.")

else:

    logger.warning(dns_floods[[
        "timestamp",
        "dns_requests",
        "packet_count"
    ]])

    logger.warning(f"\nTotal DNS floods: {len(dns_floods)}")

# ==============================
# SYN FLOOD DETECTION
# ==============================

SYN_THRESHOLD = 1000

syn_floods = df[
    df["tcp_count"] > SYN_THRESHOLD
]

logger.warning("\n===== SYN FLOODS =====\n")

if syn_floods.empty:

    logger.info("No SYN floods detected.")

else:

    logger.warning(syn_floods[[
        "timestamp",
        "tcp_count",
        "packet_count"
    ]])

    logger.warning(f"\nTotal SYN floods: {len(syn_floods)}")