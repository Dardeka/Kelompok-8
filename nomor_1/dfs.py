from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

time = 0

def dfs_visit(graph, u, visited, parent, d, f, tree_edges, back_edges, forward_edges, cross_edges):
    global time
    visited[u] = "gray"
    time += 1
    d[u] = time

    for v in graph[u]:
        if visited[v] == "white":
            parent[v] = u
            tree_edges.append((u, v))
            dfs_visit(graph, v, visited, parent, d, f, tree_edges, back_edges, forward_edges, cross_edges)
        elif visited[v] == "gray":
            back_edges.append((u, v))
        elif visited[v] == "black":
            if d[u] < d[v]:
                forward_edges.append((u, v))
            else:
                cross_edges.append((u, v))

    visited[u] = "black"
    time += 1
    f[u] = time

def dfs_tree(graph, start):
    visited = {v: "white" for v in graph}
    parent = {v: None for v in graph}
    d = {}
    f = {}
    tree_edges, back_edges, forward_edges, cross_edges = [], [], [], []

    dfs_visit(graph, start, visited, parent, d, f, tree_edges, back_edges, forward_edges, cross_edges)

    return d, f, tree_edges, back_edges, forward_edges, cross_edges

def input_graph():
    graph = {}
    print("\nMasukkan daftar simpul (pisahkan dengan spasi):")
    nodes = input(">> ").split()
    for node in nodes:
        edges = input(f"Masukkan tetangga dari simpul '{node}' (pisahkan dengan spasi):\n>> ").split()
        graph[node] = edges
    return graph

def draw_graph(graph, T, B, F, C):
    G = nx.DiGraph()
    for u in graph:
        for v in graph[u]:
            G.add_edge(u, v)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue')
    nx.draw_networkx_labels(G, pos)

    nx.draw_networkx_edges(G, pos, edgelist=T, edge_color='green', width=2, label='Tree edges (T)')
    nx.draw_networkx_edges(G, pos, edgelist=B, edge_color='red', style='dashed', width=2, label='Back edges (B)')
    nx.draw_networkx_edges(G, pos, edgelist=F, edge_color='orange', style='dotted', width=2, label='Forward edges (F)')
    nx.draw_networkx_edges(G, pos, edgelist=C, edge_color='gray', style='dashdot', width=2, label='Cross edges (C)')

    plt.title("Visualisasi DFS Tree dan Jenis Edge")
    plt.axis('off')
    plt.legend()
    plt.show()

def main():
    while True:
        print("\nMenu:")
        print("1. Gunakan graf default dari soal")
        print("2. Masukkan graf baru")
        print("3. Keluar")
        choice = input("Pilih opsi (1/2/3): ")

        if choice == '1':
            graph = {
                'a': ['b', 'd', 'e'],
                'b': [],
                'c': ['b', 'g'],
                'd': ['c'],
                'e': ['f'],
                'f': ['d', 'j'],
                'g': ['h'],
                'h': ['i'],
                'i': [],
                'j': []
            }
        elif choice == '2':
            graph = input_graph()
        elif choice == '3':
            print("Program selesai.")
            break
        else:
            print("Opsi tidak valid.")
            continue

        print("\nSimpul tersedia:", list(graph.keys()))
        start = input("Masukkan simpul awal DFS:\n>> ").strip()
        if start not in graph:
            print("Simpul tidak ditemukan di graf.")
            continue

        global time
        time = 0
        d, f, T, B, F, C = dfs_tree(graph, start)

        print(f"\nDFS Tree (start dari '{start}'):")
        print("Discovery & Finish Time:")
        for v in sorted(graph):
            print(f"{v}: d={d.get(v, '-')}, f={f.get(v, '-')}")
        print("\nTree edges (T):", T)
        print("Back edges (B):", B)
        print("Forward edges (F):", F)
        print("Cross edges (C):", C)

        draw_graph(graph, T, B, F, C)

if __name__ == "__main__":
    main()
