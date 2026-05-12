import logging
import os

from logging.handlers import RotatingFileHandler

# ==============================
# Create logs directory
# ==============================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "../../logs"
)

os.makedirs(LOG_DIR, exist_ok=True)

# ==============================
# Log format
# ==============================

LOG_FORMAT = (
    "%(asctime)s - "
    "%(levelname)s - "
    "%(message)s"
)

formatter = logging.Formatter(LOG_FORMAT)

# ==============================
# Main logger
# ==============================

logger = logging.getLogger("pluto")

logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False

# ==============================
# INFO log handler
# ==============================

info_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "info.log"),
    maxBytes=1024 * 1024,
    backupCount=5
)

info_handler.setLevel(logging.INFO)

info_handler.setFormatter(formatter)

# ==============================
# ERROR log handler
# ==============================

error_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "error.log"),
    maxBytes=1024 * 1024,
    backupCount=5
)

error_handler.setLevel(logging.ERROR)

error_handler.setFormatter(formatter)

# ==============================
# Console handler
# ==============================

console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)

console_handler.setFormatter(formatter)

# ==============================
# Add handlers
# ==============================

if not logger.handlers:

    logger.addHandler(info_handler)

    logger.addHandler(error_handler)

    logger.addHandler(console_handler)