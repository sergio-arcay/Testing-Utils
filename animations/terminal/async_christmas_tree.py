#!/usr/bin/env python3

import asyncio
import random
import os

mutex = asyncio.Lock()

tree = list(open('tree.txt').read().rstrip())

def colored_dot(color):
    if color == 'red':
        return f'\033[91mO\033[0m'
    if color == 'green':
        return f'\033[92mO\033[0m'
    if color == 'yellow':
        return f'\033[93mO\033[0m'
    if color == 'blue':
        return f'\033[94mO\033[0m'

async def lights(color, indexes):
    off = True
    while True:
        for idx in indexes:
            tree[idx] = colored_dot(color) if off else 'O'

        async with mutex:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(''.join(tree))

        off = not off

        await asyncio.sleep(random.uniform(.5, 1.5))

yellow = []
red = []
green = []
blue = []

for i, c in enumerate(tree):
    if c == 'Y':
        yellow.append(i)
        tree[i] = 'O'
    if c == 'R':
        red.append(i)
        tree[i] = 'O'
    if c == 'G':
        green.append(i)
        tree[i] = 'O'
    if c == 'B':
        blue.append(i)
        tree[i] = 'O'

async def main():
    await asyncio.gather(
        lights('yellow', yellow),
        lights('red', red),
        lights('green', green),
        lights('blue', blue),
    )

if __name__ == '__main__':
    asyncio.run(main())