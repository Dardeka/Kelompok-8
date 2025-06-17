from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

class BFSGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()
    
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
    
    def bfs_tree(self, start):
        """Breadth-First Search Tree dari vertex start"""
        if start not in self.vertices:
            return None, []
        
        visited = set()
        queue = deque([start])
        tree_edges = []
        traversal_order = []
        levels = {start: 0}  # Untuk menampilkan level
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                traversal_order.append(vertex)
                
                # Urutkan neighbors untuk konsistensi
                neighbors = sorted(self.graph[vertex])
                for neighbor in neighbors:
                    if neighbor not in visited and neighbor not in queue:
                        tree_edges.append((vertex, neighbor))
                        levels[neighbor] = levels[vertex] + 1
                        queue.append(neighbor)
        
        return tree_edges, traversal_order, levels
    
    def bfs_levels(self, start):
        """BFS dengan informasi level"""
        if start not in self.vertices:
            return None
        
        visited = set()
        queue = deque([(start, 0)])  # (vertex, level)
        levels = defaultdict(list)
        
        while queue:
            vertex, level = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                levels[level].append(vertex)
                
                # Urutkan neighbors untuk konsistensi
                neighbors = sorted(self.graph[vertex])
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, level + 1))
        
        return dict(levels)
    
    def shortest_path_bfs(self, start, end):
        """Mencari shortest path menggunakan BFS"""
        if start not in self.vertices or end not in self.vertices:
            return None, float('inf')
        
        if start == end:
            return [start], 0
        
        visited = set()
        queue = deque([(start, [start])])
        
        while queue:
            vertex, path = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                
                # Urutkan neighbors untuk konsistensi
                neighbors = sorted(self.graph[vertex])
                for neighbor in neighbors:
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                        if neighbor == end:
                            return new_path, len(new_path) - 1
                        queue.append((neighbor, new_path))
        
        return None, float('inf')  # Tidak ada path
    
    def connected_components_bfs(self):
        """Mencari connected components menggunakan BFS"""
        visited = set()
        components = []
        
        for vertex in sorted(self.vertices):
            if vertex not in visited:
                component = []
                queue = deque([vertex])
                
                while queue:
                    current = queue.popleft()
                    if current not in visited:
                        visited.add(current)
                        component.append(current)
                        
                        # Tambahkan neighbors yang belum dikunjungi
                        neighbors = sorted(self.graph[current])
                        for neighbor in neighbors:
                            if neighbor not in visited:
                                queue.append(neighbor)
                
                components.append(sorted(component))
        
        return components

    def visualize_graph(self, title="Graf", highlight_edges=None, highlight_color='red', highlight_levels=None):
        """Visualisasi graf menggunakan NetworkX dan Matplotlib"""
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
            
            # Ukuran figure yang lebih kecil untuk menghindari terpotong
            plt.figure(figsize=(10, 8))
            
            # Definisi posisi manual untuk graf yang lebih mudah dipahami
            pos = self._get_better_layout(G)
            
            # Menggambar semua edges dengan warna abu-abu
            nx.draw_networkx_edges(G, pos, edge_color='lightgray', arrows=True, 
                                 arrowsize=20, arrowstyle='->', width=1.5, alpha=0.6,
                                 connectionstyle="arc3,rad=0.1")
            
            # Highlight edges tertentu jika ada
            if highlight_edges:
                highlight_edge_list = [(u, v) for u, v in highlight_edges if G.has_edge(u, v)]
                if highlight_edge_list:
                    nx.draw_networkx_edges(G, pos, edgelist=highlight_edge_list, 
                                         edge_color=highlight_color, arrows=True, 
                                         arrowsize=20, arrowstyle='->', width=3,
                                         connectionstyle="arc3,rad=0.1")
            
            # Menggambar nodes dengan warna berdasarkan level (jika ada)
            node_colors = []
            if highlight_levels:
                color_map = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightpink', 'lightgray']
                for node in G.nodes():
                    level = highlight_levels.get(node, 0)
                    node_colors.append(color_map[level % len(color_map)])
            else:
                for node in G.nodes():
                    if highlight_edges and any(node in edge for edge in highlight_edges):
                        node_colors.append('lightcoral')
                    else:
                        node_colors.append('lightblue')
            
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                 node_size=1200, alpha=0.9, 
                                 edgecolors='black', linewidths=1.5)
            
            # Menggambar labels dengan font yang lebih kecil
            nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', 
                                  font_color='black')
            
            plt.title(title, fontsize=16, fontweight='bold', pad=20)
            plt.axis('off')
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)  # Memberikan ruang untuk judul
            plt.show()
            
        except ImportError:
            print("Error: NetworkX atau Matplotlib tidak terinstall.")
            print("Silakan install dengan: pip install networkx matplotlib")
        except Exception as e:
            print(f"Error dalam visualisasi: {e}")
    
    def _get_better_layout(self, G):
        """Membuat layout yang lebih mudah dipahami untuk graf"""
        # Jika graf kosong, gunakan layout default
        if len(G.nodes()) == 0:
            return {}
        
        # Posisi manual untuk graf default dari soal
        default_pos = {
            'a': (0, 0),     # Start node di tengah kiri
            'b': (2, 1),     # Atas kanan dari a
            'c': (4, 2),     # Lanjutan dari b
            'd': (2, -1),    # Bawah kanan dari a
            'e': (1, -2),    # Bawah dari a
            'f': (3, -2),    # Kanan dari e
            'g': (6, 1),     # Kanan dari c
            'h': (5, 3),     # Atas dari g
            'i': (7, 4),     # Isolated node di atas kanan
            'j': (4, -4)     # Bawah dari f
        }
        
        # Cek apakah semua node dari graf default ada
        if all(node in default_pos for node in G.nodes()):
            return {node: default_pos[node] for node in G.nodes()}
        
        # Untuk graf custom, gunakan hierarchical layout
        try:
            # Coba gunakan hierarchical layout
            pos = self._hierarchical_layout(G)
            return pos
        except:
            # Fallback ke spring layout yang lebih stabil
            return nx.spring_layout(G, k=3, iterations=100, seed=42)
    
    def _hierarchical_layout(self, G):
        """Membuat layout hierarkis berdasarkan level dari root"""
        pos = {}
        
        # Cari semua root nodes (nodes tanpa incoming edges)
        roots = [node for node in G.nodes() if G.in_degree(node) == 0]
        
        if not roots:
            # Jika tidak ada root, pilih node dengan out-degree tertinggi
            roots = [max(G.nodes(), key=lambda x: G.out_degree(x))]
        
        # Assign level untuk setiap node
        levels = {}
        visited = set()
        
        def assign_level(node, level):
            if node in visited:
                return
            visited.add(node)
            levels[node] = level
            
            for neighbor in G.neighbors(node):
                if neighbor not in levels:
                    assign_level(neighbor, level + 1)
        
        # Mulai dari semua root nodes
        for root in roots:
            assign_level(root, 0)
        
        # Assign level untuk isolated nodes
        for node in G.nodes():
            if node not in levels:
                levels[node] = max(levels.values()) + 1 if levels else 0
        
        # Buat posisi berdasarkan level
        level_counts = {}
        for node, level in levels.items():
            if level not in level_counts:
                level_counts[level] = 0
            level_counts[level] += 1
        
        level_positions = {}
        for level in level_counts:
            level_positions[level] = 0
        
        for node in sorted(G.nodes()):
            level = levels[node]
            max_in_level = level_counts[level]
            current_pos = level_positions[level]
            
            # Posisi horizontal berdasarkan level
            x = level * 3
            
            # Posisi vertikal terdistribusi merata dalam level
            if max_in_level == 1:
                y = 0
            else:
                y = (current_pos - (max_in_level - 1) / 2) * 2
            
            pos[node] = (x, y)
            level_positions[level] += 1
        
        return pos

