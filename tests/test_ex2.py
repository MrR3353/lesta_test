import time
from pympler import asizeof

from src.ex2 import CycledFIFOBufferList, CycledFIFOBufferArray, CycledFIFOBufferNodes, CycledFIFOBufferQueue, \
    CycledFIFOBufferDequeue, CycledFIFOBufferDict, CycledFIFOBufferFixedList


def test_ex2():
    buffers = [CycledFIFOBufferList(5),
               CycledFIFOBufferArray(5, 'i'),
               CycledFIFOBufferNodes(5),
               CycledFIFOBufferQueue(5),
               CycledFIFOBufferDequeue(5),
               CycledFIFOBufferDict(5),
               CycledFIFOBufferFixedList(5)]

    for buff in buffers:
        lst = []
        for i in range(1, 6):
            buff.push(i)
            lst.append(i)

        for i in range(1, 6):
            assert buff.pop() == lst.pop(0)

        for i in range(1, 10):
            buff.push(i)
        for i in range(5, 10):
            assert buff.pop() == i
        assert buff.size() == 0

        for i in range(1, 10):
            buff.push(i)
        assert buff.size() == 5
        buff.clear()
        assert buff.size() == 0


def test_speed_and_memory():
    size = 1000
    buffers = [CycledFIFOBufferList(size),
               CycledFIFOBufferArray(size, 'i'),
               CycledFIFOBufferNodes(size),
               CycledFIFOBufferQueue(size),
               CycledFIFOBufferDequeue(size),
               CycledFIFOBufferDict(size),
               CycledFIFOBufferFixedList(size)]
    times = {}
    for buff in buffers:
        start = time.time()
        for i in range(100_000):
            buff.push(i)
            if i % 2 == 0:
                buff.pop()
        times[buff.__class__] = time.time() - start
    print()
    buffers.sort(key=lambda b: times[b.__class__])
    for buff in buffers:
        print(f'{buff.__class__.__name__}: {times[buff.__class__]} sec, {asizeof.asizeof(buff)} bytes')
