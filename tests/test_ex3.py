import random
import time

from src.ex3 import counting_sort, radix_sort


def test_ex3():
    a = [random.randint(-10, 10) for _ in range(100)]
    assert sorted(a) == counting_sort(a) == radix_sort(a) == radix_sort(a)


def test_speed():
    sorts = [sorted, counting_sort, radix_sort]
    a = [random.randint(1, 1_000_000) for _ in range(100_000)]
    times = {}
    for sort in sorts:
        start = time.time()
        sort(a)
        times[sort] = time.time() - start
    print()
    for sort in sorts:
        print(f'{sort.__name__}: {times[sort]} sec')
