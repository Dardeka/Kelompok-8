from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

def bfs_tree(graph, start):
    visited = set()
    tree_edges = []
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                tree_edges.append((node, neighbor))
                queue.append(neighbor)
    return tree_edges

def input_graph():
    graph = {}
    print("\nMasukkan daftar simpul (pisahkan dengan spasi):")
    nodes = input(">> ").split()
    for node in nodes:
        edges = input(f"Masukkan tetangga dari simpul '{node}' (pisahkan dengan spasi):\n>> ").split()
        graph[node] = edges
    return graph

def draw_graph(graph, tree_edges=None):
    G = nx.DiGraph()
    for node in graph:
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue')
    nx.draw_networkx_labels(G, pos)

    if tree_edges:
        tree_set = set(tree_edges)
        other_edges = [edge for edge in G.edges() if edge not in tree_set]
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='green', width=2, label='BFS Tree')
        nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color='gray', style='dashed', alpha=0.5)
    else:
        nx.draw_networkx_edges(G, pos)

    plt.title("Visualisasi Graf & BFS Tree")
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
        start = input("Masukkan simpul awal BFS:\n>> ").strip()
        if start not in graph:
            print("Simpul tidak ada dalam graf. Ulangi.")
            continue

        print(f"\nBFS Tree (mulai dari simpul '{start}'):")
        tree = bfs_tree(graph, start)
        for edge in tree:
            print(f"{edge[0]} -> {edge[1]}")

        draw_graph(graph, tree_edges=tree)

if __name__ == "__main__":
    main()
