# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# блокировка логина
import sys


def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr



class LoginBlocker:
    def __init__(self, attempts_number: int, period: int, block_time: int, max_block_time: int, current_time: int):
        self.attempts_number = attempts_number
        self.period = period
        self.block_time = block_time
        self.max_block_time = max_block_time
        self.current_time = current_time

    def block_status(self, attempts: [int]) -> (bool, int):
        attempts = [attempt for attempt in heap_sort(attempts) if attempt >= self.current_time - 2 * self.max_block_time]
        '''
            Пирамидальная сортировка имеет сложность O(n*log(n)) по времени и O(1) по памяти
        '''

        block_time = self.block_time
        block_end = 0
        was_blocked = False
        attempt_index = 0

        while attempt_index <= len(attempts) - self.attempts_number:
            if attempts[attempt_index + self.attempts_number - 1] - attempts[attempt_index] >= self.period:
                attempt_index += 1
                continue
            if was_blocked:
                block_time = min(block_time * 2, self.max_block_time)
            else:
                was_blocked = True
            attempt_index += self.attempts_number
            block_end = attempts[attempt_index - 1] + block_time
            '''
                Прохождение по всему списку: O(n) по времени и O(1) по памяти
            '''
        if block_end > self.current_time:
            return True, block_end
        return False, None
'''
    В результате получаем оценки
    По времени: O(n*log(n) + n) = O(n*log(n))
    По памяти: O(1 + 1) = O(1)
'''


def main():
    input_data = []
    for line in sys.stdin:
        if line.strip():
            input_data.append(line.replace('\n', ''))
        else:
            break
    n, p, b, b_max, curr_t = (int(x) for x in input_data[0].split())
    blocker = LoginBlocker(n, p, b, b_max, curr_t)
    all_attempts = list(map(int, input_data[1:]))
    status, time = blocker.block_status(all_attempts)
    print(time if status else 'ok')


if __name__ == '__main__':
    main()
    sys.exit(0)