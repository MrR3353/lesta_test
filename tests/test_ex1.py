import time

from src.ex1 import isEven, myIsEven


def test_ex1():
    for i in range(-1000, 1000):
        assert isEven(i) == myIsEven(i)


def test_speed():
    b, e = -1_000_000, 5_000_000
    start = time.time()
    for i in range(b, e):
        isEven(i)
    isEven_time = time.time() - start

    start = time.time()
    for i in range(b, e):
        myIsEven(i)
    myIsEven_time = time.time() - start
    print(f'\nisEven_time = {isEven_time}\nmyIsEven = {myIsEven_time}')
    assert myIsEven_time <= isEven_time