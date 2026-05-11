import sqlite3
import pandas as pd
import os

from fastapi import FastAPI

# ==============================
# FastAPI app
# ==============================

app = FastAPI()

# ==============================
# Database path
# ==============================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "../storage/network_traffic.db"
)

# ==============================
# Database connection
# ==============================

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

# ==============================
# Root endpoint
# ==============================

@app.get("/")

def root():

    return {
        "message": "Pluto IDS API running"
    }

# ==============================
# Health endpoint
# ==============================

@app.get("/health")

def health():

    return {
        "status": "healthy"
    }

# ==============================
# Metrics endpoint
# ==============================

@app.get("/metrics")

def get_metrics():

    query = """
        SELECT *
        FROM metrics
        ORDER BY id DESC
        LIMIT 100
    """

    df = pd.read_sql_query(query, conn)

    return df.to_dict(orient="records")

# ==============================
# Latest metric endpoint
# ==============================

@app.get("/latest")

def get_latest():

    query = """
        SELECT *
        FROM metrics
        ORDER BY id DESC
        LIMIT 1
    """

    df = pd.read_sql_query(query, conn)

    return df.to_dict(orient="records")

# ==============================
# Alerts endpoint
# ==============================

@app.get("/alerts")

def get_alerts():

    query = """
        SELECT *
        FROM metrics
        WHERE packet_count > 1000
        OR dns_requests > 50
        ORDER BY id DESC
        LIMIT 50
    """

    df = pd.read_sql_query(query, conn)

    return df.to_dict(orient="records")