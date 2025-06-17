import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class DFSGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()
        self.time = 0
        self.discovery_times = {}
        self.finish_times = {}
        self.predecessors = {}
        self.colors = {}
        self.edge_types = {}
    
    def add_edge(self, u, v):
        """Menambahkan edge dari u ke v (directed graph)"""
        self.graph[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)
    
    def reset_dfs_data(self):
        """Reset semua data DFS"""
        self.time = 0
        self.discovery_times = {}
        self.finish_times = {}
        self.predecessors = {}
        self.colors = {}
        self.edge_types = {}
    
    def dfs_visit(self, u, dfs_tree):
        """DFS Visit untuk satu vertex"""
        self.time += 1
        self.discovery_times[u] = self.time
        self.colors[u] = 'red'  # Gray/Red - sedang diproses
        print(f"Visit {u}: d[{u}] = {self.discovery_times[u]}")
        
        # Kunjungi semua tetangga
        for v in sorted(self.graph[u]):  # Sort untuk konsistensi
            edge = (u, v)
            
            if self.colors[v] == 'white':
                # Tree edge
                self.edge_types[edge] = 'T'
                self.predecessors[v] = u
                dfs_tree.append(edge)
                print(f"  Edge {u} -> {v}: Tree edge (T)")
                self.dfs_visit(v, dfs_tree)
                
            elif self.colors[v] == 'red':
                # Back edge
                self.edge_types[edge] = 'B'
                print(f"  Edge {u} -> {v}: Back edge (B)")
                
            elif self.colors[v] == 'blue':
                # Forward atau Cross edge
                if self.discovery_times[u] < self.discovery_times[v]:
                    self.edge_types[edge] = 'F'  # Forward edge
                    print(f"  Edge {u} -> {v}: Forward edge (F)")
                else:
                    self.edge_types[edge] = 'C'  # Cross edge
                    print(f"  Edge {u} -> {v}: Cross edge (C)")
        
        self.colors[u] = 'blue'  # Black/Blue - selesai diproses
        self.time += 1
        self.finish_times[u] = self.time
        print(f"Finish {u}: f[{u}] = {self.finish_times[u]}")
    
    def dfs_forest(self, start_vertex=None):
        """Melakukan DFS dan mengembalikan DFS forest"""
        self.reset_dfs_data()
        
        # Inisialisasi semua vertex
        for vertex in self.vertices:
            self.colors[vertex] = 'white'
            self.predecessors[vertex] = None
        
        dfs_tree = []
        
        print(f"\nDFS Forest:")
        print("-" * 40)
        
        if start_vertex and start_vertex in self.vertices:
            # Mulai dari vertex yang ditentukan
            vertices_to_process = [start_vertex] + [v for v in sorted(self.vertices) if v != start_vertex]
        else:
            # Mulai dari vertex pertama secara alfabetis
            vertices_to_process = sorted(self.vertices)
        
        for vertex in vertices_to_process:
            if self.colors[vertex] == 'white':
                print(f"\nStarting DFS from vertex: {vertex}")
                self.dfs_visit(vertex, dfs_tree)
        
        return dfs_tree
    
    def get_topological_sort(self):
        """Mendapatkan topological sort berdasarkan finish times"""
        if not self.finish_times:
            print("Jalankan DFS terlebih dahulu!")
            return []
        
        # Sort berdasarkan finish time secara descending
        topo_sort = sorted(self.vertices, key=lambda x: self.finish_times[x], reverse=True)
        return topo_sort
    
    def check_cycles(self):
        """Mengecek apakah graf memiliki cycle (berdasarkan back edges)"""
        back_edges = [edge for edge, edge_type in self.edge_types.items() if edge_type == 'B']
        return len(back_edges) > 0, back_edges
    
    def print_dfs_results(self):
        """Mencetak hasil DFS secara detail"""
        print(f"\nHasil DFS:")
        print("-" * 50)
        print("Vertex | Discovery | Finish | Predecessor")
        print("-" * 50)
        for vertex in sorted(self.vertices):
            pred = self.predecessors[vertex] if self.predecessors[vertex] else "None"
            print(f"  {vertex:4} |    {self.discovery_times[vertex]:2}     |   {self.finish_times[vertex]:2}   |     {pred}")
        
        print(f"\nEdge Types:")
        print("-" * 30)
        for edge, edge_type in self.edge_types.items():
            type_name = {
                'T': 'Tree',
                'B': 'Back', 
                'F': 'Forward',
                'C': 'Cross'
            }[edge_type]
            print(f"  {edge[0]} -> {edge[1]}: {type_name} ({edge_type})")
    
    def visualize_dfs_forest(self, dfs_tree):
        """Visualisasi DFS forest"""
        # Membuat graf untuk visualisasi
        G = nx.DiGraph()
        
        # Menambahkan semua vertices
        for vertex in self.vertices:
            G.add_node(vertex)
        
        # Menambahkan edges dari graf asli
        for u in self.graph:
            for v in self.graph[u]:
                G.add_edge(u, v)
        
        # Membuat DFS forest graph
        DFS_forest_graph = nx.DiGraph()
        DFS_forest_graph.add_nodes_from(self.vertices)
        DFS_forest_graph.add_edges_from(dfs_tree)
        
        # Membuat subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Graf asli dengan edge types
        pos1 = nx.spring_layout(G, seed=42)
        ax1.set_title("Graf Asli dengan Tipe Edge", fontsize=14, fontweight='bold')
        
        # Warna untuk different edge types
        edge_colors = []
        for u, v in G.edges():
            edge_type = self.edge_types.get((u, v), 'T')
            if edge_type == 'T':
                edge_colors.append('green')
            elif edge_type == 'B':
                edge_colors.append('red')
            elif edge_type == 'F':
                edge_colors.append('blue')
            else:  # Cross
                edge_colors.append('orange')
        
        nx.draw(G, pos1, ax=ax1, with_labels=True, node_color='lightblue', 
                node_size=1000, font_size=12, font_weight='bold', 
                arrows=True, edge_color=edge_colors, width=2)
        
        # Legend untuk edge types
        legend_elements = [
            plt.Line2D([0], [0], color='green', lw=2, label='Tree (T)'),
            plt.Line2D([0], [0], color='red', lw=2, label='Back (B)'),
            plt.Line2D([0], [0], color='blue', lw=2, label='Forward (F)'),
            plt.Line2D([0], [0], color='orange', lw=2, label='Cross (C)')
        ]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # DFS Forest
        pos2 = nx.spring_layout(DFS_forest_graph, seed=42)
        ax2.set_title("DFS Forest (Tree edges only)", fontsize=14, fontweight='bold')
        nx.draw(DFS_forest_graph, pos2, ax=ax2, with_labels=True, node_color='lightgreen', 
                node_size=1000, font_size=12, font_weight='bold', arrows=True,
                edge_color='green', width=2)
        
        plt.tight_layout()
        plt.show()

