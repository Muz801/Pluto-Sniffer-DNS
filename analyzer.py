from collections import defaultdict
import time
from alerts import alert

connection_counter = defaultdict(int)
time_window = defaultdict(list)

THRESHOLD = 50  # conexiones en ventana
WINDOW_SECONDS = 10

def process_packet(packet):
    current_time = time.time()

    # --- IP layer ---
    if not packet.haslayer("IP"):
        return  # ignorar paquetes sin IP

    src = packet["IP"].src
    dst = packet["IP"].dst

    print(f"[IP] {src} -> {dst}")

    # --- Contador de conexiones (para detección) ---
    connection_counter[src] += 1
    time_window[src].append(current_time)

    # limpiar ventana (últimos N segundos)
    time_window[src] = [
        t for t in time_window[src]
        if current_time - t < WINDOW_SECONDS
    ]

    if len(time_window[src]) > THRESHOLD:
        alert(f"Tráfico anormal desde {src}")

    # --- TCP ---
    if packet.haslayer("TCP"):
        tcp = packet["TCP"]
        print(f"[TCP] {tcp.sport} -> {tcp.dport}")

    # --- UDP ---
    if packet.haslayer("UDP"):
        udp = packet["UDP"]
        print(f"[UDP] {udp.sport} -> {udp.dport}")

    # --- DNS ---
    if packet.haslayer("DNS") and packet.haslayer("DNSQR"):
        domain = packet["DNSQR"].qname.decode().strip(".")

        print(f"[DNS] {domain}")

        # detección simple
        if "xyz" in domain or len(domain) > 50:
            alert(f"Dominio sospechoso: {domain}")