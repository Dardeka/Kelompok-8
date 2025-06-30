import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from collections import defaultdict

class Graph:
    def __init__(self, vertices_count=0):
        self.V = vertices_count
        self.graph = []
        self.vertices_set = set()

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])
        self.vertices_set.add(u)
        self.vertices_set.add(v)
        self.V = len(self.vertices_set)

    def find(self, parent, i): 
        if parent[i] != i: 
            parent[i] = self.find(parent, parent[i]) 
        return parent[i]
    
    def union(self, parent, rank, x, y):        
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1
    
    # Algoritma Kruskal
    def kruskal_mst(self):
        steps = []
        result_edges = []
        total_weight = 0

        sorted_graph = sorted(self.graph, key=lambda item: item[2])
        
        parent = {vertex: vertex for vertex in self.vertices_set}
        rank = {vertex: 0 for vertex in self.vertices_set}

        steps.append({
            "title": "Algoritma Kruskal",
            "mst_edges": [],
            "considered_edge": None,
            "total_weight": 0
        })

        for u, v, w in sorted_graph:
            steps.append({
                "title": "Algoritma Kruskal",
                "sub_title": f"Mempertimbangkan edge ({u}, {v}) dengan bobot {w}",
                "mst_edges": [tuple(edge) for edge in result_edges], 
                "considered_edge": (u, v, w),
                "total_weight": total_weight
            })

            root_u = self.find(parent, u)
            root_v = self.find(parent, v)

            if root_u != root_v:
                self.union(parent, rank, root_u, root_v)
                result_edges.append([u, v, w])
                total_weight += w
                
                steps.append({
                    "title": "Algoritma Kruskal",
                    "sub_title": f"Edge ({u}, {v}) ditambahkan ke MST",
                    "mst_edges": [tuple(edge) for edge in result_edges],
                    "considered_edge": None,
                    "total_weight": total_weight
                })
            else:
                steps.append({
                    "title": "Algoritma Kruskal",
                    "sub_title": f"Edge ({u}, {v}) ditolak karena membentuk siklus",
                    "mst_edges": [tuple(edge) for edge in result_edges],
                    "considered_edge": None,
                    "total_weight": total_weight
                })
        
        print("\n=== HASIL KRUSKAL ===")
        print("Edge dalam MST:")
        for u, v, w in result_edges:
            print(f"  ({u}, {v}) = {w}")
        print(f"Total bobot MST: {total_weight}")
        print("=" * 25)
        
        steps.append({
            "title": "Hasil MST dengan Algoritma Kruskal",
            "sub_title": f"Total Bobot MST: {total_weight}",
            "mst_edges": [tuple(edge) for edge in result_edges],
            "considered_edge": None,
            "total_weight": total_weight
        })
        return steps
    
    # Algoritma Prim
    def prim_mst(self, start_vertex):
        steps = []
        mst_set = set()
        min_heap = []
        total_weight = 0
        mst_edges = []

        adj = defaultdict(list)
        for u, v, w in self.graph:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        if start_vertex not in self.vertices_set:
            print(f"Error: Start vertex '{start_vertex}' tidak ditemukan pada graph untuk Prim.")
            return steps

        steps.append({
            "title": f"Algoritma Prim - Mulai dari verteks {start_vertex}",
            "mst_edges": [],
            "visited_nodes": [start_vertex],
            "considered_edge": None,
            "total_weight": 0
        })

        mst_set.add(start_vertex)
        for v, w in adj[start_vertex]:
            heapq.heappush(min_heap, (w, start_vertex, v))

        while min_heap and len(mst_set) < len(self.vertices_set):
            w, u, v = heapq.heappop(min_heap)
            
            steps.append({
                "title": "Algoritma Prim",
                "sub_title": f"Mempertimbangkan edge ({u}, {v}) dengan bobot {w}",
                "mst_edges": [tuple(edge) for edge in mst_edges],
                "visited_nodes": list(mst_set),
                "considered_edge": (u, v, w),
                "total_weight": total_weight
            })

            if v in mst_set:
                steps.append({
                    "title": "Algoritma Prim",
                    "sub_title": f"Edge ({u}, {v}) ditolak karena membentuk siklus",
                    "mst_edges": [tuple(edge) for edge in mst_edges],
                    "visited_nodes": list(mst_set),
                    "considered_edge": None, # No longer considered, it's rejected
                    "total_weight": total_weight
                })
                continue
            
            mst_set.add(v)
            total_weight += w
            mst_edges.append((u, v, w))

            steps.append({
                "title": "Algoritma Prim",
                "sub_title": f"Edge ({u}, {v}) ditambahkan ke MST",
                "mst_edges": [tuple(edge) for edge in mst_edges],
                "visited_nodes": list(mst_set),
                "considered_edge": None,
                "total_weight": total_weight
            })

            for to, weight in adj[v]:
                if to not in mst_set:
                    heapq.heappush(min_heap, (weight, v, to))
        
        print(f"\n=== HASIL PRIM (dari vertex {start_vertex}) ===")
        print("Edge dalam MST:")
        for u, v, w in mst_edges:
            print(f"  ({u}, {v}) = {w}")
        print(f"Total bobot MST: {total_weight}")
        print("=" * 25)
        
        steps.append({
            "title": "Hasil MST dengan Algoritma Prim",
            "sub_title": f"Total Bobot MST: {total_weight}",
            "mst_edges": [tuple(edge) for edge in mst_edges],
            "visited_nodes": list(mst_set),
            "considered_edge": None,
            "total_weight": total_weight
        })
        return steps

