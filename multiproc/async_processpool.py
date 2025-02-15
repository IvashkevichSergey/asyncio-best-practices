import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from utils import sync_timed


@sync_timed()
def cpu_bound_func(num: int):
    """Имитирует нагрузку на процессор"""
    print('Function with num -', num)
    counter = 0
    res = []
    while counter < num:
        res.append(counter * counter)
        counter += 1
    for num_ in range(1, num):
        num_ **= num
    return f'Function with num {num} finished'


@sync_timed()
async def main():
    with ProcessPoolExecutor() as process_poll:
        running_loop = asyncio.get_running_loop()

        fns = [partial(cpu_bound_func, 5000),
               partial(cpu_bound_func, 7000),
               partial(cpu_bound_func, 6000)]

        funcs_for_perform = [running_loop.run_in_executor(process_poll, fn) for fn in fns]

        for func in asyncio.as_completed(funcs_for_perform):
            print(await func)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
