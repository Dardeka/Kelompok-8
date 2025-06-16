import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])
    
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
    def kruskal_mst(self, visualize=False):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = {}
        rank = {}
        for u, v, w in self.graph:
            parent[u] = u
            parent[v] = v
            rank[u] = 0
            rank[v] = 0
        
        while e < self.V - 1:
            if i >= len(self.graph):
                break
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            
            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
        
        print("\nKruskal's MST:")
        total_weight = 0
        for u, v, weight in result:
            print(f"{u} -- {v} == {weight}")
            total_weight += weight
        print(f"Total weight: {total_weight}\n")
        if visualize:
            draw_graph(self.graph, "Original Graph (Kruskal)")
            draw_graph(result, "Kruskal's MST")
    
    #Algoritma Prim
    def prim_mst(self, start_vertex, visualize=False):
        mst_set = set()
        min_heap = []
        total_weight = 0
        mst_edges = []

        adj = {}
        for u, v, w in self.graph:
            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))

        mst_set.add(start_vertex)
        for v, w in adj[start_vertex]:
            heapq.heappush(min_heap, (w, start_vertex, v))

        print(f"Prim's MST (starting from vertex '{start_vertex}'):")
        while min_heap and len(mst_set) < self.V:
            w, u, v = heapq.heappop(min_heap)
            if v not in mst_set:
                mst_set.add(v)
                total_weight += w
                mst_edges.append((u, v, w))
                for to, weight in adj[v]:
                    if to not in mst_set:
                        heapq.heappush(min_heap, (weight, v, to))

        for u, v, w in mst_edges:
            print(f"{u} -- {v} == {w}")
        print(f"Total weight: {total_weight}\n")
        if visualize:
            draw_graph(self.graph, "Original Graph (Prim)")
            draw_graph(mst_edges, f"Prim's MST (start: {start_vertex})")

def create_graph_from_input():
    vertices = input("\nMasukkan vertex (pisahkan dengan spasi, contoh: A B C D): ").split()
    vertices = [v.upper() for v in vertices]
    g = Graph(len(vertices))
    
    print("\nMasukkan edge dan beratnya (format: u v w), ketik 'done' jika selesai:")
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
            print("Berat edge (w) harus berupa angka! (contoh: A B 5)")
            continue
    return g

def draw_graph(graph_edges, title="Graph"):
    G = nx.Graph()
    for u, v, w in graph_edges:
        G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()

def main():    
    #graf default
    g_default = Graph(11)
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
        elif choice == '2':
            g = create_graph_from_input()
        elif choice == '3':
            break
        else:
            print("Pilihan tidak valid!")
            continue
        
        g.kruskal_mst(visualize=True)
        start_vertex = input("Masukkan start vertex untuk Prim's MST: ").upper()
        g.prim_mst(start_vertex, visualize=True)

if __name__ == "__main__":
    main()
