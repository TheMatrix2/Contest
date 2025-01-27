# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# двоичный поиск
import sys


def binary_search(array, start_index, end_index, target):
    if end_index >= start_index:
        mid_index = int(end_index - start_index // 2)
        if array[mid_index] == target:
            if mid_index == start_index or array[mid_index - 1] < target:
                return mid_index
            else:
                return binary_search(array, start_index, mid_index - 1, target)
        elif target > array[mid_index]:
            return binary_search(array, mid_index + 1, end_index, target)
        elif target < array[mid_index]:
            return binary_search(array, start_index, mid_index - 1, target)
    else:
        return -1


def main():
    std_input = sys.stdin.read().strip().splitlines()
    array = []
    if 'search' in std_input[0].split():
        for i in range(len(std_input) - 1):
            print(-1)
    else:
        array = [int(x) for x in std_input[0].split()]
    for line in std_input[1:]:
        number = int(line.split()[1])
        print(binary_search(array, 0, len(array) - 1, number))


if __name__ == '__main__':
    main()
