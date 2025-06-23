from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class DFSGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()
        self.timestamps = {}  # Untuk menyimpan d[u] dan f[u]
        self.time = 0
        self.colors = {}  # Untuk menyimpan warna vertex
        self.parent = {}  # Untuk menyimpan parent/predecessor
        self.edge_types = {}  # Untuk menyimpan jenis edge (T, B, F, C)
    
    def add_edge(self, u, v):
        """Menambahkan edge dari vertex u ke vertex v"""
        self.graph[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)
    
    def display_graph(self):
        """Menampilkan representasi graf"""
        print("Graf saat ini:")
        for vertex in sorted(self.vertices):
            if vertex in self.graph:
                print(f"{vertex} -> {', '.join(sorted(self.graph[vertex]))}")
            else:
                print(f"{vertex} -> (tidak ada edge keluar)")
        print()
    
    def reset_dfs_data(self):
        """Reset semua data DFS untuk run yang baru"""
        self.timestamps = {}
        self.time = 0
        self.colors = {}
        self.parent = {}
        self.edge_types = {}
        
        # Inisialisasi warna semua vertex ke white
        for vertex in self.vertices:
            self.colors[vertex] = 'white'
            self.parent[vertex] = None
    
    def dfs_with_timestamps(self, start_vertex=None):
        """DFS dengan timestamp seperti algoritma pada buku"""
        self.reset_dfs_data()
        
        visited_order = []
        tree_edges = []
        
        def dfs_visit(u):
            nonlocal visited_order, tree_edges
            
            # Vertex u ditemukan (discovery time)
            self.time += 1
            self.timestamps[u] = [self.time, 0]  # [d[u], f[u]]
            self.colors[u] = 'gray'  # Sedang diproses
            visited_order.append(u)
            
            print(f"Menemukan vertex {u} pada waktu {self.time}")
            
            # Eksplorasi semua tetangga u
            neighbors = sorted(self.graph[u])  # Sort untuk konsistensi
            for v in neighbors:
                edge = (u, v)
                
                if self.colors[v] == 'white':
                    # Tree edge
                    self.edge_types[edge] = 'T'
                    self.parent[v] = u
                    tree_edges.append(edge)
                    print(f"  Edge {u} -> {v}: Tree edge (T)")
                    dfs_visit(v)
                    
                elif self.colors[v] == 'gray':
                    # Back edge
                    self.edge_types[edge] = 'B'
                    print(f"  Edge {u} -> {v}: Back edge (B)")
                    
                elif self.colors[v] == 'black':
                    # Forward atau Cross edge
                    if self.timestamps[u][0] < self.timestamps[v][0]:
                        # Forward edge
                        self.edge_types[edge] = 'F'
                        print(f"  Edge {u} -> {v}: Forward edge (F)")
                    else:
                        # Cross edge
                        self.edge_types[edge] = 'C'
                        print(f"  Edge {u} -> {v}: Cross edge (C)")
            
            # Selesai memproses vertex u (finish time)
            self.colors[u] = 'black'
            self.time += 1
            self.timestamps[u][1] = self.time
            print(f"Selesai memproses vertex {u} pada waktu {self.time}")
        
        # Mulai DFS dari vertex yang dipilih
        if start_vertex and start_vertex in self.vertices:
            if self.colors[start_vertex] == 'white':
                print(f"\n=== Memulai DFS dari vertex {start_vertex} ===")
                dfs_visit(start_vertex)
        
        # Lanjutkan untuk vertex lain yang belum dikunjungi
        for vertex in sorted(self.vertices):
            if self.colors[vertex] == 'white':
                print(f"\n=== Memulai DFS dari vertex {vertex} (komponen baru) ===")
                dfs_visit(vertex)
        
        return visited_order, tree_edges
    
    def print_dfs_summary(self):
        """Mencetak ringkasan hasil DFS"""
        print("\n" + "="*50)
        print("RINGKASAN HASIL DFS")
        print("="*50)
        
        print("Timestamps untuk setiap vertex:")
        for vertex in sorted(self.vertices):
            d_time, f_time = self.timestamps[vertex]
            print(f"  {vertex}: d[{vertex}] = {d_time}, f[{vertex}] = {f_time}")
        
        print("\nKlasifikasi edges:")
        edge_count = {'T': 0, 'B': 0, 'F': 0, 'C': 0}
        for edge, edge_type in self.edge_types.items():
            edge_count[edge_type] += 1
            print(f"  {edge[0]} -> {edge[1]}: {edge_type}")
        
        print(f"\nJumlah edges per tipe:")
        print(f"  Tree edges (T): {edge_count['T']}")
        print(f"  Back edges (B): {edge_count['B']}")
        print(f"  Forward edges (F): {edge_count['F']}")
        print(f"  Cross edges (C): {edge_count['C']}")
    
    def has_cycle(self):
        """Mengecek apakah graf memiliki cycle berdasarkan back edges"""
        return any(edge_type == 'B' for edge_type in self.edge_types.values())
    
    def topological_sort(self):
        """Topological Sort berdasarkan finish time"""
        if self.has_cycle():
            return None
        
        # Urutkan vertex berdasarkan finish time secara descending
        sorted_vertices = sorted(self.vertices, 
                               key=lambda x: self.timestamps[x][1], 
                               reverse=True)
        return sorted_vertices
    
    def visualize_graph_with_timestamps(self, title="Graf dengan Timestamps", 
                                      highlight_edges=None, highlight_colors=None):
        """Visualisasi graf dengan timestamps seperti contoh"""
        try:
            # Membuat graf NetworkX
            G = nx.DiGraph()
            
            # Menambahkan edges
            for vertex in self.graph:
                for neighbor in self.graph[vertex]:
                    G.add_edge(vertex, neighbor)
            
            # Menambahkan isolated vertices
            for vertex in self.vertices:
                if vertex not in G.nodes():
                    G.add_node(vertex)
            
            plt.figure(figsize=(12, 8))
            
            # Layout untuk posisi nodes
            pos = self._get_better_layout(G)
            
            # Warna nodes berdasarkan tipe edge atau default
            node_colors = []
            node_labels = {}
            
            for node in G.nodes():
                # Buat label dengan timestamp jika ada
                if node in self.timestamps:
                    d_time, f_time = self.timestamps[node]
                    node_labels[node] = f"{node}\n{d_time}/{f_time}"
                else:
                    node_labels[node] = node
                
                # Tentukan warna node
                if highlight_colors and node in highlight_colors:
                    node_colors.append(highlight_colors[node])
                else:
                    # Warna berdasarkan jenis edges yang terlibat
                    has_back_edge = any(
                        (edge[0] == node or edge[1] == node) and self.edge_types.get(edge) == 'B'
                        for edge in self.edge_types
                    )
                    if has_back_edge:
                        node_colors.append('lightcoral')  # Merah muda untuk nodes dengan back edge
                    else:
                        node_colors.append('lightblue')   # Biru muda untuk nodes biasa
            
            # Gambar semua edges dengan warna abu-abu terlebih dahulu
            nx.draw_networkx_edges(G, pos, edge_color='lightgray', arrows=True, 
                                 arrowsize=20, arrowstyle='->', width=1.5, alpha=0.6,
                                 connectionstyle="arc3,rad=0.1")
            
            # Highlight edges berdasarkan tipe
            if highlight_edges:
                edge_colors = {
                    'T': 'blue',    # Tree edges - biru
                    'B': 'red',     # Back edges - merah
                    'F': 'green',   # Forward edges - hijau
                    'C': 'purple'   # Cross edges - ungu
                }
                
                for edge_type, color in edge_colors.items():
                    edges_of_type = [edge for edge, etype in self.edge_types.items() 
                                   if etype == edge_type and edge in highlight_edges]
                    
                    if edges_of_type:
                        nx.draw_networkx_edges(G, pos, edgelist=edges_of_type, 
                                             edge_color=color, arrows=True, 
                                             arrowsize=20, arrowstyle='->', width=3,
                                             connectionstyle="arc3,rad=0.1", alpha=0.8)
            
            # Gambar nodes
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                 node_size=2000, alpha=0.9, 
                                 edgecolors='black', linewidths=2)
            
            # Gambar labels dengan timestamps
            nx.draw_networkx_labels(G, pos, labels=node_labels, 
                                  font_size=10, font_weight='bold', 
                                  font_color='black')
            
            # Tambahkan legend untuk jenis edges
            if self.edge_types:
                legend_elements = []
                edge_colors = {
                    'T': ('blue', 'Tree edges'),
                    'B': ('red', 'Back edges'), 
                    'F': ('green', 'Forward edges'),
                    'C': ('purple', 'Cross edges')
                }
                
                for edge_type, (color, label) in edge_colors.items():
                    if any(etype == edge_type for etype in self.edge_types.values()):
                        legend_elements.append(plt.Line2D([0], [0], color=color, lw=3, label=label))
                
                if legend_elements:
                    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
            
            plt.title(title, fontsize=16, fontweight='bold', pad=20)
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Error: NetworkX atau Matplotlib tidak terinstall.")
            print("Silakan install dengan: pip install networkx matplotlib")
        except Exception as e:
            print(f"Error dalam visualisasi: {e}")
    
    def _get_better_layout(self, G):
        """Layout yang lebih baik untuk visualisasi"""
        if len(G.nodes()) == 0:
            return {}
        
        # Posisi manual untuk graf yang umum digunakan
        common_layouts = {
            # Layout untuk graf dengan vertex s,t,u,v,w,x,y,z
            frozenset(['s', 't', 'u', 'v', 'w', 'x', 'y', 'z']): {
                's': (-2, 0), 't': (0, 1), 'u': (2, 0), 'v': (0, -1),
                'w': (1, -1), 'x': (-1, -2), 'y': (-1, 0), 'z': (1, 1)
            },
            # Layout untuk graf a,b,c,d,e,f,g,h,i,j
            frozenset(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']): {
                'a': (0, 0), 'b': (2, 1), 'c': (4, 2), 'd': (2, -1),
                'e': (1, -2), 'f': (3, -2), 'g': (6, 1), 'h': (5, 3),
                'i': (7, 4), 'j': (4, -4)
            }
        }
        
        node_set = frozenset(G.nodes())
        for layout_nodes, positions in common_layouts.items():
            if node_set.issubset(layout_nodes):
                return {node: positions[node] for node in G.nodes()}
        
        # Fallback ke spring layout
        return nx.spring_layout(G, k=3, iterations=100, seed=42)

