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

print("\n===== TRAFFIC ANALYSIS =====\n")

# ==============================
# ROLLING AVERAGE
# ==============================

# Media móvil de packet_count
df["rolling_avg"] = df["packet_count"].rolling(window=10).mean()

# ==============================
# Z-SCORE
# ==============================

# Media global
mean_packets = df["packet_count"].mean()

# Desviación estándar
std_packets = df["packet_count"].std()

# Calcular z-score
df["z_score"] = (
    (df["packet_count"] - mean_packets)
    / std_packets
)

# ==============================
# DETECTAR SPIKES
# ==============================

# Threshold z-score
Z_THRESHOLD = 3

# Detectar anomalías
spikes = df[df["z_score"] > Z_THRESHOLD]

# ==============================
# RESULTADOS
# ==============================

print("\n===== SPIKES DETECTED =====\n")

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