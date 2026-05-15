# 🛡️ Pluto IDS — Network Traffic Anomaly Detection

> ⚠️ **Work in Progress** — Este proyecto está en desarrollo activo. Algunas funcionalidades pueden estar incompletas o sujetas a cambios.

Sistema de detección de intrusiones (IDS) en tiempo real construido con Python. Captura tráfico de red, analiza métricas, detecta anomalías mediante reglas de umbral y machine learning, y envía alertas por consola, JSON o Slack.

---

## 🚧 Estado del proyecto

| Módulo | Estado |
|--------|--------|
| Captura de paquetes (`sniffer.py`) | ✅ Funcional |
| Worker / cola de paquetes (`worker.py`) | ✅ Funcional |
| Almacenamiento SQLite (`database.py`) | ✅ Funcional |
| Exportación CSV (`export_csv.py`) | ✅ Funcional |
| Detección por umbrales (`anomaly.py`) | ✅ Funcional |
| Modelo ML — Isolation Forest (`model.py`) | ✅ Funcional |
| Notificaciones / Slack (`notifier.py`) | ✅ Funcional |
| API REST FastAPI (`main.py`) | ✅ Funcional |
| Dashboard / visualización | 🔧 En desarrollo |
| Tests unitarios | 🔧 En desarrollo |
| Docker / containerización | 🔧 En desarrollo |
| Documentación completa | 🔧 En desarrollo |

---

## 📋 Descripción

**Pluto IDS** es una herramienta de monitoreo de red que:

1. **Captura** paquetes en tiempo real desde una interfaz de red con Scapy
2. **Procesa** cada paquete en un worker dedicado mediante una cola concurrente
3. **Almacena** métricas agregadas en una base de datos SQLite
4. **Detecta** anomalías con dos enfoques complementarios:
   - Reglas de umbral (threshold-based) para detección inmediata
   - Modelo de machine learning `IsolationForest` para detección no supervisada
5. **Notifica** las anomalías por consola, JSON estructurado o webhook de Slack
6. **Expone** una API REST con FastAPI para consultar métricas y alertas en tiempo real

---

## 🗂️ Estructura del proyecto

```
pluto-ids/
│
├── app/
│   ├── core/
│   │   ├── sniffer.py          # Captura de paquetes con Scapy
│   │   ├── worker.py           # Worker thread para procesar la cola
│   │   ├── anomaly.py          # Detección por umbrales (threshold + z-score)
│   │   └── queue_manager.py    # Cola compartida entre sniffer y worker
│   │
│   ├── ml/
│   │   └── model.py            # Entrenamiento y predicción con Isolation Forest
│   │
│   ├── storage/
│   │   ├── database.py         # Conexión SQLite y guardado de métricas
│   │   ├── export_csv.py       # Exportación de métricas a CSV
│   │   ├── schema.sql          # Esquema de la base de datos
│   │   └── network_traffic.db  # Base de datos SQLite (generada en runtime)
│   │
│   └── utils/
│       ├── notifier.py         # Alertas: consola, JSON y Slack webhook
│       └── logger.py           # Logger centralizado
│
├── main.py                     # API REST con FastAPI
├── metrics_export.csv          # CSV exportado de métricas
└── requirements.txt
```

---

## ⚙️ Instalación

### Requisitos previos

- Python 3.10 o superior
- pip
- Permisos de administrador / root (necesarios para captura de paquetes con Scapy)

### Pasos

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd pluto-ids

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 🚀 Uso

### 1. Iniciar el sniffer (captura de paquetes)

```bash
sudo python -m app.core.sniffer
```

Al ejecutarlo, lista las interfaces disponibles y solicita seleccionar una:

```
Available interfaces:
0: eth0
1: wlan0
Select interface number: 0
Using interface: eth0
Sniffing on interface: eth0
```

### 2. Iniciar la API REST

```bash
uvicorn main:app --reload
```

### 3. Ejecutar detección por umbrales

```bash
python -m app.core.anomaly
```

### 4. Entrenar / ejecutar el modelo ML

```bash
python -m app.ml.model
```

> Si el modelo `isolation_forest.pkl` no existe, lo entrena y lo guarda automáticamente. En ejecuciones posteriores lo carga directamente.

### 5. Exportar métricas a CSV

```bash
python -m app.storage.export_csv
```

---

## 🌐 API REST — Endpoints

Base URL: `http://localhost:8000`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Estado general de la API |
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | Últimas 100 métricas registradas |
| `GET` | `/latest` | Métrica más reciente |
| `GET` | `/alerts` | Registros con anomalías detectadas |

---

## 🔍 Detección de anomalías

### Detección por umbrales (`anomaly.py`)

| Tipo de anomalía | Condición |
|-----------------|-----------|
| Alto volumen de paquetes | `packet_count > 1000` |
| DNS flood | `dns_requests > 50` |
| Muchas IPs únicas | `unique_ips > 30` |
| Traffic spike (z-score) | `z_score > 3` |
| SYN flood | `tcp_count > 1000` |

### Modelo ML (`model.py`)

Usa **Isolation Forest** con las siguientes features:

- `packet_count` — total de paquetes
- `dns_requests` — solicitudes DNS
- `unique_ips` — IPs únicas observadas
- `tcp_count` — paquetes TCP
- `udp_count` — paquetes UDP
- `dns_protocol_count` — paquetes DNS a nivel protocolo

Los datos se normalizan con `MinMaxScaler` antes del entrenamiento. El modelo clasifica cada registro como `NORMAL` o `ANOMALOUS`.

---

## 🔔 Notificaciones (`notifier.py`)

El sistema soporta tres canales de alerta:

- **Consola** — log estructurado con `colorama`
- **JSON** — log estructurado con timestamp, severidad y datos del evento
- **Slack** — mensaje enviado al webhook configurado en `config.py`

### Configurar Slack

En `config.py` (o variable de entorno):

```python
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

---

## 🗄️ Base de datos

### Esquema — tabla `metrics`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INTEGER | Clave primaria autoincremental |
| `timestamp` | TEXT | Fecha y hora del registro |
| `packet_count` | INTEGER | Total de paquetes en el intervalo |
| `dns_requests` | INTEGER | Solicitudes DNS detectadas |
| `unique_ips` | INTEGER | IPs únicas observadas |
| `protocols` | TEXT | JSON con conteo por protocolo (TCP, UDP, DNS…) |
| `top_talkers` | TEXT | JSON con las IPs más activas |

---

## 🤝 Contribuciones

Este proyecto está en desarrollo activo. Las contribuciones son bienvenidas.

1. Haz un fork del repositorio
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit de tus cambios: `git commit -m "Agrega nueva funcionalidad"`
4. Push a tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y personales.

---

> 🔧 *Este README se actualizará conforme el proyecto avance.*
