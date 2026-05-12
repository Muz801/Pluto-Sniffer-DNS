import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database config
DATABASE_PATH = os.getenv(
    "DATABASE_PATH"
)

# Slack webhook
SLACK_WEBHOOK_URL = os.getenv(
    "SLACK_WEBHOOK_URL"
)

# API config
API_HOST = os.getenv(
    "API_HOST"
)

API_PORT = os.getenv(
    "API_PORT"
)