class MST_Visualizer:
    def __init__(self, graph_obj, initial_prim_vertex=None):
        self.graph_obj = graph_obj
        
        self.G = nx.Graph()
        for u, v, w in self.graph_obj.graph:
            self.G.add_edge(u, v, weight=w)
        
        self.pos = nx.spring_layout(self.G, seed=41) 

        # Pengaturan gambar
        plt.ion() 
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.2)

        # Menentukan sumbu tombol
        self.prev_ax = plt.axes([0.6, 0.05, 0.1, 0.075])
        self.next_ax = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.method_ax = plt.axes([0.3, 0.05, 0.2, 0.075])

        # Membuat buttons
        self.prev_button = Button(self.prev_ax, 'Previous', color='lightblue', hovercolor='deepskyblue')
        self.next_button = Button(self.next_ax, 'Next', color='lightblue', hovercolor='deepskyblue')
        self.method_button = Button(self.method_ax, 'Switch Algoritma', color='lightgreen', hovercolor='limegreen')

        # Menghubungkan button events ke metode
        self.prev_button.on_clicked(self.prev_step)
        self.next_button.on_clicked(self.next_step)
        self.method_button.on_clicked(self.switch_algoritma)

        # Inisialisasi status algoritma
        self.current_algoritma = "Kruskal"
        self.steps_kruskal = self.graph_obj.kruskal_mst()

        self.steps_prim = []
        if initial_prim_vertex and initial_prim_vertex in self.graph_obj.vertices_set: #
            self.steps_prim = self.graph_obj.prim_mst(initial_prim_vertex) #
        elif self.graph_obj.vertices_set: #
            fallback_vertex = next(iter(self.graph_obj.vertices_set)) #
            print(f"Warning: Verteks awal Prim tidak valid atau tidak diberikan. Menggunakan '{fallback_vertex}' sebagai gantinya.")
            self.steps_prim = self.graph_obj.prim_mst(fallback_vertex) #
        else: 
            print("Tidak ada verteks dalam graf. Prim's MST tidak dapat dihitung.")

        self.current_step = 0 if self.steps_kruskal else -1
        self.update_figure()

    def prev_step(self, event):
        steps = self.steps_kruskal if self.current_algoritma == "Kruskal" else self.steps_prim
        if steps and self.current_step > 0:
            self.current_step -= 1
            self.update_figure()

    def next_step(self, event):
        steps = self.steps_kruskal if self.current_algoritma == "Kruskal" else self.steps_prim
        if steps and self.current_step < len(steps) - 1:
            self.current_step += 1
            self.update_figure()

    def switch_algoritma(self, event):
        if self.current_algoritma == "Kruskal":
            if self.steps_prim: 
                self.current_algoritma = "Prim"
                self.current_step = 0
                self.update_figure()
            else:
                print("Vertex awal untuk Prim belum diatur. Silakan atur vertex awal untuk Prim.")
        else:
            self.current_algoritma = "Kruskal"
            self.current_step = 0
            self.update_figure()

    def update_figure(self):
        self.ax.clear() 
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        steps = self.steps_kruskal if self.current_algoritma == "Kruskal" else self.steps_prim

        if not steps or self.current_step < 0 or self.current_step >= len(steps):
            self.ax.set_title("Tidak ada langkah tersedia atau graf kosong.")
            self.fig.canvas.draw_idle()
            return

        step = steps[self.current_step]

        nx.draw_networkx_nodes(self.G, self.pos, node_color='orange', node_size=800, ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax)

        all_edges = [(u, v) for u, v, _ in self.graph_obj.graph]
        nx.draw_networkx_edges(self.G, self.pos, edgelist=all_edges, edge_color='black', width=1, ax=self.ax)

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        # Highlight sisi MST dengan warna merah
        if step["mst_edges"]:
            mst_edges_tuple_list = [(u, v) for u, v, w in step["mst_edges"]]
            nx.draw_networkx_edges(self.G, self.pos, edgelist=mst_edges_tuple_list, width=3, edge_color='red', ax=self.ax)

        # Highlight pertimbangan sisi dengan warna yellow
        if step["considered_edge"]:
            u, v, w = step["considered_edge"]
            nx.draw_networkx_edges(self.G, self.pos, edgelist=[(u, v)], width=3, edge_color='yellow', ax=self.ax)

        # Highlight node yang sudah dikunjungi untuk algoritma prim
        if self.current_algoritma == "Prim" and "visited_nodes" in step:
            valid_visited = [node for node in step["visited_nodes"] if node in self.pos]
            if valid_visited:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=valid_visited,
                                      node_color='blue', node_size=800, ax=self.ax)

        # Set title, sub title dan langkahnya
        self.ax.set_title(f"{step['title']}\n{step.get('sub_title', '')}", pad=15)
        self.ax.text(0.95, 0.05, f"Step {self.current_step + 1}/{len(steps)}",
                     transform=self.ax.transAxes, ha='right', va='bottom', fontsize=9, color='gray')

        # Update button text
        self.method_button.label.set_text("Switch Prim" if self.current_algoritma == "Kruskal" else "Switch Kruskal")
        self.fig.canvas.draw_idle() 

