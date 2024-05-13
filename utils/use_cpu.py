"""
Some free tiers will reclaim a VM if resource usage is low.
Create some artificial load.

Create a high load for at least a minute
"""
import datetime as dt
import time
import os
import multiprocessing

def time_consuming_task(number=90000000):
    result = sum(i * i for i in range(number))
    return result


if __name__ == "__main__":
    logical_processors = os.cpu_count()
    print(f"Found {logical_processors} logical processors")
    start_time = time.time()
    while time.time() - start_time < 120:
        print(f"{dt.datetime.now().isoformat()} - Create a batch of tasks")
        processes = []
        for _ in range(logical_processors):
            processes.append(multiprocessing.Process(target=time_consuming_task))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
    
    print(f"Generated CPU load for {time.time() - start_time:.2f} seconds")
