CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    packet_count INTEGER,
    dns_requests INTEGER,
    unique_ips INTEGER,
    protocols TEXT,
    top_talkers TEXT
);