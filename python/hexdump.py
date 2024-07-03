import sys

CROSS = "╋"  # cross
TOP_LEFT = "┏"  # top left corner
TOP_RIGHT = "┓"  # top right corner
BOTTOM_LEFT = "┗"  # bottom left corner
BOTTOM_RIGHT = "┛"  # bottom right corner
LEFT_T = "┣"  # left T
RIGHT_T = "┫"  # right T
TOP_T = "┳"  # top T
BOTTOM_T = "┻"  # bottom T
VERTICAL = "┃"  # vertical line
HORIZONTAL = "━"  # horizontal line


def print_content_in_box(content: str) -> None:
    content_lines = content.split("\n")
    max_line_len = max([len(line) for line in content_lines])

    print(f"{TOP_LEFT}{HORIZONTAL * max_line_len}{TOP_RIGHT}")

    for line in content_lines:
        print(f"{VERTICAL}{line.ljust(max_line_len)}{VERTICAL}")

    print(f"{BOTTOM_LEFT}{HORIZONTAL * max_line_len}{BOTTOM_RIGHT}")


def print_line(buffer: list[int], offset: int, line_len: int) -> None:
    sys.stdout.write(f"{offset:06x} |")

    num_bytes = len(buffer)

    for i in range(line_len):
        if i > 0 and i % 4 == 0:
            sys.stdout.write(" ")
        if i < num_bytes:
            sys.stdout.write(f" {buffer[i]:02x}")
        else:
            sys.stdout.write("   ")

    sys.stdout.write(" | ")

    for i in range(num_bytes):
        if 31 < buffer[i] < 127:
            sys.stdout.write(chr(buffer[i]))
        else:
            sys.stdout.write(".")

    sys.stdout.write("\n")


def print_dump(content: list[int], offset: int, to_read: int, line_len: int) -> None:
    for i in range(0, to_read, line_len):
        print_line(content[i : i + line_len], offset + i, line_len)


def hexdump_in_box(
    content: list[int], offset: int, to_read: int, line_len: int
) -> None:
    """
    ┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
    ┃ 000000 ┃ 01 00 5e 7f  ff fa 00 15  5d b7 c6 7d  08 00 45 00 ┃ ..^.....]..}..E. ┃
    ┃ 000001 ┃ 10 11 12 13  14 15 16 17  18 19 1a 1b  1c 1d 1e 1f ┃ ................ ┃
    ┃ 000002 ┃ 00 cb 41 73  00 00 01 11  4b 98 ac 1b  90 01 ef ff ┃ ..As....K....... ┃
    ┃ 000003 ┃ ff ff 00 00  00 00 00 00  00 00 00 00  00 00 00 00 ┃ ................ ┃
    ┃ 000004 ┃ 00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 ┃ ................ ┃
    ┗━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┛
    """
    sys.stdout.write(
        f"{TOP_LEFT}{HORIZONTAL * 8}{TOP_T}{HORIZONTAL * (line_len * 3 + 4)}{TOP_T}{HORIZONTAL * 18}{TOP_RIGHT}\n"
    )
    num_lines = (to_read // line_len) + 1

    for i in range(num_lines):
        sys.stdout.write(f"{VERTICAL} {offset + i:06x} {VERTICAL}")

        for j in range(line_len):
            if j > 0 and j % 4 == 0:
                sys.stdout.write(" ")
            if i * line_len + j < to_read:
                sys.stdout.write(f" {content[i * line_len + j]:02x}")
            else:
                sys.stdout.write(" 00")

        sys.stdout.write(f" {VERTICAL} ")

        for j in range(line_len):
            if i * line_len + j < to_read:
                if 31 < content[i * line_len + j] < 127:
                    sys.stdout.write(chr(content[i * line_len + j]))
                else:
                    sys.stdout.write(".")
            else:
                sys.stdout.write(" ")

        sys.stdout.write(f" {VERTICAL}\n")

    sys.stdout.write(
        f"{BOTTOM_LEFT}{HORIZONTAL * 8}{BOTTOM_T}{HORIZONTAL * (line_len * 3 + 4)}{BOTTOM_T}{HORIZONTAL * 18}{BOTTOM_RIGHT}\n"
    )
