from scapy.all import sniff, get_if_list
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.dns import DNS
from collections import defaultdict
import time
from collections import defaultdict, deque
from app.storage.database import save_metrics
from datetime import datetime


# Packet metrics
packet_count = 0
dns_requests = 0

# Protocol counters
protocol_counter = defaultdict(int)

# Unique IP tracker
unique_ips = set()

# Track packets/sec
start_time = time.time()

# Track top talkers
ip_counter = defaultdict(int)

# Temporary packet buffer
packet_buffer = deque(maxlen=1000)

# List available network interfaces
def detect_interface():

    interfaces = get_if_list()

    print("\nAvailable interfaces:\n")

    for index, interface in enumerate(interfaces):
        print(f"{index}: {interface}")

    selected = input("\nSelect interface number: ")

    chosen_interface = interfaces[int(selected)]

    print(f"\nUsing interface: {chosen_interface}")

    return chosen_interface

def process_packet(packet):

    global packet_count
    global dns_requests
    global start_time

    packet_count += 1
    packet_buffer.append(packet)

    # ===== IP LAYER =====
    if packet.haslayer(IP):

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        unique_ips.add(src_ip)
        unique_ips.add(dst_ip)

        ip_counter[src_ip] += 1

    # ===== TCP LAYER =====
    if packet.haslayer(TCP):

        protocol_counter["TCP"] += 1

    # Detect SYN
        if packet[TCP].flags == "S":
            pass  # (luego puedes alertar aquí)

    # ===== UDP LAYER =====
    if packet.haslayer(UDP):

        protocol_counter["UDP"] += 1

    # ===== DNS LAYER =====
    if packet.haslayer(DNS):

        protocol_counter["DNS"] += 1
        dns_requests += 1

    # ===== TIME WINDOW =====
    elapsed_time = time.time() - start_time

    if elapsed_time >= 5:

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "packet_count": packet_count,
            "dns_requests": dns_requests,
            "unique_ips": len(unique_ips),
            "protocols": dict(protocol_counter),
            "top_talkers": dict(ip_counter)
        }

        save_metrics(metrics)


        print("\n========== METRICS (5s WINDOW) ==========")

        print(f"Packets: {packet_count}")
        print(f"DNS Requests: {dns_requests}")
        print(f"Unique IPs: {len(unique_ips)}")

        print("\nProtocols:")
        for protocol, count in protocol_counter.items():
            print(f"  - {protocol}: {count}")

        print("\nTop Talkers:")
        top_talkers = sorted(ip_counter.items(), key=lambda x: x[1], reverse=True)[:5]

        for ip, count in top_talkers:
            print(f"  - {ip}: {count} packets")

        print("=========================================\n")

        packet_count = 0
        dns_requests = 0
        protocol_counter.clear()
        unique_ips.clear()
        ip_counter.clear()

        start_time = time.time()


# Start packet sniffing
def start_sniffer(interface):

    print(f"\nSniffing on interface: {interface}\n")

    sniff(
        iface=interface,
        prn=process_packet,
        store=False
    )


if __name__ == "__main__":

    interface = detect_interface()

    start_sniffer(interface)