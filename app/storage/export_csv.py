import sqlite3
import csv
import json
import os
from app.utils.logger import logger
# 📍 Ruta a la base de datos (SIEMPRE la de storage)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "network_traffic.db")

# Conexión a SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Leer todas las métricas
cursor.execute("SELECT * FROM metrics")
rows = cursor.fetchall()

# Archivo CSV de salida
csv_file = "metrics_export.csv"

# Crear CSV
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)

    # HEADER del CSV
    writer.writerow([
        "id",
        "timestamp",
        "packet_count",
        "dns_requests",
        "unique_ips",
        "protocols",
        "top_talkers"
    ])

    # DATA
    for row in rows:

        writer.writerow([
            row[0],  # id
            row[1],  # timestamp
            row[2],  # packet_count
            row[3],  # dns_requests
            row[4],  # unique_ips

            # JSON strings → objetos Python (para análisis futuro)
            json.loads(row[5]) if row[5] else {},
            json.loads(row[6]) if row[6] else {}
        ])

logger.info(f"CSV exported successfully → {csv_file}")