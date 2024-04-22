from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT_DIR = HERE.parent.parent

sys.path.append(str(ROOT_DIR))

from src.utils.mics import timing

# ==============================================================================

import time
from threading import Thread
import asyncio


def countdown(n):
    while n > 0:
        n -= 1

@timing
def sequential(n):
    countdown(n)


@timing
def multithread(n):
    t1 = Thread(target=countdown, args=(n//2,))
    t2 = Thread(target=countdown, args=(n//2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    for r in range(5):
        print(f"*** Round {r + 1} ***")
        n = 100000000
        sequential(n)
        multithread(n)
    print('Do you see that multithread is slower than sequential?')
        
