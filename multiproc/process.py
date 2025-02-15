from multiprocessing import Process

from multiproc.async_processpool import cpu_bound_func
from utils import sync_timed


@sync_timed()
def main():
    process_1 = Process(target=cpu_bound_func, args=(8000,))
    process_2 = Process(target=cpu_bound_func, args=(1000,))

    process_1.start()
    process_2.start()

    print("Starts join process 1")
    process_1.join()
    print("Starts join process 2")
    process_2.join()

    cpu_bound_func(100)


if __name__ == '__main__':
    main()
