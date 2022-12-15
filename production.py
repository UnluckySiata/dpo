
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

p1 = Production(L, K, R, labels)

productions = [p1]
