import os
import sqlite3
import json

# Ruta ABSOLUTA a storage/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "network_traffic.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

print("USING DB:", DB_PATH)


def save_metrics(metrics):

    cursor.execute("""
        INSERT INTO metrics (
            timestamp,
            packet_count,
            dns_requests,
            unique_ips,
            protocols,
            top_talkers
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        metrics["timestamp"],
        metrics["packet_count"],
        metrics["dns_requests"],
        metrics["unique_ips"],
        json.dumps(metrics["protocols"]),
        json.dumps(metrics["top_talkers"])
    ))

    conn.commit()