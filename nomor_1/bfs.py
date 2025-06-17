import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict

class BFSGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()
    
    def add_edge(self, u, v):
        """Menambahkan edge dari u ke v (directed graph)"""
        self.graph[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)
    
    def bfs_tree(self, start):
        """Melakukan BFS dan mengembalikan BFS tree"""
        visited = {vertex: False for vertex in self.vertices}
        queue = deque([start])
        visited[start] = True
        
        # Untuk menyimpan BFS tree
        bfs_tree = []
        distances = {start: 0}
        predecessors = {start: None}
        
        print(f"\nBFS Tree starting from vertex '{start}':")
        print(f"Start: {start} (distance: 0)")
        
        while queue:
            current = queue.popleft()
            
            # Proses semua tetangga dari vertex current
            for neighbor in sorted(self.graph[current]):  # Sort untuk konsistensi
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
                    distances[neighbor] = distances[current] + 1
                    predecessors[neighbor] = current
                    bfs_tree.append((current, neighbor))
                    print(f"Visit: {neighbor} (distance: {distances[neighbor]}, predecessor: {current})")
        
        return bfs_tree, distances, predecessors
    
    def visualize_bfs_tree(self, start, bfs_tree):
        """Visualisasi BFS tree"""
        # Membuat graf untuk visualisasi
        G = nx.DiGraph()
        
        # Menambahkan semua vertices
        for vertex in self.vertices:
            G.add_node(vertex)
        
        # Menambahkan edges dari graf asli
        for u in self.graph:
            for v in self.graph[u]:
                G.add_edge(u, v)
        
        # Membuat BFS tree graph
        BFS_tree_graph = nx.DiGraph()
        BFS_tree_graph.add_nodes_from(self.vertices)
        BFS_tree_graph.add_edges_from(bfs_tree)
        
        # Membuat subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Graf asli
        pos1 = nx.spring_layout(G, seed=42)
        ax1.set_title("Graf Asli", fontsize=14, fontweight='bold')
        nx.draw(G, pos1, ax=ax1, with_labels=True, node_color='lightblue', 
                node_size=1000, font_size=12, font_weight='bold', arrows=True)
        
        # BFS Tree
        pos2 = nx.spring_layout(BFS_tree_graph, seed=42)
        ax2.set_title(f"BFS Tree (start: {start})", fontsize=14, fontweight='bold')
        nx.draw(BFS_tree_graph, pos2, ax=ax2, with_labels=True, node_color='lightgreen', 
                node_size=1000, font_size=12, font_weight='bold', arrows=True)
        
        plt.tight_layout()
        plt.show()

def create_default_graph():
    """Membuat graf default dari soal"""
    graph = BFSGraph()
    
    # Edges berdasarkan gambar soal
    edges = [
        ('a', 'b'), ('a', 'e'),
        ('b', 'c'), ('b', 'd'),
        ('c', 'h'), ('c', 'g'),
        ('d', 'f'),
        ('e', 'd'),
        ('f', 'j'),
        ('g', 'i'),
        ('h', 'g'), ('h', 'i'),
        ('i', 'g')
    ]
    
    for u, v in edges:
        graph.add_edge(u, v)
    
    return graph

def input_custom_graph():
    """Input graf kustom dari user"""
    graph = BFSGraph()
    
    print("\nMasukkan graf (format: vertex1 vertex2)")
    print("Ketik 'done' untuk selesai")
    
    while True:
        edge_input = input("Masukkan edge (u v): ").strip()
        if edge_input.lower() == 'done':
            break
        
        try:
            u, v = edge_input.split()
            graph.add_edge(u, v)
            print(f"Edge {u} -> {v} ditambahkan")
        except ValueError:
            print("Format tidak valid! Gunakan format: vertex1 vertex2")
    
    return graph

def main():
    print("=" * 50)
    print("PROGRAM BFS TREE")
    print("=" * 50)
    
    while True:
        print("\nMenu:")
        print("1. Gunakan graf default dari soal")
        print("2. Masukkan graf baru")
        print("3. Keluar")
        
        choice = input("Pilih opsi (1-3): ").strip()
        
        if choice == '1':
            graph = create_default_graph()
            start_vertex = 'a'  # Default starting vertex
            
            print(f"\nGraf default dimuat dengan vertices: {sorted(graph.vertices)}")
            print("Edges dalam graf:")
            for u in sorted(graph.graph.keys()):
                for v in graph.graph[u]:
                    print(f"  {u} -> {v}")
            
        elif choice == '2':
            graph = input_custom_graph()
            if not graph.vertices:
                print("Graf kosong! Silakan masukkan edges terlebih dahulu.")
                continue
            
            print(f"\nVertices dalam graf: {sorted(graph.vertices)}")
            start_vertex = input("Masukkan starting vertex: ").strip()
            
            if start_vertex not in graph.vertices:
                print("Vertex tidak ditemukan dalam graf!")
                continue
                
        elif choice == '3':
            print("Terima kasih!")
            break
            
        else:
            print("Opsi tidak valid!")
            continue
        
        # Jalankan BFS
        bfs_tree, distances, predecessors = graph.bfs_tree(start_vertex)
        
        print(f"\nBFS Tree edges: {bfs_tree}")
        print(f"Distances dari {start_vertex}: {distances}")
        print(f"Predecessors: {predecessors}")
        
        # Visualisasi
        try:
            graph.visualize_bfs_tree(start_vertex, bfs_tree)
        except Exception as e:
            print(f"Error dalam visualisasi: {e}")
            print("Pastikan matplotlib dan networkx sudah terinstall!")

if __name__ == "__main__":
    main()