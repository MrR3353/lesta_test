import array
import collections
import queue


# -: примерно в 2 раза медленее CycledFIFOBufferDequeue
# -: занимает больше всего места
class CycledFIFOBufferList:
    def __init__(self, max_size):
        self.__data = []
        self.max_size = max_size

    def push(self, item):
        self.__data.append(item)
        if len(self.__data) > self.max_size:
            self.__data.pop(0)

    def pop(self):
        if len(self.__data) == 0:
            raise BufferError("pop from empty buffer")
        return self.__data.pop(0)

    def clear(self):
        self.__data.clear()

    def size(self):
        return len(self.__data)


class CycledFIFOBufferFixedList:
    def __init__(self, max_size):
        self.__data = [None] * max_size
        self.__old = 0
        self.__new = 0
        self.max_size = max_size

    def push(self, item):
        if self.size() == self.max_size:
            self.__old += 1
        self.__data[self.__new % self.max_size] = item
        self.__new += 1

    def pop(self):
        if self.size() == 0:
            raise BufferError("pop from empty buffer")
        self.__old += 1
        return self.__data[(self.__old - 1) % self.max_size]

    def clear(self):
        self.__data = [None] * self.max_size
        self.__old = 0
        self.__new = 0

    def size(self):
        return self.__new - self.__old


# +: самый экономный по памяти
# -: работает только с числами
# -: медленее чем CycledFIFOBufferList, хотя по идее должен быть быстрее
class CycledFIFOBufferArray:
    def __init__(self, max_size, typecode):
        self.__data = array.array(typecode)
        self.max_size = max_size

    def push(self, item):
        self.__data.append(item)
        if len(self.__data) > self.max_size:
            self.__data.pop(0)

    def pop(self):
        if len(self.__data) == 0:
            raise BufferError("pop from empty buffer")
        return self.__data.pop(0)

    def clear(self):
        self.__data = []

    def size(self):
        return len(self.__data)


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


# -: медленный
class CycledFIFOBufferNodes:
    def __init__(self, max_size):
        self.max_size = max_size
        self.__start = None
        self.__end = None
        self.__size = 0

    def push(self, item):
        node = Node(item)
        if self.__start is None:
            self.__start = node
            self.__end = node
        else:
            self.__end.next = node
            self.__end = node
        self.__size += 1
        if self.__size > self.max_size:
            self.pop()

    def pop(self):
        if self.__size == 0:
            raise BufferError("pop from empty buffer")
        value = self.__start.value
        self.__start = self.__start.next
        self.__size -= 1
        return value

    def clear(self):
        for _ in range(self.__size):
            self.pop()
        self.__size = 0

    def size(self):
        return self.__size


# -: самый медленный
class CycledFIFOBufferQueue(queue.Queue):
    def __init__(self, max_size):
        super().__init__(max_size)

    def push(self, item):
        if self.qsize() == self.maxsize:
            self.get()
        self.put(item)

    def pop(self):
        if self.qsize() == 0:
            raise BufferError("pop from empty buffer")
        return self.get()

    def clear(self):
        for _ in range(self.qsize()):
            self.get()

    def size(self):
        return self.qsize()


# +: самый быстрый способ из найденных
class CycledFIFOBufferDequeue(collections.deque):
    def __init__(self, max_size):
        super().__init__(maxlen=max_size)

    def push(self, item):
        self.append(item)

    def pop(self):
        return self.popleft()

    def clear(self):
        super().clear()

    def size(self):
        return len(self)


class CycledFIFOBufferDict:
    def __init__(self, max_size):
        self.__data = {}
        self.max_size = max_size
        self.__counter = 0

    def push(self, item):
        self.__counter += 1
        self.__data[self.__counter] = item
        if len(self.__data) > self.max_size:
            self.pop()

    def pop(self):
        if len(self.__data) == 0:
            raise BufferError("pop from empty buffer")
        return self.__data.pop(self.__counter - len(self.__data) + 1)

    def clear(self):
        self.__data.clear()
        self.__counter = 0

    def size(self):
        return len(self.__data)
