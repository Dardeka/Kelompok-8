import heapq
import sys
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra_and_plot(node_map, edges_huruf, source_label):
    reverse_map = {v: k for k, v in node_map.items()}
    edges = [[node_map[u], node_map[v], w] for u, v, w in edges_huruf]

    V = len(node_map)
    src = node_map[source_label]

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

    print(f"\nJarak dari simpul '{source_label}':")
    for i in range(V):
        print(f"{reverse_map[i]}: {dist[i]}")

    G = nx.DiGraph()
    for u, v, w in edges:
        G.add_edge(reverse_map[u], reverse_map[v], weight=w)

    path_edges = []
    for i in range(V):
        if prev[i] != -1:
            path_edges.append((reverse_map[prev[i]], reverse_map[i]))

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title("Graf Dijkstra")
    plt.show()

print("=== PROGRAM DIJKSTRA ===")
print("1. Gunakan graf bawaan")
print("2. Masukkan graf sendiri")
choice = input("Pilihan (1/2): ")

if choice == '1':
    # Graf default
    node_map = {'s': 0, 'x': 1, 'u': 2, 'v': 3, 'y': 4}
    edges_huruf = [
        ['s', 'u', 10], ['s', 'x', 5], ['u', 'x', 2], ['x', 'u', 3],
        ['x', 'v', 9], ['u', 'v', 1], ['x', 'y', 2], ['y', 'v', 6],
        ['v', 'y', 4], ['y', 's', 7]
    ]
    source_label = 's'

elif choice == '2':
    print("\nMasukkan daftar simpul, pisahkan dengan koma (contoh: a,b,c):")
    nodes_input = input("Simpul: ").replace(" ", "").split(',')
    node_map = {name: idx for idx, name in enumerate(nodes_input)}

    print("\nMasukkan jumlah edge (sisi):")
    n_edges = int(input("Jumlah edge: "))

    edges_huruf = []
    print("Masukkan masing-masing edge dalam format: asal tujuan bobot")
    for i in range(n_edges):
        raw = input(f"Edge {i+1}: ").split()
        u, v, w = raw[0], raw[1], int(raw[2])
        edges_huruf.append([u, v, w])

    print("\nMasukkan simpul asal untuk algoritma Dijkstra:")
    source_label = input("Simpul asal: ")

else:
    print("Pilihan tidak valid.")
    sys.exit(1)

dijkstra_and_plot(node_map, edges_huruf, source_label)
