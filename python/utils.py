RESET = "\033[0m"
WHITE = "\033[0;37m"
LIGHT_RED = "\033[1;31m"
LIGHT_PURPLE = "\033[1;35m"
BOLD = "\033[1m"


def print_info(*args):
    """
    Simply print content in bold cyan
    """
    print(f"{BOLD}{WHITE}[{LIGHT_PURPLE}INFO{WHITE}] - {' '.join(args)}{RESET}")


def print_error(*args):
    """
    Simply print content in bold red
    """
    print(f"{BOLD}{WHITE}[{LIGHT_RED}ERROR{WHITE}] - {' '.join(args)}{RESET}")