def print_bfs_results(g, start_vertex='a'):
    """Mencetak hasil analisis BFS"""
    print("="*60)
    print("HASIL ANALISIS GRAF MENGGUNAKAN BFS")
    print("="*60)
    
    # Tampilkan representasi graf
    g.display_graph()
    
            # BFS Tree
    print(f"1. BFS TREE (dari vertex '{start_vertex}'):")
    if start_vertex in g.vertices:
        bfs_edges, bfs_order, levels = g.bfs_tree(start_vertex)
        print(f"   Urutan traversal: {' -> '.join(bfs_order)}")
        print("   Tree edges:")
        if bfs_edges:
            for edge in bfs_edges:
                print(f"     {edge[0]} -> {edge[1]}")
        else:
            print("     (Tidak ada edges)")
        
        # Tampilkan level-level BFS
        print("   Level dalam BFS:")
        for level, vertices in sorted(levels.items()):
            if isinstance(vertices, list):
                print(f"     Level {level}: {', '.join(vertices)}")
            else:
                print(f"     Level {level}: {vertices}")
        
        # Visualisasi BFS Tree
        g.visualize_graph(f"BFS Tree dari vertex '{start_vertex}'", 
                         highlight_edges=bfs_edges, highlight_color='green',
                         highlight_levels=levels)
    else:
        print(f"   Vertex '{start_vertex}' tidak ditemukan dalam graf")
    print()
    
    # BFS Levels
    print(f"2. BFS LEVELS (dari vertex '{start_vertex}'):")
    if start_vertex in g.vertices:
        level_info = g.bfs_levels(start_vertex)
        if level_info:
            for level in sorted(level_info.keys()):
                print(f"   Level {level}: {', '.join(sorted(level_info[level]))}")
    print()
    
    # Shortest Path (contoh ke beberapa vertex)
    print(f"3. SHORTEST PATH dari '{start_vertex}':")
    if start_vertex in g.vertices:
        sample_vertices = [v for v in sorted(g.vertices) if v != start_vertex][:3]  # Ambil 3 vertex contoh
        for target in sample_vertices:
            path, distance = g.shortest_path_bfs(start_vertex, target)
            if path:
                print(f"   Ke '{target}': {' -> '.join(path)} (jarak: {distance})")
            else:
                print(f"   Ke '{target}': Tidak ada path")
    print()
    
    # Connected Components
    print("4. CONNECTED COMPONENTS:")
    components = g.connected_components_bfs()
    print(f"   Jumlah komponen: {len(components)}")
    for i, component in enumerate(components, 1):
        print(f"   Komponen {i}: {', '.join(component)}")
    print()
    
    # Visualisasi Graf Asli
    g.visualize_graph("Graf Asli")

