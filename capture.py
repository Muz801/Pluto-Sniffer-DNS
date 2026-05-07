from scapy.all import sniff
from analyzer import process_packet

def start_sniffer():
    sniff(
        filter="udp port 53",
        prn=process_packet,
        store=False,
        timeout=60
    )