def create_graph_from_input():
    g = Graph()
    
    print("\nMasukkan verteks (pisahkan dengan spasi, contoh: A B C D): ")
    vertices_input = input().split()
    for v in vertices_input:
        g.vertices_set.add(v.upper())
    
    print(f"{len(g.vertices_set)} vertices ditambahkan: {sorted(g.vertices_set)}")

    print("\nMasukkan edge dan beratnya (format: u v w), ketik 'done' jika selesai:")
    edge_count = 0
    while True:
        edge_input = input("Edge: ")
        if edge_input.lower() == 'done':
            break
        parts = edge_input.split()
        if len(parts) != 3:
            print("Format salah! Masukkan dengan spasi (contoh: A B 5)")
            continue
        u, v, w = parts
        try:
            g.add_edge(u.upper(), v.upper(), int(w))
        except ValueError:
            print("Berat sisi (w) harus berupa angka! (contoh: A B 5)")
            continue
    
    print(f"\nTotal {edge_count} edges berhasil ditambahkan")
    return g

def main():    
    # Default graph dari soal
    g_default = Graph() 
    g_default.add_edge('A', 'V1', 4)
    g_default.add_edge('A', 'V3', 14)
    g_default.add_edge('V1', 'V2', 4)
    g_default.add_edge('V1', 'V4', 20)
    g_default.add_edge('V2', 'V3', 7)
    g_default.add_edge('V2', 'V5', 9)
    g_default.add_edge('V3', 'V6', 12)
    g_default.add_edge('V4', 'V5', 11)
    g_default.add_edge('V4', 'V7', 15)
    g_default.add_edge('V4', 'V8', 7)
    g_default.add_edge('V5', 'V6', 8)
    g_default.add_edge('V6', 'V7', 11)
    g_default.add_edge('V7', 'V8', 7)
    g_default.add_edge('V7', 'V9', 4)
    g_default.add_edge('V8', 'V9', 5)
    g_default.add_edge('V8', 'B', 7)
    g_default.add_edge('V9', 'B', 3)

    while True:
        print("------------------------------------")
        print("Program MST dengan Kruskal dan Prim")
        print("------------------------------------")
        print("Menu:")
        print("1. Gunakan graf default dari soal")
        print("2. Masukkan graf baru")
        print("3. Keluar")
        print("------------------------------------")
        choice = input("Pilihan: ")
        
        if choice == '1':
            g = g_default
            print("\nMenggunakan graf default dari soal")
            print(f"Graf memiliki {len(g.vertices_set)} vertices dan {len(g.graph)} edges")
        elif choice == '2':
            print("\nMembuat graf baru...")
            g = create_graph_from_input()
            print(f"\nGraf berhasil dibuat dengan {len(g.vertices_set)} vertices dan {len(g.graph)} edges")
        elif choice == '3':
            break
        else:
            print("Pilihan tidak valid!")
            continue
        
        # Memeriksa apakah graf memiliki verteks
        if not g.vertices_set:
            print("Tidak ada verteks dalam graf. Kembali ke menu utama.")
            continue

        start_vertex_input = None
        if g.vertices_set: 
            print(f"\nVertices tersedia: {sorted(g.vertices_set)}")
            start_vertex_input = input("Masukkan start verteks untuk Prim's MST: ").upper()
            if not start_vertex_input: 
                start_vertex_input = next(iter(g.vertices_set)) 
                print(f"Vertex awal Prim diatur secara otomatis ke: {start_vertex_input}")
            elif start_vertex_input not in g.vertices_set:
                print(f"Vertex '{start_vertex_input}' tidak ditemukan dalam graf.")
                start_vertex_input = next(iter(g.vertices_set))
                print(f"Menggunakan verteks '{start_vertex_input}' sebagai awal untuk Prim.")
            else:
                print(f"Vertex awal Prim: {start_vertex_input}")

        visualizer = MST_Visualizer(g, initial_prim_vertex=start_vertex_input)
        
        print(f"\nVisualisasi interaktif dimulai!")
        print(f"Gunakan tombol 'Previous' dan 'Next' untuk navigasi langkah")
        print(f"Gunakan tombol 'Switch Algoritma' untuk beralih antara Kruskal dan Prim")
        print(f"Tutup jendela visualisasi untuk kembali ke menu\n") 

        plt.ioff() 
        plt.show()

if __name__ == "__main__":
    main()