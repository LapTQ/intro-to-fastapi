# When you mark a function as `async`, it becomes a coroutine, indicating that it can be paused and resumed during its execution.
# The `await` keyword is used to signify that the coroutine should pause execution until the awaited task completes.
# During this pause, the event loop can switch to executing other tasks

import time
import asyncio
from tqdm import tqdm
from datetime import datetime


async def cashier_service_earlier_guess(name, n_guesses, choosing_period):
    print(f'[{datetime.now()}] Can you (Mr.{name}) wait for me to process {n_guesses} earlier guess?')
    await asyncio.sleep(n_guesses * choosing_period)

async def cook_make_pizza(name):
    print(f'[{datetime.now()}] Mr.{name}, I am making your pizza')
    await asyncio.sleep(10)
    print(f'[{datetime.now()}] Mr.{name}, your pizza is ready')

async def have_pizza(name, n_guesses):
    choosing_period = 3
    await cashier_service_earlier_guess(name, n_guesses, choosing_period) # wasting time

    print(f'[{datetime.now()}] Mr.{name}, please order your pizza')
    time.sleep(choosing_period) # useful task

    await cook_make_pizza(name) # wasting time


async def main():
    await asyncio.gather(
        have_pizza('HungPT', 0),
        have_pizza('DieuNH', 1),
        have_pizza('GiangND', 2),
        have_pizza('LapTQ', 3),
    )

start = time.time()
asyncio.run(
    main()
)
print('Total time:', time.time() - start)

# Let's decode the async/await:
# If we write the program sequentially, it will run like this:
# (1) - have_pizza('HungPT', 0)
# (2)   ++ cashier_service_earlier_guess('HungPT', 0, 3)
# (3)   ++ time.sleep(3)
# (4)   ++ cook_make_pizza('HungPT')
# (5) - have_pizza('DieuNH', 1)
# (6)   ++ cashier_service_earlier_guess('DieuNH', 1, 3)
# (7)   ++ time.sleep(3)
# (8)   ++ cook_make_pizza('DieuNH')
# (9) - have_pizza('GiangND', 2)
# (10)  ++ cashier_service_earlier_guess('GiangND', 2, 3)
# (11)  ++ time.sleep(3)
# (12)  ++ cook_make_pizza('GiangND')
# (13) - have_pizza('LapTQ', 3)
# (14)  ++ cashier_service_earlier_guess('LapTQ', 3, 3)
# (15)  ++ time.sleep(3)
# ... and so on
#
# But with async/await, the program will run like this:
# Here si the output:
"""
[2024-03-03 05:38:55.992165] Can you (Mr.HungPT) wait for me to process 0 earlier guess?
[2024-03-03 05:38:55.992217] Can you (Mr.DieuNH) wait for me to process 1 earlier guess?
[2024-03-03 05:38:55.992252] Can you (Mr.GiangND) wait for me to process 2 earlier guess?
[2024-03-03 05:38:55.992270] Can you (Mr.LapTQ) wait for me to process 3 earlier guess?
[2024-03-03 05:38:55.992290] Mr.HungPT, please order your pizza
[2024-03-03 05:38:58.995539] Mr.HungPT, I am making your pizza
[2024-03-03 05:38:58.996056] Mr.DieuNH, please order your pizza
[2024-03-03 05:39:01.999354] Mr.DieuNH, I am making your pizza
[2024-03-03 05:39:01.999823] Mr.GiangND, please order your pizza
[2024-03-03 05:39:05.003101] Mr.GiangND, I am making your pizza
[2024-03-03 05:39:05.003504] Mr.LapTQ, please order your pizza
[2024-03-03 05:39:08.006697] Mr.LapTQ, I am making your pizza
[2024-03-03 05:39:08.997316] Mr.HungPT, your pizza is ready
[2024-03-03 05:39:12.003880] Mr.DieuNH, your pizza is ready
[2024-03-03 05:39:15.007551] Mr.GiangND, your pizza is ready
[2024-03-03 05:39:18.010288] Mr.LapTQ, your pizza is ready
Total time: 22.019198179244995
"""
# Assume that single command except for the sleep runs in 0 seconds:
# ==> because (1) should be paused at (2), and (5) is executed immediately at this point (together with (2)). 
# Also, because (2) included an awaited function (sleep) in the very beginning, it is also paused at this point 
# ... and so on
# ==> we will see that (1, 2, 3, 5, 6, 9, 10, 13) runs at almost the same time.
# ... the rest is hard to explain, but simple to envision :D


# async: single-threaded concurrent
# threading: multi-threaded concurrent, in a single process, but GIL
# multiprocessing: multi-process parallel, each with its own Python interpreter and run independently, but need to communicate with each other