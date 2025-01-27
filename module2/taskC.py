# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# двоичная min-куча
import sys
import re


class MinHeap:

    def __init__(self):
        self.heap_list = [] # [(key1: value1), (key2: value2), ...]
        self.index_map = {} # {key1: index1, key2: index2, ...}

    def _swap(self, i, j):
        self.index_map[self.heap_list[i][0]], self.index_map[self.heap_list[j][0]] = j, i
        self.heap_list[i], self.heap_list[j] = self.heap_list[j], self.heap_list[i]

    def _sift_down(self, index):
        while 2 * index + 1 < len(self.heap_list):
            left = 2 * index + 1
            right = 2 * index + 2
            j = left
            if right < len(self.heap_list) and self.heap_list[right][0] < self.heap_list[left][0]:
                j = right
            if self.heap_list[index][0] >= self.heap_list[j][0]:
                self._swap(index, j)
            index = j

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap_list[index][0] < self.heap_list[parent][0]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def add(self, key, value):
        if key in self.index_map:
            raise ValueError
        self.heap_list.append((key, value))
        self.index_map[key] = len(self.heap_list) - 1
        self._sift_up(len(self.heap_list) - 1)

    def set(self, key, value):
        if key not in self.index_map:
            raise ValueError
        index = self.index_map[key]
        self.heap_list[index] = (key, value)

    def search(self, key):
        if key not in self.index_map:
            return None
        index = self.index_map[key]
        return index, self.heap_list[index][1]

    def min(self):
        if not self.heap_list:
            raise ValueError()
        min_key, min_value = self.heap_list[0]
        return min_key, 0, min_value

    def max(self): # поиск среди листьев
        if not self.heap_list:
            raise ValueError()
        first_leaf_index = len(self.heap_list) // 2
        max_key, max_index, max_value = max(
            ((k, i, v) for i, (k, v) in enumerate(self.heap_list[first_leaf_index:], start=first_leaf_index)),
            key=lambda x: x[0])
        return max_key, max_index, max_value

    def delete(self, key):
        if not self.heap_list or key not in self.index_map:
            raise ValueError()
        index = self.index_map[key]
        self._swap(index, len(self.heap_list) - 1)
        self.heap_list.pop()
        del self.index_map[key]
        if index == len(self.heap_list):
            return
        if (index - 1) // 2 >= 0 and self.heap_list[index][0] < self.heap_list[(index - 1) // 2][0]:
            self._sift_up(index)
            return
        self._sift_down(index)


    def extract_min(self):
        if not self.heap_list:
            raise ValueError()
        min_key, min_value = self.heap_list[0]
        self.delete(min_key)
        return min_key, min_value

    # output_handler функция, принимающая на вход строку и реализующая ее вывод (по умолчанию в консоль)
    def output_heap(self, output_handler=print):
        if not self.heap_list:
            output_handler("_")
            return

        output_handler(f'[{self.heap_list[0][0]} {self.heap_list[0][1]}]')

        current_level, level_size = 1, 2
        while level_size <= len(self.heap_list):
            items = self.heap_list[current_level:current_level + level_size]
            if len(items) == level_size:
                output_handler(' '.join(f'[{key} {value} {self.heap_list[(current_level + j - 1) // 2][0]}]'
                               for j, (key, value) in enumerate(items)))
            else:
                output_handler(' '.join(f'[{key} {value} {self.heap_list[(current_level + j - 1) // 2][0]}]'
                               for j, (key, value) in enumerate(items)) + ' ' +  ' '.join(['_'] * (level_size - len(items))))
            current_level += level_size
            level_size *= 2

def main():
    heap = MinHeap()

    for line in sys.stdin:
        if not line.strip():
            continue
        add_match = re.match(r"^add\s+(-?\d+)\s+(.*)$", line)
        set_match = re.match(r"^set\s+(-?\d+)\s+(.*)$", line)
        search_match = re.match(r"^search\s+(-?\d+)$", line)
        min_match = re.match(r"^min$", line)
        max_match = re.match(r"^max$", line)
        delete_match = re.match(r"^delete\s+(-?\d+)$", line)
        extract_min_match = re.match(r"^extract$", line)
        print_match = re.match(r"^print$", line)

        try:
            if add_match:
                key = int(add_match.group(1))
                value = add_match.group(2)
                heap.add(key, value)
            elif set_match:
                key = int(set_match.group(1))
                value = set_match.group(2)
                heap.set(key, value)
            elif search_match:
                key = int(search_match.group(1))
                result = heap.search(key)
                if result:
                    print(f"1 {result[0]} {result[1]}")
                else:
                    print("0")
            elif min_match:
                result = heap.min()
                print(f"{result[0]} {result[1]} {result[2]}")
            elif max_match:
                result = heap.max()
                print(f"{result[0]} {result[1]} {result[2]}")
            elif delete_match:
                key = int(delete_match.group(1))
                heap.delete(key)
            elif extract_min_match:
                result = heap.extract_min()
                print(f"{result[0]} {result[1]}")
            elif print_match:
                heap.output_heap()
            else:
                print("error")
        except ValueError:
            print("error")

if __name__ == "__main__":
    main()
