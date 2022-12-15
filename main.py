from production import productions
from graph import graphs
from visualization import draw

# TODO: prawdziwe TUI
if __name__ == "__main__":

    need_graph = True
    G = graphs[0]
    while need_graph:
        try:
            g = int(input(f"Wybierz graf spośród {list(range(len(graphs)))}: "))
            G = graphs[g]
            need_graph = False
        except Exception:
            pass

    draw(G.to_nx())

    P = productions[0]
    run = True
    while run:
        need_production = True
        while need_production:
            try:
                p = int(input(f"Wybierz produkcje spośród {list(range(len(productions)))}: "))
                P = productions[p]
                need_production = False
            except Exception:
                pass

        need_vertices = True
        vertices = []
        while need_vertices:
            vertices = []
            try:
                p = input(f"Podaj indeksy wierzchołków (oddzielone spacją) na których chcesz wykonać produkcję: \n")
                for v in p.split(sep=" "):
                    vertices.append(int(v))
                need_vertices = False
            except Exception:
                pass

        G.transform(P, vertices)
        #for i in G.active:
            #print(G.M[i])
        draw(G.to_nx())

        confirm = True
        while confirm:
            d = input("Kontynuować? [t/n] ")

            if d == 't':
                confirm = False
                run = True
            elif d == 'n':
                confirm = False
                run = False
