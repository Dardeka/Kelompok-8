import heapq
import sys
import networkx as nx
import matplotlib.pyplot as plt

node_map = {'s': 0, 'x': 1, 'u': 2, 'v': 3, 'y': 4}
reverse_map = {v: k for k, v in node_map.items()}

edges_huruf = [['s', 'u', 10], ['s', 'x', 5], ['u', 'x', 2], ['x', 'u', 3], ['x', 'v', 9], ['u', 'v', 1], ['x', 'y', 2], ['y', 'v', 6], ['v', 'y', 4], ['y', 's', 7]]

edges = [[node_map[u], node_map[v], w] for u, v, w in edges_huruf]

V = len(node_map)
src = node_map['s']

def constructAdj(V, edges):
    adj = [[] for _ in range(V)]
    for u, v, wt in edges:
        adj[u].append([v, wt])
    return adj

adj = constructAdj(V, edges)
dist = [sys.maxsize] * V
dist[src] = 0
prev = [-1] * V 

pq = []
heapq.heappush(pq, [0, src])

while pq:
    u = heapq.heappop(pq)[1]

    for v, weight in adj[u]:
        if dist[v] > dist[u] + weight:
            dist[v] = dist[u] + weight
            prev[v] = u 
            heapq.heappush(pq, [dist[v], v])

print("Jarak dari 's':")
for i in range(V):
    print(f"{reverse_map[i]}: {dist[i]}")

G = nx.DiGraph()
for u, v, w in edges:
    G.add_edge(reverse_map[u], reverse_map[v], weight=w) 

path_edges = []
for i in range(V):
    if prev[i] != -1:
        path_edges.append((reverse_map[i], reverse_map[prev[i]]))  

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

plt.title("Graf Dijkstras")
plt.show()