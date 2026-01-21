import os

def print_dividing_line(char: str = "="):
    if len(char) < 1:
        char = char[0]
    elif len(char) == 0:
        raise ValueError("Char must be at least 1 character long")
    
    print(char * os.get_terminal_size().columns)