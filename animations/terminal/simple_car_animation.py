"""
Source:

    https://github.com/v1nam

NOTES:

    - It's a must to exec this script from a terminal!

"""
import os
import time


car = """

  ______
 /|_||_\`.__
(   _    _ _\\
=`-(_)--(_)-'

"""

car = car.strip("\n")
size = os.get_terminal_size().columns - 13
height = os.get_terminal_size().lines

while True:

    for i in range(size):

        parts = car.split("\n")
        parts[-1] += "_"*(size - i)
        parts[-1] = "_"*i + parts[-1]

        for k in range(3):
            parts[k] = " "*i + parts[k]

        os.system("clear")  # Some terminals do not support this command!

        print("\n"*(height//2))
        print("\n".join(parts))

        time.sleep(0.04)
