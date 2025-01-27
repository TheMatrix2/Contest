# Copyright Boris Ermolovich ermolovich.boris@gmail.com
# обход графа
import sys
from collections import defaultdict, deque


def dfs(graph, start):
    visited = set()
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            stack.extend(sorted(graph[vertex], reverse=True))


def bfs(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            queue.extend(sorted(graph[vertex]))


def main():
    lines = sys.stdin.read().strip().splitlines()
    graph_type, start_vertex, search_type = lines[0].strip().split()
    graph = defaultdict(list)

    for edge in lines[1:]:
        u, v = edge.split()
        graph[u].append(v)
        if graph_type == 'u':
            graph[v].append(u)

    if search_type == 'd':
        dfs(graph, start_vertex)
    elif search_type == 'b':
        bfs(graph, start_vertex)


if __name__ == "__main__":
    main()
