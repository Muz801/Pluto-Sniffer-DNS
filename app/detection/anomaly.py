import sqlite3
import pandas as pd
import os

# Ruta DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../storage/network_traffic.db")

# Conexión SQLite
conn = sqlite3.connect(DB_PATH)

# Leer datos
query = "SELECT * FROM metrics"

df = pd.read_sql_query(query, conn)

print("\n===== THRESHOLD DETECTION =====\n")

# Thresholds básicos
PACKET_THRESHOLD = 1000
DNS_THRESHOLD = 50
UNIQUE_IP_THRESHOLD = 30

# Detectar anomalías
anomalies = df[
    (df["packet_count"] > PACKET_THRESHOLD) |
    (df["dns_requests"] > DNS_THRESHOLD) |
    (df["unique_ips"] > UNIQUE_IP_THRESHOLD)
]

# Mostrar anomalías
if anomalies.empty:

    print("No anomalies detected.")

else:

    print(anomalies[[
        "timestamp",
        "packet_count",
        "dns_requests",
        "unique_ips"
    ]])

    print(f"\nTotal anomalies detected: {len(anomalies)}")