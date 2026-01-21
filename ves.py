from ves_core import (
    VESCLI,
    VES_Windows,
    VES_Linux,
    VES_Darwin,
)
import platform
import sys

def main():
    match platform.system():
        case "Windows":
            ves = VES_Windows(print_run_statistics=True)
        case "Linux":
            ves = VES_Linux(print_run_statistics=True)
        case "Darwin":
            ves = VES_Darwin(print_run_statistics=True)
        case _:
            raise NotImplementedError("Unsupported OS")
    cli = VESCLI(ves)
    return cli.main()

if __name__ == "__main__":
    sys.exit(main())