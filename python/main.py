import argparse

from capture import capture
from utils import print_error
from hexdump import print_content_in_box, hexdump_in_box

if __name__ == "__main__":
    # hexdump_in_box([0x01, 0x02, 0x03, 0x04, 0x05, 0x06], 0, 6, 16)
    arg_parser = argparse.ArgumentParser(description="Packet capture tool")
    arg_parser.add_argument("interface", help="Interface to capture packets from")
    arg_parser.add_argument("-p", action="store_true", help="Enable promiscuous mode")
    args = arg_parser.parse_args()

    if not args.interface or args.interface == "":
        print_error("Interface name cannot be empty")
        exit(1)

    capture(args.interface, args.p)
