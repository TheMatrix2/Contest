# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# косое дерево
import sys
import re

class Node:
    def __init__(self, key, value, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def has_both_children(self):
        return self.left is not None and self.right is not None

    def has_left_child(self):
        return self.left is not None

    def has_right_child(self):
        return self.right is not None

    def is_left_child(self):
        return self.parent and self.parent.left == self

    def is_right_child(self):
        return self.parent and self.parent.right == self

    def clear(self):
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate_left(self, node):
        right_child = node.right
        if right_child:
            node.right = right_child.left
            if right_child.left:
                right_child.left.parent = node
            right_child.parent = node.parent
            if not node.parent:
                self.root = right_child
            elif node.is_left_child():
                node.parent.left = right_child
            else:
                node.parent.right = right_child
            right_child.left = node
            node.parent = right_child

    def _rotate_right(self, node):
        left_child = node.left
        if left_child:
            node.left = left_child.right
            if left_child.right:
                left_child.right.parent = node
            left_child.parent = node.parent
            if not node.parent:
                self.root = left_child
            elif node.is_left_child():
                node.parent.left = left_child
            else:
                node.parent.right = left_child
            left_child.right = node
            node.parent = left_child

    def _splay(self, node):
        while node and node.parent:
            if not node.parent.parent:
                if node.is_left_child():
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node.is_left_child() and node.parent.is_left_child():
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node.is_right_child() and node.parent.is_right_child():
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            elif node.is_left_child() and node.parent.is_right_child():
                self._rotate_right(node.parent)
                self._rotate_left(node.parent)
            elif node.is_right_child() and node.parent.is_left_child():
                self._rotate_left(node.parent)
                self._rotate_right(node.parent)

    def _put(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return

        current_node = self.root
        parent = None
        while current_node:
            parent = current_node

            if key < current_node.key:
                current_node = current_node.left
            elif key > current_node.key:
                current_node = current_node.right
            else:
                current_node.value = value
                self._splay(current_node)
                return

        new_node = Node(key, value, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def _find(self, key): # возвращает найденный узел (или None) и последний посещенный узел
        current_node = self.root
        last_visited = None

        while current_node:
            last_visited = current_node
            if key < current_node.key:
                current_node = current_node.left
            elif key > current_node.key:
                current_node = current_node.right
            else:
                return current_node, last_visited
        return None, last_visited

    @staticmethod
    def _min(current_node=None):
        while current_node and current_node.has_left_child():
            current_node = current_node.left
        return current_node

    @staticmethod
    def _max(current_node=None):
        while current_node and current_node.has_right_child():
            current_node = current_node.right
        return current_node

    def add(self, key, value):
        node = self._find(key)[0]
        if node:
            self._splay(node)
            raise ValueError("error")
        self._put(key, value)

    def set(self, key, value):
        node, last_visited = self._find(key)
        if not node:
            self._splay(last_visited)
            raise ValueError("error")
        node.value = value
        self._splay(node)

    def search(self, key):
        if not self.root:
            return None
        node, last_visited = self._find(key)
        if not node:
            self._splay(last_visited)
            return node
        self._splay(node)
        return node

    def find_min(self):
        if not self.root:
            raise ValueError("error")
        min_node = self._min(self.root)
        self._splay(min_node)
        return min_node

    def find_max(self):
        if not self.root:
            raise ValueError("error")
        max_node = self._max(self.root)
        self._splay(max_node)
        return max_node

    def delete(self, key):
        node, last_visited = self._find(key)
        if not node:
            self._splay(last_visited)
            raise ValueError("error")
        self._splay(node)
        if node.has_both_children():
            left_subtree = node.left
            right_subtree = node.right
            left_subtree.parent = None
            right_subtree.parent = None
            max_left = self._max(left_subtree)
            self._splay(max_left)
            max_left.right = right_subtree
            right_subtree.parent = max_left
            self.root = max_left
        elif node.has_left_child():
            self.root = node.left
            self.root.parent = None
        elif node.has_right_child():
            self.root = node.right
            self.root.parent = None
        else:
            self.root = None
        node.clear()

    # сторонний разработчик должен реализовать функцию output_handler, если необходимо выводить дерево не в консоль
    def output(self, output_handler=None):
        if not output_handler:
            console_output(self)
        else:
            output_handler(self)


def console_output(tree):
    if not tree.root:
        print("_")
        return

    print(f"[{tree.root.key} {tree.root.value}]")

    if not tree.root.has_left_child() and not tree.root.has_right_child():
        return

    current_len = 2
    current_layer = {}
    next_layer = {}
    stop = False

    if tree.root.left:
        current_layer[0] = tree.root.left
    if tree.root.right:
        current_layer[1] = tree.root.right

    while not stop:
        stop = True
        print_value = ""
        keys = sorted(current_layer.keys())
        previous_key = 0

        for key in keys:
            node = current_layer.pop(key)

            print_value += "_ " * (key - previous_key)

            if node.left:
                stop = False
                next_layer[key * 2] = node.left
            if node.right:
                stop = False
                next_layer[key * 2 + 1] = node.right

            parent_key = node.parent.key if node.parent else ''
            print_value += f"[{node.key} {node.value} {parent_key}] "
            previous_key = key + 1

        print_value += "_ " * (current_len - previous_key)
        print(print_value.strip())

        current_layer = next_layer
        next_layer = {}
        current_len *= 2


def main():
    tree = SplayTree()

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
                tree.add(key, value)
            elif set_match:
                key = int(set_match.group(1))
                value = set_match.group(2)
                tree.set(key, value)
            elif search_match:
                key = int(search_match.group(1))
                node = tree.search(key)
                if node:
                    print(f"1 {node.value}")
                else:
                    print("0")
            elif find_min_match:
                node = tree.find_min()
                print(f"{node.key} {node.value}")
            elif find_max_match:
                node = tree.find_max()
                print(f"{node.key} {node.value}")
            elif delete_match:
                key = int(delete_match.group(1))
                tree.delete(key)
            elif print_match:
                tree.output()
            else:
                print("error")
        except ValueError:
            print("error")


if __name__ == "__main__":
    main()