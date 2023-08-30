import threading
import time
import sys


def run_bouncing_between_walls_one_line(function, length=10):
    i = 0

    thread = threading.Thread(target=function)
    thread.start()

    while thread.is_alive():
        spaces = [" "] * (length - 1)
        spaces.insert(abs(i), "===")
        sys.stdout.write("\r" + "-[{}]-".format("".join(spaces)))
        sys.stdout.flush()
        time.sleep(.1)
        i = (2 - length) if i == (length - 1) else (i + 1)


if __name__ == '__main__':

    def action_1():
        time.sleep(5)

    run_bouncing_between_walls_one_line(action_1)
