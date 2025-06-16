import networkx as nx
import matplotlib.pyplot as plt

node_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
reverse_map = {v: k for k, v in node_map.items()}


edges_huruf = [['a', 'b'], ['a', 'd'], ['a', 'e'], ['b', 'c'], ['c', 'h'], ['c', 'g'], ['h', 'g'], ['i', 'h'], ['i', 'g'], ['b', 'd'], ['e', 'd'], ['d', 'f'], ['e', 'f'], ['f', 'j']]

edges = [[node_map[u], node_map[v]] for u, v in edges_huruf]
v = len(node_map)

def constructadj(x, edges):
    adj = [[] for _ in range(x)]

    for u, v in edges:
        adj[u].append(v)

    return adj

def topologicalSort(v, adj, visited, stack):
    visited[v] = True

    for i in adj[v]:
        if not visited[i]:
            topologicalSort(i, adj, visited, stack)

    stack.append(v)

adj = constructadj(v, edges)
stack = []
visited = [False] * v

start_node = node_map['a']
topologicalSort(start_node, adj, visited, stack)

print("Urutan Topological Sort:")
print(" -> ".join(reverse_map[i] for i in stack[::-1]))

G = nx.DiGraph()
for u, v in edges_huruf:
    G.add_edge(u, v)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
plt.title("Graf Topological ")
plt.show()