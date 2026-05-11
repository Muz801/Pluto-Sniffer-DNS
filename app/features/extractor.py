import sqlite3
import pandas as pd
import os

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
print("\n===== DATAFRAME =====\n")
print(df)

# Mostrar información general
print("\n===== DATAFRAME INFO =====\n")
print(df.info())

# Mostrar estadísticas básicas
print("\n===== DATAFRAME STATS =====\n")
print(df.describe())