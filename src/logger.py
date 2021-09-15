class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(message, color=None, end="\n", flush=True):
    if color:
        print(f"{color}{message}{bcolors.ENDC}", end=end, flush=flush)
    else:
        print(message, end=end, flush=flush)
