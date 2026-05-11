import sqlite3
import pandas as pd
import os
import json

# Ruta DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../storage/network_traffic.db")

# Conexión SQLite
conn = sqlite3.connect(DB_PATH)

# Leer datos
query = "SELECT * FROM metrics"

df = pd.read_sql_query(query, conn)

print("\n===== NETWORK ANOMALY DETECTION =====\n")

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

print("\n===== THRESHOLD ANOMALIES =====\n")

if threshold_anomalies.empty:

    print("No threshold anomalies detected.")

else:

    print(threshold_anomalies[[
        "timestamp",
        "packet_count",
        "dns_requests",
        "unique_ips"
    ]])

    print(
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

print("\n===== TRAFFIC SPIKES =====\n")

if spikes.empty:

    print("No traffic spikes detected.")

else:

    print(spikes[[
        "timestamp",
        "packet_count",
        "rolling_avg",
        "z_score"
    ]])

    print(f"\nTotal spikes detected: {len(spikes)}")

# ==============================
# DNS FLOOD DETECTION
# ==============================

DNS_FLOOD_THRESHOLD = 50

dns_floods = df[
    df["dns_requests"] > DNS_FLOOD_THRESHOLD
]

print("\n===== DNS FLOODS =====\n")

if dns_floods.empty:

    print("No DNS floods detected.")

else:

    print(dns_floods[[
        "timestamp",
        "dns_requests",
        "packet_count"
    ]])

    print(f"\nTotal DNS floods: {len(dns_floods)}")

# ==============================
# SYN FLOOD DETECTION
# ==============================

SYN_THRESHOLD = 1000

syn_floods = df[
    df["tcp_count"] > SYN_THRESHOLD
]

print("\n===== SYN FLOODS =====\n")

if syn_floods.empty:

    print("No SYN floods detected.")

else:

    print(syn_floods[[
        "timestamp",
        "tcp_count",
        "packet_count"
    ]])

    print(f"\nTotal SYN floods: {len(syn_floods)}")