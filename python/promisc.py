import socket
import fcntl
import ctypes
import signal
import atexit

from utils import print_info, print_error

SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914
IFF_PROMISC = 0x100


class ifreq(ctypes.Structure):
    _fields_ = [("ifr_ifrn", ctypes.c_char * 16), ("ifr_flags", ctypes.c_short)]


def set_promisc_on(sock: socket.socket, ifname: str, auto_off_signal: bool = True):
    try:
        fno = sock.fileno()
        encoded_ifname = ifname.encode("utf-8")
        ifr = ifreq()
        ifr.ifr_ifrn = bytes(encoded_ifname)
        ifr.ifr_flags = 0

        fcntl.ioctl(fno, SIOCGIFFLAGS, ifr)
        ifr.ifr_flags |= IFF_PROMISC
        fcntl.ioctl(fno, SIOCSIFFLAGS, ifr)

        if auto_off_signal:

            def signal_handler(sig, frame):
                set_promisc_off(sock, ifname)
                exit(0)

            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            atexit.register(lambda: set_promisc_off(sock, ifname))

        print_info(f"Promiscuous mode enabled on interface {ifname}")
    except Exception as err:
        print_error(f"{err}")
        raise err


def set_promisc_off(sock: socket.socket, ifname: str):
    try:
        fno = sock.fileno()
        ifname = ifname.encode("utf-8")
        ifr = ifreq()
        ifr.ifr_ifrn = bytes(ifname)
        ifr.ifr_flags = 0

        fcntl.ioctl(fno, SIOCGIFFLAGS, ifr)
        ifr.ifr_flags &= ~IFF_PROMISC
        fcntl.ioctl(fno, SIOCSIFFLAGS, ifr)

        print_info(f"Promiscuous mode disabled on interface {ifname}")

    except Exception as err:
        print_error(f"{err}")
        raise err
