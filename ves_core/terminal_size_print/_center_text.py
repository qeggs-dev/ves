import os

def center_title(title: str):
    print(title.center(os.get_terminal_size().columns))