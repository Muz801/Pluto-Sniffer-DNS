from scapy.all import sniff, get_if_list
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.dns import DNS
import time
from collections import defaultdict


# Packet counter
packet_count = 0

# Track packet rate
start_time = time.time()

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


# Process captured packets
def process_packet(packet):

    global packet_count
    global start_time

    # Count packets
    packet_count += 1

    # Calculate packets per second
    elapsed_time = time.time() - start_time

    if elapsed_time >= 1:

        print(f"\n[METRICS] Packets/sec: {packet_count}")

        packet_count = 0
        start_time = time.time()

    # Check IP layer
    if packet.haslayer(IP):

        # Extract source IP
        src_ip = packet[IP].src

        # Extract destination IP
        dst_ip = packet[IP].dst

        print(f"\n[IP]")
        print(f"Source IP: {src_ip}")
        print(f"Destination IP: {dst_ip}")

    # Check TCP layer
    if packet.haslayer(TCP):

        # Extract ports
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        print(f"[TCP]")
        print(f"Source Port: {src_port}")
        print(f"Destination Port: {dst_port}")

        # Detect SYN packets
        if packet[TCP].flags == "S":

            print("[ALERT] SYN packet detected")

    # Check UDP layer
    if packet.haslayer(UDP):

        # Extract ports
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport

        print(f"[UDP]")
        print(f"Source Port: {src_port}")
        print(f"Destination Port: {dst_port}")

    # Check DNS layer
    if packet.haslayer(DNS):

        print("[DNS] DNS packet detected")


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