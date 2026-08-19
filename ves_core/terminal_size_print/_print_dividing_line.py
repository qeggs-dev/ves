import os

def dividing_line(char: str = "="):
    columns = os.get_terminal_size().columns
    if len(char) == 1:
        text = char * columns
    elif len(char) > 1:
        times = columns // len(char)
        text = char * times + char[:columns % len(char)]
    else:
        raise ValueError("No character specified")

    return text

def print_dividing_line(char: str = "="):
    print(dividing_line(char))
