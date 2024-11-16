import sys
import re


class Deque:
    def __init__(self, size):
        if size >= 0:
            self.n = size
        else:
            self.n = 0
            print('error')
        self.deque = [None] * self.n
        self.front = 0
        self.back = 0
        self.size = 0

    def print_deque(self):
        if self.size == 0:
            print('empty')
        else:
            ind = self.front
            data = []
            for i in range(self.size):
                data.append(self.deque[ind])
                ind = (ind + 1) % self.n
            print(' '.join(map(str, data)))

    def push_back(self, to_add):
        if self.size == self.n:
            print('overflow')
        else:
            self.deque[self.back] = to_add
            self.back = (self.back + 1) % self.n
            self.size += 1

    def push_front(self, to_add):
        if self.size == self.n:
            print('overflow')
        else:
            self.front = (self.front - 1) % self.n
            self.deque[self.front] = to_add
            self.size += 1

    def pop_back(self):
        if self.size == 0:
            print('underflow')
        else:
            value = self.deque[self.back - 1]
            self.back = (self.back - 1) % self.n
            self.size -= 1
            print(value)

    def pop_front(self):
        if self.size == 0:
            print('underflow')
        else:
            value = self.deque[self.front]
            self.front = (self.front + 1) % self.n
            self.size -= 1
            print(value)


def main():
    deq = None
    allocated = False
    for command in sys.stdin.read().splitlines():
        if not command.strip():
            continue

        content = re.findall(r'\S+|\s+', command)

        if content[0] == 'set_size' and not allocated and int(content[2]) >= 0:
            try:
                size = int(content[2])
                deq = Deque(size)
                allocated = True
            except ValueError:
                print('error')

        elif not allocated:
            print("error")
            continue

        elif len(content) == 1:
            head = content[0]
            if head == 'print':
                deq.print_deque()
            elif head == 'popb':
                deq.pop_back()
            elif head == 'popf':
                deq.pop_front()
            else:
                print('error')
        elif len(content) == 3 and content[1] == ' ':
            head = None
            value = None
            try:
                head, value = content[0], content[2]
            except ValueError:
                print('error')
            if head == 'pushb':
                deq.push_back(value)
            elif head == 'pushf':
                deq.push_front(value)
            else:
                print('error')
        else:
            print('error')


if __name__ == '__main__':
    main()
