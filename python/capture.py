import socket

from promisc import set_promisc_on
from hexdump import print_dump, hexdump_in_box
from utils import print_info, print_error

PKT_SIZE = 2048


def capture(ifname: str, promisc: bool):
    try:
        sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        sock.bind((ifname, 0))
    except Exception as err:
        print_error(f"Error: {err}")
        exit(1)

    if promisc:
        set_promisc_on(sock, ifname)

    print_info(f"Capturing packets on interface {ifname}")

    while True:
        packet = list(sock.recv(PKT_SIZE))
        hexdump_in_box(packet, 0, len(packet), 16)
        print("")  # Skip line between packets
