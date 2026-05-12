import sqlite3
import pandas as pd
import json
import os
from sklearn.preprocessing import MinMaxScaler
from app.utils.logger import logger
# Ruta absoluta a la DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../storage/network_traffic.db")

# Conexión SQLite
conn = sqlite3.connect(DB_PATH)

# Leer tabla completa
query = "SELECT * FROM metrics"

df = pd.read_sql_query(query, conn)

logger.info("\n===== ORIGINAL DATAFRAME =====\n")
logger.info(df.head())

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

logger.info("\n===== FEATURES CREATED =====\n")
logger.info(df[[
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

logger.info("\n===== NORMALIZED DATA =====\n")
logger.info(df[columns_to_normalize].head())

logger.info("\n===== FINAL DATAFRAME INFO =====\n")
logger.info(df.info())