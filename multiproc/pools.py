from multiprocessing import Pool

from utils import sync_timed
from multiproc.async_processpool import cpu_bound_func


@sync_timed()
def main():
    with Pool(4) as pool:
        res_1 = pool.apply_async(func=cpu_bound_func, args=(5000,))
        res_2 = pool.apply_async(func=cpu_bound_func, args=(8000,))
        res_3 = pool.apply_async(func=cpu_bound_func, args=(6000,))
        res_4 = pool.apply_async(func=cpu_bound_func, args=(8000,))
        print(res_1.get())
        print(res_2.get())
        print(res_3.get())
        print(res_4.get())


if __name__ == '__main__':
    main()
