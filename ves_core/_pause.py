import time

def pause(seconds: float | None = None):
    if seconds is None:
        while True:
            time.sleep(60)
    else:
        time.sleep(seconds)