def create_default_graph():
    """Membuat graf default dari soal"""
    graph = DFSGraph()
    
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
    graph = DFSGraph()
    
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
    print("PROGRAM DFS FOREST")
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
            start_vertex = input("Masukkan starting vertex (Enter untuk default): ").strip()
            
            if start_vertex and start_vertex not in graph.vertices:
                print("Vertex tidak ditemukan dalam graf!")
                continue
                
        elif choice == '3':
            print("Terima kasih!")
            break
            
        else:
            print("Opsi tidak valid!")
            continue
        
        # Jalankan DFS
        dfs_tree = graph.dfs_forest(start_vertex if start_vertex else None)
        
        # Print hasil detail
        graph.print_dfs_results()
        
        # Cek cycle dan topological sort
        has_cycle, back_edges = graph.check_cycles()
        print(f"\nApakah graf memiliki cycle? {'Ya' if has_cycle else 'Tidak'}")
        if has_cycle:
            print(f"Back edges yang menyebabkan cycle: {back_edges}")
        
        if not has_cycle:
            topo_sort = graph.get_topological_sort()
            print(f"Topological Sort: {' -> '.join(topo_sort)}")
        else:
            print("Tidak dapat membuat topological sort karena graf memiliki cycle.")
        
        print(f"\nDFS Tree edges: {dfs_tree}")
        
        # Visualisasi
        try:
            graph.visualize_dfs_forest(dfs_tree)
        except Exception as e:
            print(f"Error dalam visualisasi: {e}")
            print("Pastikan matplotlib dan networkx sudah terinstall!")

if __name__ == "__main__":
    main()