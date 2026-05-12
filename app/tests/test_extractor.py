import pandas as pd

# ==============================
# Test dataframe creation
# ==============================

def test_dataframe_creation():

    data = {
        "packet_count": [10, 20, 30],
        "dns_requests": [1, 2, 3]
    }

    df = pd.DataFrame(data)

    assert not df.empty

# ==============================
# Test dataframe columns
# ==============================

def test_dataframe_columns():

    data = {
        "packet_count": [10],
        "dns_requests": [1]
    }

    df = pd.DataFrame(data)

    assert "packet_count" in df.columns

    assert "dns_requests" in df.columns

# ==============================
# Test dataframe row count
# ==============================

def test_dataframe_row_count():

    data = {
        "packet_count": [10, 20, 30]
    }

    df = pd.DataFrame(data)

    assert len(df) == 3