def input_custom_graph():
    """Fungsi untuk input graf custom"""
    g = BFSGraph()
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
            print("Format salah! Gunakan format: u v")
    
    return g

def main():
    print("="*60)
    print("PROGRAM BFS (BREADTH-FIRST SEARCH)")
    print("="*60)
    print("Pastikan Anda sudah menginstall dependencies:")
    print("pip install networkx matplotlib")
    print("="*60)
    
    # Graf default dari soal
    default_edges = [
        ('a', 'b'), ('a', 'd'), ('a', 'e'),
        ('b', 'c'), ('b', 'd'),
        ('c', 'h'), ('c', 'g'),
        ('d', 'f'),
        ('e', 'd'), ('e', 'f'),
        ('f', 'j'),
        ('h', 'g'),
        ('i', 'g'), ('i', 'h')
    ]
    
    while True:
        print("\nMenu:")
        print("1. Gunakan graf default dari soal")
        print("2. Masukkan graf baru")
        print("3. Keluar")
        
        try:
            choice = int(input("Masukkan pilihan (1-3): "))
        except ValueError:
            print("Input tidak valid! Masukkan angka 1, 2, atau 3.")
            continue
        
        if choice == 3:
            print("Terima kasih telah menggunakan program BFS ini!")
            break
        
        elif choice == 1:
            # Gunakan graf default
            g = BFSGraph()
            print("\n" + "="*40)
            print("MENGGUNAKAN GRAF DEFAULT DARI SOAL")
            print("="*40)
            
            for u, v in default_edges:
                g.add_edge(u, v)
            
            print("Graf default berhasil dimuat!")
            print_bfs_results(g, 'a')
        
        elif choice == 2:
            # Input graf custom
            print("\n" + "="*40)
            print("INPUT GRAF BARU")
            print("="*40)
            
            g = input_custom_graph()
            
            if not g.vertices:
                print("Graf kosong! Kembali ke menu utama.")
                continue
            
            # Tanya vertex start
            print(f"\nVertex yang tersedia: {', '.join(sorted(g.vertices))}")
            start_vertex = input("Masukkan vertex start untuk BFS Tree (default: a): ").strip()
            if not start_vertex:
                start_vertex = 'a'
            
            print_bfs_results(g, start_vertex)
        
        else:
            print("Pilihan tidak valid! Masukkan angka 1, 2, atau 3.")

if __name__ == "__main__":
    main()
        