def create_default_graph():
    """Membuat graf default dari soal asli"""
    g = DFSGraph()
    edges = [('a', 'b'), ('a', 'd'), ('a', 'e'), ('b', 'c'), ('b', 'd'),
             ('c', 'h'), ('c', 'g'), ('d', 'f'), ('e', 'd'), ('e', 'f'),
             ('f', 'j'), ('h', 'g'), ('i', 'g'), ('i', 'h')]
    for u, v in edges:
        g.add_edge(u, v)
    return g

def input_custom_graph():
    """Input graf custom dari user"""
    g = DFSGraph()
    print("\nMasukkan edges graf (format: u v)")
    print("Ketik 'selesai' untuk mengakhiri input")
    print("Contoh: a b")
    print("-" * 30)
    
    while True:
        edge_input = input("Masukkan edge: ").strip()
        if edge_input.lower() == 'selesai':
            break
        
        try:
            parts = edge_input.split()
            if len(parts) != 2:
                print("Format salah! Gunakan format: u v")
                continue
            
            u, v = parts[0], parts[1]
            g.add_edge(u, v)
            print(f"✓ Edge {u} -> {v} berhasil ditambahkan")
        except Exception as e:
            print(f"Error: {e}")
    
    return g

def main():
    print("="*70)
    print("PROGRAM DFS DENGAN TIMESTAMPS DAN KLASIFIKASI EDGES")
    print("="*70)
    print("Pastikan dependencies terinstall: pip install networkx matplotlib")
    print("="*70)
    
    while True:
        print("\nMenu:")
        print("1. Gunakan graf default dari soal")
        print("2. Masukkan graf baru")
        print("3. Keluar")
        
        try:
            choice = int(input("Masukkan pilihan (1-3): "))
        except ValueError:
            print("Input tidak valid!")
            continue
        
        if choice == 3:
            print("Terima kasih!")
            break
        
        elif choice == 1:
            # Gunakan graf default dari soal
            selected_graph = create_default_graph()
            graph_name = "Graf Default dari Soal"
            
            print(f"\n{'='*50}")
            print(f"MENGGUNAKAN GRAF DEFAULT")
            print("="*50)
            print("Graf default berhasil dimuat!")
        
        elif choice == 2:
            # Input graf custom
            selected_graph = input_custom_graph()
            graph_name = "Graf Custom"
            
            if not selected_graph.vertices:
                print("Graf kosong!")
                continue
                
            print(f"\n{'='*50}")
            print(f"GRAF CUSTOM BERHASIL DIBUAT")
            print("="*50)
        
        else:
            print("Pilihan tidak valid!")
            continue
        
        # Tampilkan graf
        print(f"\nANALISIS: {graph_name}")
        print("="*50)
        selected_graph.display_graph()
        
        # Pilih vertex start untuk DFS
        vertices_list = sorted(selected_graph.vertices)
        print(f"Vertex yang tersedia: {', '.join(vertices_list)}")
        
        start_vertex = input(f"Pilih vertex start untuk DFS (default: {vertices_list[0]}): ").strip()
        if not start_vertex or start_vertex not in selected_graph.vertices:
            start_vertex = vertices_list[0]
        
        print(f"\nMemulai DFS dari vertex: {start_vertex}")
        
        # Jalankan DFS
        visited_order, tree_edges = selected_graph.dfs_with_timestamps(start_vertex)
        
        # Tampilkan hasil
        selected_graph.print_dfs_summary()
        
        # Topological sort
        print(f"\n{'='*50}")
        print("TOPOLOGICAL SORT")
        print("="*50)
        
        topo_result = selected_graph.topological_sort()
        if topo_result is None:
            print("TIDAK DAPAT DILAKUKAN (Graf memiliki cycle - ada back edges)")
        else:
            print(f"Hasil topological sort: {' -> '.join(topo_result)}")
        
        # Visualisasi
        print(f"\nMenampilkan visualisasi graf...")
        
        # Graf asli
        selected_graph.visualize_graph_with_timestamps(
            f"Graf Asli: {graph_name}",
            highlight_edges=list(selected_graph.edge_types.keys())
        )
        
        # Tree edges saja
        tree_edges_only = [edge for edge, etype in selected_graph.edge_types.items() 
                          if etype == 'T']
        if tree_edges_only:
            selected_graph.visualize_graph_with_timestamps(
                f"DFS Tree dari vertex {start_vertex}",
                highlight_edges=tree_edges_only
            )

if __name__ == "__main__":
    main()