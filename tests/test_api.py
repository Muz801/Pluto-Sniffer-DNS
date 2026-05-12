from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)

# ==============================
# Root endpoint test
# ==============================

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

# ==============================
# Health endpoint test
# ==============================

def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"

# ==============================
# Metrics endpoint test
# ==============================

def test_metrics_endpoint():

    response = client.get("/metrics")

    assert response.status_code == 200

# ==============================
# Latest endpoint test
# ==============================

def test_latest_endpoint():

    response = client.get("/latest")

    assert response.status_code == 200

# ==============================
# Alerts endpoint test
# ==============================

def test_alerts_endpoint():

    response = client.get("/alerts")

    assert response.status_code == 200