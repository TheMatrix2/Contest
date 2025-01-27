# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# двоичное дерево поиска
import sys
import re


class Node:
    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def has_both_children(self):
        return self.left and self.right

    def has_any_children(self):
        return self.left or self.right

    def has_left_child(self):
        return self.left is not None

    def has_right_child(self):
        return self.right is not None


class BST: # Binary Search Tree
    def __init__(self):
        self.root = None

    def search(self, key, current_node=None):
        if self.root is None:
            return None
        else:
            if current_node is None:
                current_node = self.root
            if key < current_node.key:
                return self.search(key, current_node.left) if current_node.has_left_child() else None
            elif key > current_node.key:
                return self.search(key, current_node.right) if current_node.has_right_child() else None
            else:
                return current_node

    def _put(self, key, value, current_node=None):
        if self.root is None:
            self.root = Node(key, value)
        else:
            if current_node is None:
                current_node = self.root

            if key < current_node.key:
                if current_node.has_left_child():
                    self._put(key, value, current_node.left)
                else:
                    current_node.left = Node(key, value, parent=current_node)
            elif key > current_node.key:
                if current_node.has_right_child():
                    self._put(key, value, current_node.right)
                else:
                    current_node.right = Node(key, value, parent=current_node)
            else:
                current_node.value = value

    def add(self, key, value):
        if self.search(key) is not None:
            raise ValueError()
        else:
            self._put(key, value)


    def set(self, key, value):
        if self.search(key) is not None:
            self._put(key, value)
        else:
            raise ValueError()

    def find_min(self, current_node=None):
        if self.root is None:
            raise ValueError()
        else:
            current_node = self.root if current_node is None else current_node
            while current_node.has_left_child():
                current_node = current_node.left
            return current_node

    def find_max(self, current_node=None):
        if self.root is None:
            raise ValueError()
        else:
            current_node = self.root if current_node is None else current_node
            while current_node.has_right_child():
                current_node = current_node.right
            return current_node

    def _remove(self, key, current_node):
        if key < current_node.key:
            current_node.left = self._remove(key, current_node.left)
        elif key > current_node.key:
            current_node.right = self._remove(key, current_node.right)
        else:
            if not current_node.has_any_children():
                if current_node == self.root:
                    self.root = None
                return None
            elif not current_node.has_both_children():
                if current_node.has_left_child():
                    temp = current_node.left
                else:
                    temp = current_node.right
                temp.parent = current_node.parent
                if current_node == self.root:
                    self.root = temp
                return temp
            else:
                max_in_left = self.find_max(current_node.left)
                current_node.key = max_in_left.key
                current_node.value = max_in_left.value
                current_node.left = self._remove(max_in_left.key, current_node.left)

        return current_node

    def delete(self, key):
        if not self.root:
            raise ValueError('error')
        if self.search(key) is not None:
            self._remove(key, self.root)
        else:
            raise ValueError('error')

    # output_handler функция, принимающая на вход строку и реализующая ее вывод (по умолчанию в консоль)
    def output_tree(self, output_handler=print):
        if self.root is None:
            output_handler("_")
            return

        current_level = [self.root]
        while current_level:
            next_level = []
            result_line = []
            for node in current_level:
                if node is None:
                    result_line.append("_")
                    next_level.append(None)
                    next_level.append(None)
                else:
                    parent_key = node.parent.key if node.parent is not None else None
                    result_line.append(f"[{node.key} {node.value} {parent_key}]" if parent_key is not None else
                                       f"[{node.key} {node.value}]")
                    next_level.append(node.left)
                    next_level.append(node.right)

            if any(n is not None for n in current_level):
                output_handler(" ".join(result_line))
            else:
                return
            current_level = next_level


def main():
    binary_tree = BST()

    for line in sys.stdin:
        add_match = re.match(r"^add\s+(-?\d+)\s+(.*)$", line)
        set_match = re.match(r"^set\s+(-?\d+)\s+(.*)$", line)
        search_match = re.match(r"^search\s+(-?\d+)$", line)
        find_min_match = re.match(r"^min$", line)
        find_max_match = re.match(r"^max$", line)
        delete_match = re.match(r"^delete\s+(-?\d+)$", line)
        print_match = re.match(r"^print$", line)

        try:
            if add_match:
                key = int(add_match.group(1))
                value = add_match.group(2)
                binary_tree.add(key, value)
            elif set_match:
                key = int(set_match.group(1))
                value = set_match.group(2)
                binary_tree.set(key, value)
            elif search_match:
                key = int(search_match.group(1))
                node = binary_tree.search(key)
                if node:
                    print(f"1 {node.value}")
                else:
                    print("0")
            elif find_min_match:
                node = binary_tree.find_min()
                print(f"{node.key} {node.value}")
            elif find_max_match:
                node = binary_tree.find_max()
                print(f"{node.key} {node.value}")
            elif delete_match:
                key = int(delete_match.group(1))
                binary_tree.delete(key)
            elif print_match:
                binary_tree.output_tree()
            else:
                print("error")
        except ValueError:
            print("error")


if __name__ == "__main__":
    main()
