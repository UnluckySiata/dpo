
class Production:
    def __init__(self, L, K, R, labels):
        self.L = L
        self.K = K
        self.R = R
        self.labels = labels
        # te wierzchołki wraz z incydentnymi do nich krawędziami będą usuwane w dpo
        self.to_delete = [i for i in self.L[0] if i not in self.K[0]]
        self.to_add = [i for i in self.R[0] if i not in self.K[0]]

        edges_L = set()
        for i, v in enumerate(L[0]):
            for w in L[i + 1]:
                edges_L.add((v, w))
        edges_K = set()
        for i, v in enumerate(K[0]):
            for w in K[i + 1]:
                edges_K.add((v, w))
        edges_R = set()
        for i, v in enumerate(R[0]):
            for w in R[i + 1]:
                edges_R.add((v, w))

        # krawędzie grafu L\K
        self.obsolete_edges = list(edges_L - edges_K)
        # krawędzie grafu R\K
        self.new_edges = list(edges_R - edges_K)


# zdefiniowane produkcje
# dołożenie wierzchołka B i krawędzi A -> B
p0 = Production(((1,), ()), ((1,), ()), ((1, 2), (2,), ()), {1: "A", 2: "B"})
# dołożenie wierzchołków C i D oraz krawędzi B -> C i B -> D
p1 = Production(((1,), (), (), ()), ((1,), (), (), ()), ((1, 2, 3), (2, 3), (), ()), {1: "B", 2: "C", 3: "D"})

L = ((1, 2, 3), (2, 3), (), ())
K = ((1,), ())
R = ((1, 4), (4,), ())
labels = {
    1: "B",
    2: "C",
    3: "D",
    4: "E"
}
# "sklejenie" wierzchołków z poprzedniej produkcji w 1
p2 = Production(L, K, R, labels)

L = ((1, 2), (), ())
K = ((1, 2), (), ())
R = ((1, 2, 3), (3,), (3,), ())
labels = {
    1: "C",
    2: "D",
    3: "E"
}

# dołożenie wierzchołka E i krawędzi C -> E oraz D -> E
p3 = Production(L, K, R, labels)

L = ((1, 2, 3), (2, 3), (), (2,))
K = ((1, 2), (), ())
R = ((1, 2, 4, 5), (4, 5), (), (2,), (2,))
labels = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E"
}

px = Production(L, K, R, labels)

productions = [p0, p1, p2, p3, px]
