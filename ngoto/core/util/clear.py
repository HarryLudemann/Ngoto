import os


def clear_screen():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    return True
