# 🧠 Python DSA Solutions

A curated collection of **Data Structures and Algorithms** implemented in Python with clean, well-documented code.

Each implementation includes:
- 📖 Clear docstrings with time/space complexity analysis
- ✅ Built-in test cases using `doctest`
- 🎯 Multiple approaches where applicable

## 📂 Structure

```
python-dsa-solutions/
├── data_structures/
│   ├── b_tree.py
│   ├── binary_search_tree.py
│   ├── disjoint_set.py
│   ├── fenwick_tree.py
│   ├── linked_list.py
│   ├── lru_cache.py
│   ├── queue.py
│   ├── segment_tree.py
│   ├── skip_list.py
│   ├── stack.py
│   └── trie.py
├── dynamic_programming/
│   └── dp_solutions.py
├── graphs/
│   ├── a_star.py
│   ├── bellman_ford.py
│   ├── dijkstra.py
│   ├── eulerian_path.py
│   ├── floyd_warshall.py
│   ├── graph_traversals.py
│   ├── kosaraju_scc.py
│   ├── kruskal_mst.py
│   ├── max_flow_edmonds_karp.py
│   ├── tarjan_scc.py
│   └── topological_sort.py
├── searching/
│   ├── binary_search.py
│   └── interpolation_search.py
├── sorting/
│   ├── heap_sort.py
│   ├── merge_sort.py
│   └── quick_sort.py
└── README.md
```

## 📊 Graph Algorithms Overview

| Algorithm | File | Time Complexity | Space Complexity | Use Case |
|---|---|---|---|---|
| **Edmonds-Karp Max Flow** | `graphs/max_flow_edmonds_karp.py` | $O(V \cdot E^2)$ | $O(V + E)$ | Network flow optimization & Min-Cut |
| **Hierholzer's Eulerian Path** | `graphs/eulerian_path.py` | $O(V + E)$ | $O(V + E)$ | Eulerian path/circuit detection & reconstruction |
| **A\* Pathfinding** | `graphs/a_star.py` | $O(E)$ worst case | $O(V)$ | Heuristic 2D grid pathfinding |
| **Kosaraju's SCC** | `graphs/kosaraju_scc.py` | $O(V + E)$ | $O(V)$ | Strongly Connected Components (2-pass DFS) |
| **Tarjan's SCC** | `graphs/tarjan_scc.py` | $O(V + E)$ | $O(V)$ | Strongly Connected Components (Single-pass DFS) |

## 🚀 How to Run

Each file is self-contained. Run any file directly:

```bash
python sorting/merge_sort.py
```

Or run with doctests:

```bash
python -m doctest sorting/merge_sort.py -v
```

## 🤝 Contributing

Feel free to add new algorithms! Please follow the existing code style:
1. Include docstrings with complexity analysis
2. Add `doctest` examples
3. Keep implementations clean and readable

## 📄 License

MIT License — feel free to use this code for learning and reference.
