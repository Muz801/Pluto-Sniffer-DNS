import sqlite3
import pandas as pd
import json
import os
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "../storage/network_traffic.db"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "isolation_forest.pkl"
)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Read metrics table
query = "SELECT * FROM metrics"

df = pd.read_sql_query(query, conn)

print("\n===== ORIGINAL DATASET =====\n")
print(df.head())

# ==============================
# Feature extraction
# ==============================

# Extract TCP packet count
df["tcp_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("TCP", 0)
)

# Extract UDP packet count
df["udp_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("UDP", 0)
)

# Extract DNS packet count
df["dns_protocol_count"] = df["protocols"].apply(
    lambda x: json.loads(x).get("DNS", 0)
)

# ==============================
# Create ML dataset
# ==============================

dataset = df[[
    "packet_count",
    "dns_requests",
    "unique_ips",
    "tcp_count",
    "udp_count",
    "dns_protocol_count"
]]

print("\n===== ML DATASET =====\n")
print(dataset.head())

# ==============================
# Normalize data
# ==============================

scaler = MinMaxScaler()

dataset_scaled = scaler.fit_transform(dataset)

# ==============================
# Train model only if not exists
# ==============================

if not os.path.exists(MODEL_PATH):

    print("\n===== TRAINING MODEL =====\n")

    model = IsolationForest(
        contamination=0.01,
        random_state=42
    )

    model.fit(dataset_scaled)

    # Save model
    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully.")

else:

    print("\n===== LOADING MODEL =====\n")

    # Load existing model
    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully.")

# ==============================
# Real-time predictions
# ==============================

predictions = model.predict(dataset_scaled)

# Add predictions to dataframe
df["anomaly"] = predictions

# ==============================
# Traffic classification
# ==============================

df["traffic_label"] = df["anomaly"].apply(
    lambda x: "ANOMALOUS" if x == -1 else "NORMAL"
)

# ==============================
# Extract anomalies
# ==============================

anomalies = df[df["anomaly"] == -1]

print("\n===== ANOMALIES DETECTED =====\n")

print(anomalies[[
    "timestamp",
    "packet_count",
    "dns_requests",
    "unique_ips",
    "traffic_label"
]])

print(f"\nTotal anomalies detected: {len(anomalies)}")