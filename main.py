from create_alphabet import create_matrix_from_file,save_matrix_to_file,create_sigma
from create_D import create_D
from scheduler import scheduler
from graphviz import Digraph
import os


#znajdowanie pierwszej warstwy - czyli warstwy wszystkich wierzchołkow ktore nie maja parentow 
def find_first_fnf_layer(edges):

    def has_parent(node):
        for u,v in edges:
            if v == node:
                return True
        return False
    
    layer = []
    for u,v in edges:
        if not has_parent(u) and u not in layer:
            layer.append(u)

    return layer

#znaleziennie wszystkich wierzcholkow w grafie
def find_all_nodes(edges):
    nodes = []
    for u,v in edges:
        if u not in nodes:
            nodes.append(u)
        if v not in nodes:
            nodes.append(v)

    return nodes


def find_FNF(edges):
    #funkcja pomocnicza do dodania krawędzi (ostatni_node, None)
    def add_last_edges():
        for node in nodes:
            flag = True
            for u,v in edges:
                if node == u:
                    flag = False
            if flag:
                edges.append([node,None])

    fnf = []
    nodes = find_all_nodes(edges)
    add_last_edges()
    #algorytm znajdowania fnf z grafu 
    #bierzemy pierwszą warstwę
    current_fnf_layer = find_first_fnf_layer(edges)

    #dopoki mamy warstwe
    while current_fnf_layer:
        #dodajemy warstwe do fnf
        fnf.append(current_fnf_layer)
        
        #usuwamy krawedzie pomiedzy wezlami naszej warstwy a kolejnymi
        edges = [(u, v) for u, v in edges if u not in current_fnf_layer]

        #znajdujemy kolejna warstwe - przez to ze usunelismy krawedzie, mozemy wykorzystac 
        #znajdowanie wierzchołków bez parentó 
        current_fnf_layer = find_first_fnf_layer(edges)

    return fnf

#funkcja pomocnicza usuwajaca wczesniej zdefiniowane wierzchołki końcowe
def remove_last_edges(edges):
    to_del = []
    for u,v in edges:
        if not v:
            to_del.append([u,v])

    for u,v in to_del:
        edges.remove([u,v])

#rysowanie grafu dickerta
def draw_dickert_graph_with_layers(edges, layers):

    def create_label(node):
        return f"{node[0]}{''.join(map(str, node[1:]))}"

    remove_last_edges(edges)

    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan","grey"]

    graph = Digraph(format='png')

    #kolorowanie wezlow
    for i, layer in enumerate(layers):
        #każda warstwa ma inny kolor
        color = colors[i % len(colors)] 
        for node in layer:
            label = create_label(node)
            graph.node(label, style="filled", fillcolor=color)

    #narysowanie krawedzi
    for edge in edges:
        start = create_label(edge[0])
        end = create_label(edge[1])
        graph.edge(start, end)

    graph.render("dickert_graph_colored", view=True)

def create_ident_matrix(M):
    rows = len(M)
    cols = len(M[0])

    for i in range(rows):
        # normalizacja wiersza zeby glowny element byl rowny 1
        divisor = M[i][i]
        for k in range(cols):
            M[i][k] /= divisor

        # wyzerowanie wszystkich innych elementow 
        for j in range(rows):
            if i != j:
                factor = M[j][i]
                for k in range(cols):
                    M[j][k] -= factor * M[i][k]

    return matrix


file_path = 'ex2.txt'


matrix = create_matrix_from_file(os.path.join("examples",file_path))
sigma = create_sigma(matrix)

print(f'Alfabet: {sigma}\n')

edges,D,I = create_D(sigma)

print(f'Relacja zaleznosci: {D}\n')
print(f'Postac normalna Foaty:')

fnf = find_FNF(edges)

for layer in fnf:
    print(layer)

draw_dickert_graph_with_layers(edges,fnf)

gauss = scheduler(fnf,matrix)

matrix_ident = create_ident_matrix(gauss)

save_matrix_to_file(os.path.join("results",file_path),matrix_ident)
