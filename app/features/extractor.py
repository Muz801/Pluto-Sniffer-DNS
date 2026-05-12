import sqlite3
import pandas as pd
import os
from app.utils.logger import logger
# Ruta absoluta a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../storage/network_traffic.db")

# Conexión SQLite
conn = sqlite3.connect(DB_PATH)

# Leer tabla metrics completa
query = "SELECT * FROM metrics"

# Crear DataFrame con pandas
df = pd.read_sql_query(query, conn)

# Mostrar DataFrame
logger.info("\n===== DATAFRAME =====\n")
logger.info(df)

# Mostrar información general
logger.info("\n===== DATAFRAME INFO =====\n")
logger.info(df.info())

# Mostrar estadísticas básicas
logger.info("\n===== DATAFRAME STATS =====\n")
logger.info(df.describe())