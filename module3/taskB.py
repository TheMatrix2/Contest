# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# фильтр Блума
import math
import sys
import re


class BitArray:
    def __init__(self, size: int):
        self.size = size
        self.array = bytearray(math.ceil(size / 8))

    def set(self, index: int):
        if 0 <= index < self.size:
            self.array[index // 8] |= 1 << (index % 8)
        else:
            raise Exception

    def get(self, index: int) -> bool:
        if 0 <= index < self.size:
            return self.array[index // 8] & (1 << (index % 8)) != 0
        else:
            raise Exception


def console_output(array: bytearray, size: int):
    print(''.join(f'{(array[i // 8] >> (i % 8)) & 1}' for i in range(size)))


class BloomFilter:
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    M = (1 << 31) - 1
    _is_initialized = False

    def __init__(self, number: int, probability: float):
        if BloomFilter._is_initialized:
            raise Exception
        if number <= 0 or not 0 <= probability <= 1:
            raise Exception
        self.number = number
        self.probability = probability
        self.m = int(round(-number * math.log2(probability) / math.log(2)))
        self.k = int(round(-math.log2(probability)))
        self.bit_array = BitArray(self.m)
        if self.m < 1 or self.k < 1:
            raise Exception
        BloomFilter._is_initialized = True

    @staticmethod
    def __is_prime(number: int) -> bool:
        if number < 2:
            return True
        sqrt_number = math.ceil(math.sqrt(number))
        for prime in BloomFilter.PRIMES:
            if prime > sqrt_number:
                break
            if number % prime == 0:
                return False
        return True

    @staticmethod
    def __add_primes(quantity: int):
        length_before = len(BloomFilter.PRIMES)
        number = BloomFilter.PRIMES[-1]
        while len(BloomFilter.PRIMES) < length_before + quantity:
            number += 2
            if BloomFilter.__is_prime(number):
                BloomFilter.PRIMES.append(number)

    def __hash(self, x: int, i: int) -> int:
        if i > len(BloomFilter.PRIMES) - 1:
            BloomFilter.__add_primes(i - len(BloomFilter.PRIMES) + 1)
        return (((i + 1) * x + BloomFilter.PRIMES[i]) % BloomFilter.M) % self.m

    def add(self, key: int):
        if self.k > len(BloomFilter.PRIMES) - 1:
            BloomFilter.__add_primes(self.k - len(BloomFilter.PRIMES) + 1)
        for i in range(self.k):
            index = self.__hash(key, i)
            self.bit_array.set(index)

    def search(self, key: int) -> bool:
        for i in range(self.k):
            index = self.__hash(key, i)
            if not self.bit_array.get(index):
                return False
        return True

    def output(self, output_handler=None):
        if not output_handler:
            console_output(self.bit_array.array, self.m)
        else:
            output_handler(self.bit_array.array, self.m)


def main():
    bloom_filter = None
    input_data = sys.stdin.read().splitlines()
    for idx, line in enumerate(input_data):
        if not line.strip():
            continue
        set_match = re.match(r'^set\s+(\d+)\s+(0(\.\d+)?|1(\.0*)?)$', line)
        add_match = re.match(r'^add\s+(\d+)$', line)
        search_match = re.match(r'^search\s+(\d+)$', line)
        print_match = re.match(r'^print$', line)

        try:
            if set_match:
                bloom_filter = BloomFilter(int(set_match.group(1)), float(set_match.group(2)))
                print(bloom_filter.m, bloom_filter.k)
            elif add_match:
                bloom_filter.add(int(add_match.group(1)))
            elif search_match:
                print('1' if bloom_filter.search(int(search_match.group(1))) else '0')
            elif print_match:
                bloom_filter.output()
            else:
                raise Exception
        except Exception:
            print('error')
    return bloom_filter


if __name__ == '__main__':
    main()
