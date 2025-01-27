# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# приближенный рюкзак
import sys
from queue import PriorityQueue

class Item:
    def __init__(self, num: int, weight: int, cost: int):
        self.num = num
        self.weight = weight
        self.cost = cost


class Solution:
    def __init__(self, total_weight: int, total_cost: int, indexes: [int]):
        self.total_weight = total_weight
        self.total_cost = total_cost
        self.indexes = indexes

    def output(self, output_handler=None):
        if not output_handler:
            solution_to_console(self)
        else:
            output_handler(self)


def solution_to_console(solution: Solution):
    print(solution.total_weight, solution.total_cost)
    for index in sorted(solution.indexes):
        print(index)


class KnapsackProblem:

    def __init__(self, items: [Item], capacity: int, precision: float):
        self.items = items
        self.capacity = capacity
        self.precision = precision

    # узел для метода ветвей и границ
    class Node:
        def __init__(self, level, value, weight, bound, selection):
            self.level = level
            self.value = value
            self.weight = weight
            self.bound = bound
            self.selection = selection

        def __lt__(self, other):
            return self.bound > other.bound

    # расчет предельного значения
    def bound(self, node, sorted_items):
        if node.weight > self.capacity:
            return 0
        result = node.value
        total_weight = node.weight
        for i in range(node.level + 1, len(sorted_items)):
            item = sorted_items[i]
            if total_weight + item.weight <= self.capacity:
                total_weight += item.weight
                result += item.cost_scaled
            else:
                result += (self.capacity - total_weight) * item.cost_scaled / item.weight
                break
        return result

    # масштабирование + метод ветвей и границ
    def approximate_solution(self) -> Solution:
        max_cost = max(item.cost for item in self.items)
        scale = self.precision * max_cost / (len(self.items) * (1 + self.precision))

        for item in self.items:
            item.cost_scaled = int(item.cost // scale)

        sorted_items = sorted(self.items, key=lambda x: x.cost_scaled / x.weight if x.weight > 0 else float('inf'),
                              reverse=True)

        queue = PriorityQueue()
        root = self.Node(-1, 0, 0, 0, [])
        root.bound = self.bound(root, sorted_items)
        queue.put(root)

        max_value = 0
        best_selection = []

        while not queue.empty():
            node = queue.get()

            if node.bound <= max_value:
                continue

            if node.level + 1 < len(sorted_items):
                next_item = sorted_items[node.level + 1]

                node_with_item = self.Node(
                    level=node.level + 1,
                    value=node.value + next_item.cost_scaled,
                    weight=node.weight + next_item.weight,
                    bound=0,
                    selection=node.selection + [1]
                )
                if node_with_item.weight <= self.capacity:
                    if node_with_item.value > max_value:
                        max_value = node_with_item.value
                        best_selection = node_with_item.selection
                    node_with_item.bound = self.bound(node_with_item, sorted_items)
                    if node_with_item.bound > max_value:
                        queue.put(node_with_item)

                node_without_item = self.Node(
                    level=node.level + 1,
                    value=node.value,
                    weight=node.weight,
                    bound=0,
                    selection=node.selection + [0]
                )
                node_without_item.bound = self.bound(node_without_item, sorted_items)
                if node_without_item.bound > max_value:
                    queue.put(node_without_item)

        selected_indices = [
            self.items.index(sorted_items[i]) + 1 for i in range(len(best_selection))
            if best_selection[i] == 1
        ]
        total_weight = sum(self.items[i - 1].weight for i in selected_indices)
        total_cost = sum(self.items[i - 1].cost for i in selected_indices)

        return Solution(total_weight=total_weight, total_cost=total_cost, indexes=selected_indices)



def main():
    approximation_coefficient = float(sys.stdin.readline())
    sys.stdin.flush()
    max_weight = int(sys.stdin.readline())
    sys.stdin.flush()
    items = []
    i = 1
    for line in sys.stdin.read().splitlines():
        items.append(Item(i, int(line.split()[0]), int(line.split()[1])))
        i += 1
    knapsack = KnapsackProblem(items, max_weight, approximation_coefficient)
    solution = knapsack.approximate_solution()
    solution.output()


if __name__ == '__main__':
    main()