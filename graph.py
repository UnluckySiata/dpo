import networkx as nx
from production import Production

class Graph:
    def __init__(self, M: list[list[bool]], labels):
        self.M = M # macierz sąsiedztwa grafu skierowanego
        self.labels = labels # etykiety wierzchołków
        self.n = len(M) # całkowiny rozmiar macierzy
        self.active = [i for i in range(self.n)] # lista aktywnych wierzchołków indeksowanych tak jak w M

    # najpierw trzeba przeetykietować bo indeksy
    # w produkcji nie muszą być tożsame z grafowymi
    def remove(self, to_remove: list[int], obsolete_edges: list[tuple[int, int]], mapping):
        for v in to_remove:
            self.active.remove(mapping[v])
            self.M[mapping[v]] = [False for _ in range(len(self.M))]

            for line in self.M:
                line[mapping[v]] = False

        for e in obsolete_edges:
            M[mapping[e[0]]][mapping[e[1]]] = False

    def add(self, vertice_n: int, edges: list[tuple[int, int]], mapping):
        for i in range(vertice_n):
            for line in self.M: line.append(False)
            self.M.append([False for _ in range(vertice_n + len(self.M))])

            self.active.append(i + self.n)

        for e in edges:
            self.M[mapping[e[0]]][mapping[e[1]]] = True

        self.n = self.n + vertice_n


    def transform(self, p: Production, target_vertices: list[int]):

        # czy podgraf na tych wierzchołkach jest izomorficzny do L?
        #mapping = dict()
        mapping = {k: v for k in p.L[0] for v in target_vertices if self.labels[v] == p.labels[k]}
        """
        for v in target_vertices:
            for i, w in enumerate(p.L[0]):
                if w == 3 and v == 2:
                    print(i + 1)
                    print(p.L[i + 1])
                    print([self.M[v][x] for x in p.L[i + 1]])
                    print(self.labels[v] == p.labels[w])
                if all(self.M[v][x] for x in p.L[i + 1]) and self.labels[v] == p.labels[w]:
                    mapping[w] = v
        """

        if len(mapping) != len(target_vertices):
            print("Produkcja nie została wykonania przez błąd przypasowania lewej strony produkcji do grafu")
            return

        # czy produkcja może zostać wykonana?
        for v in p.to_delete:
            for a in self.active:
                if a not in target_vertices and (self.M[mapping[v]][a] or self.M[a][mapping[v]]):
                    print("Produkcja nie została wykonana, nie spełniony jest warunek sklejania - pozostawione zwisające krawędzie")
                    return

        self.remove(p.to_delete, p.obsolete_edges, mapping)

        # doklejenie grafu R\K
        new_mapping = {p.to_add[i]: i + self.n for i in range(len(p.to_add))}
        mapping.update(new_mapping)

        for k, v in new_mapping.items():

            # etykietowanie nowych wierzchołków
            self.labels[v] = p.labels[k]

        self.add(len(p.to_add), p.new_edges, mapping)

    def to_nx(self):
        NX = nx.DiGraph()
        nodes = []
        edges = [(v, w) for v in range(self.n) for w in range(self.n) if self.M[v][w]]

        for a in self.active:
            nodes.append((a, {"label": self.labels[a]}))


        NX.add_nodes_from(nodes)
        NX.add_edges_from(edges)

        return NX


# zdefiniowane grafy
g0 = Graph([[False]], {0: "A"})

M = [
        [False, True, True, True, False],
        [False, False, False, False, True],
        [False, True, False, False, False],
        [False,False, False, False,True],
        [False for _ in range(5)]
    ]

labels = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E"
}

g1 = Graph(M, labels)

graphs = [g0, g1]
