// Copyright Boris Ermolovich ermolovich.boris@gmail.com
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cmath>
#include <limits>

using namespace std;

struct Item {
    int num;
    int weight;
    int cost;

    Item(int n, int w, int c) : num(n), weight(w), cost(c) {}
};

struct Solution {
    int total_weight;
    int total_cost;
    vector<int> indexes;

    Solution(int tw, int tc, const vector<int>& idx) : total_weight(tw), total_cost(tc), indexes(idx) {}

    void output() const {
        cout << total_weight << " " << total_cost << endl;
        for (int index : indexes) {
            cout << index << endl;
        }
    }
};

class KnapsackProblem {
    struct Node {
        int level;
        int value;
        int weight;
        double bound;
        vector<int> selection;

        Node(int l, int v, int w, double b, const vector<int>& sel)
            : level(l), value(v), weight(w), bound(b), selection(sel) {}

        bool operator<(const Node& other) const {
            return bound < other.bound;
        }
    };

    vector<Item> items;
    int capacity;
    double precision;

public:
    KnapsackProblem(const vector<Item>& items, int capacity, double precision)
        : items(items), capacity(capacity), precision(precision) {}

    double bound(const Node& node, const vector<Item>& sorted_items) {
        if (node.weight > capacity) {
            return 0;
        }

        double result = node.value;
        int total_weight = node.weight;

        for (size_t i = node.level + 1; i < sorted_items.size(); ++i) {
            const Item& item = sorted_items[i];
            if (total_weight + item.weight <= capacity) {
                total_weight += item.weight;
                result += item.cost;
            } else {
                result += (capacity - total_weight) * (double)item.cost / item.weight;
                break;
            }
        }

        return result;
    }

    Solution approximate_solution() {
        int max_cost = 0;
        for (const auto& item : items) {
            max_cost = max(max_cost, item.cost);
        }

        double scale = precision * max_cost / (items.size() * (1 + precision));

        vector<Item> scaled_items;
        for (const auto& item : items) {
            scaled_items.emplace_back(item.num, item.weight, (int)(item.cost / scale));
        }

        sort(scaled_items.begin(), scaled_items.end(), [](const Item& a, const Item& b) {
            return (double)a.cost / a.weight > (double)b.cost / b.weight;
        });

        priority_queue<Node> queue;
        Node root(-1, 0, 0, 0.0, {});
        root.bound = bound(root, scaled_items);
        queue.push(root);

        int max_value = 0;
        vector<int> best_selection;

        while (!queue.empty()) {
            Node node = queue.top();
            queue.pop();

            if (node.bound <= max_value) {
                continue;
            }

            if (node.level + 1 < (int)scaled_items.size()) {
                const Item& next_item = scaled_items[node.level + 1];

                Node node_with_item(
                    node.level + 1,
                    node.value + next_item.cost,
                    node.weight + next_item.weight,
                    0.0,
                    node.selection
                );
                node_with_item.selection.push_back(1);

                if (node_with_item.weight <= capacity) {
                    if (node_with_item.value > max_value) {
                        max_value = node_with_item.value;
                        best_selection = node_with_item.selection;
                    }
                    node_with_item.bound = bound(node_with_item, scaled_items);
                    if (node_with_item.bound > max_value) {
                        queue.push(node_with_item);
                    }
                }

                Node node_without_item(
                    node.level + 1,
                    node.value,
                    node.weight,
                    0.0,
                    node.selection
                );
                node_without_item.selection.push_back(0);

                node_without_item.bound = bound(node_without_item, scaled_items);
                if (node_without_item.bound > max_value) {
                    queue.push(node_without_item);
                }
            }
        }

        vector<int> selected_indices;
        for (size_t i = 0; i < best_selection.size(); ++i) {
            if (best_selection[i] == 1) {
                selected_indices.push_back(scaled_items[i].num);
            }
        }

        int total_weight = 0;
        int total_cost = 0;
        for (int index : selected_indices) {
            total_weight += items[index - 1].weight;
            total_cost += items[index - 1].cost;
        }

        return Solution(total_weight, total_cost, selected_indices);
    }
};

int main() {
    double approximation_coefficient;
    cin >> approximation_coefficient;

    int max_weight;
    cin >> max_weight;

    vector<Item> items;
    int i = 1;
    int weight, cost;

    while (cin >> weight >> cost) {
        items.emplace_back(i, weight, cost);
        ++i;
    }

    KnapsackProblem knapsack(items, max_weight, approximation_coefficient);
    Solution solution = knapsack.approximate_solution();
    solution.output();

    return 0;
}