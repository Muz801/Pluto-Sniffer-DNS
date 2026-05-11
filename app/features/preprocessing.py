import sqlite3
import pandas as pd
import json
import os
from sklearn.preprocessing import MinMaxScaler

# Ruta absoluta a la DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../storage/network_traffic.db")

# Conexión SQLite
conn = sqlite3.connect(DB_PATH)

# Leer tabla completa
query = "SELECT * FROM metrics"

df = pd.read_sql_query(query, conn)

print("\n===== ORIGINAL DATAFRAME =====\n")
print(df.head())

# ==============================
# LIMPIEZA DE DATOS
# ==============================

# Reemplazar valores nulos
df.fillna(0, inplace=True)

# ==============================
# CREAR FEATURES NUMÉRICAS
# ==============================

# Extraer TCP packets
df["tcp_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("TCP", 0)
)

# Extraer UDP packets
df["udp_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("UDP", 0)
)

# Extraer DNS packets
df["dns_protocol_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("DNS", 0)
)

print("\n===== FEATURES CREATED =====\n")
print(df[[
    "packet_count",
    "tcp_count",
    "udp_count",
    "dns_protocol_count"
]].head())

# ==============================
# NORMALIZACIÓN
# ==============================

scaler = MinMaxScaler()

columns_to_normalize = [
    "packet_count",
    "dns_requests",
    "unique_ips",
    "tcp_count",
    "udp_count",
    "dns_protocol_count"
]

df[columns_to_normalize] = scaler.fit_transform(
    df[columns_to_normalize]
)

print("\n===== NORMALIZED DATA =====\n")
print(df[columns_to_normalize].head())

print("\n===== FINAL DATAFRAME INFO =====\n")
print(df.info())