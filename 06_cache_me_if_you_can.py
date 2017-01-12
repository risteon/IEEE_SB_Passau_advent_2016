#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod
from collections import deque
from operator import itemgetter

__author__ = "Christoph Rist"
__license__ = "MIT"


class Cache(metaclass=ABCMeta):
    def __init__(self, size):
        self._size = size
        self.hits = 0
        self.misses = 0
        self._deque = deque([], size)

    def shift_to_right(self, index):
        tmp = self._deque[index]
        for i in range(index, len(self._deque)-1):
            self._deque[i] = self._deque[i+1]
        self._deque[len(self._deque)-1] = tmp

    @abstractmethod
    def push(self, key, value):
        raise NotImplementedError

    @abstractmethod
    def get(self, key):
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError


class FiFo(Cache):
    def __init__(self, size):
        Cache.__init__(self, size)

    def push(self, key, value):
        self._deque.append((key, value))

    def get(self, key):
        l = [v for k, v in self._deque if k == key]
        if not l:
            self.misses += 1
            return "miss"
        self.hits += 1
        return l[0]

    @property
    def name(self):
        return "FIFO"


class LRU(Cache):
    def __init__(self, size):
        Cache.__init__(self, size)

    def push(self, key, value):
        if len(self._deque) == self._size:
            self._deque.popleft()
        self._deque.appendleft((key, value))

    def get(self, key):
        l = [(i, v) for i, (k, v) in enumerate(self._deque) if k == key]
        if not l:
            self.misses += 1
            return "miss"

        self.shift_to_right(l[0][0])
        self.hits += 1
        return l[0][1]

    @property
    def name(self):
        return "LRU"


class MRU(Cache):
    def __init__(self, size):
        Cache.__init__(self, size)

    def push(self, key, value):
        self._deque.appendleft((key, value))

    def get(self, key):
        l = [(i, v) for i, (k, v) in enumerate(self._deque) if k == key]
        if not l:
            self.misses += 1
            return "miss"
        i, v = l[0]
        self.shift_to_right(i)
        self.hits += 1
        return v

    @property
    def name(self):
        return "MRU"


class LFU(Cache):
    def __init__(self, size):
        Cache.__init__(self, size)
        self._use_count = {}

    def push(self, key, value):
        if len(self._deque) == self._size:
            # search for oldest min use count
            l = [(self._use_count[k], k, v) for k, v in self._deque]
            min_uc = min(l, key=itemgetter(0))[0]
            for uc, k, v in l:
                if uc == min_uc:
                    self._deque.remove((k, v))
                    del self._use_count[k]
                    break;

        self._deque.append((key, value))
        self._use_count[key] = 0

    def get(self, key):
        l = [(k, v) for k, v in self._deque if k == key]
        if not l:
            self.misses += 1
            return "miss"
        k, v = l[0]
        self.hits += 1
        self._use_count[k] += 1
        return v

    @property
    def name(self):
        return "LFU"


def cache_factory(cache_key, size):
    if cache_key == 0:
        return FiFo(size)
    elif cache_key == 1:
        return LRU(size)
    elif cache_key == 2:
        return MRU(size)
    elif cache_key == 3:
        return LFU(size)
    raise RuntimeError("Unknown cache type.")


def main():
    nb_test_cases = int(input())
    for n in range(nb_test_cases):
        size, nb_caches, nb_ops = map(int, input().split())
        caches = [cache_factory(int(x), size) for x in input().split()]

        for o in range(nb_ops):
            operation = list(map(int, input().split()))
            if operation[0] == 0:
                # PUSH
                if len(operation) != 3:
                    raise RuntimeError("Invalid input")
                # call push on every cache
                for c in caches:
                    c.push(operation[1], operation[2])

            elif operation[0] == 1:
                # GET
                if len(operation) != 2:
                    raise RuntimeError("Invalid input")
                # call get on every cache
                outputs = [c.get(operation[1]) for c in caches]
                print(*outputs, sep='\n')

            else:
                raise RuntimeError("Invalid input")

        # print cache with max hits
        cache = max(caches, key=lambda c: c.hits)
        print("{}: H:{} M:{}".format(cache.name, cache.hits, cache.misses))


if __name__ == "__main__":
    main()
