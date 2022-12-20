import pickle
from production import Production, productions
from graph import graphs, Graph
from visualization import draw, show_graphs, show_productions

def choose_graph(graphs):
    try:
        g = int(input(f"Wybierz graf spośród {list(range(len(graphs)))}: "))
        if g not in range(len(graphs)): return (False, -1)
        return (True, g)
    except Exception: return (False, -1)



def choose_production(productions):
    try:
        p = int(input(f"Wybierz produkcje spośród {list(range(len(productions)))}: "))
        if p not in range(len(productions)): return (False, -1)
        return (True, p)
    except Exception: return (False, -1)


def choose_vertices(G: Graph):
    vertices = []
    cond = True
    try:
        while cond:
            vertices = []
            p = input(f"Podaj indeksy wierzchołków (oddzielone spacją) na których chcesz wykonać produkcję: \n")
            for v in p.split(sep=" "):
                vertices.append(int(v))

            cond = False

            for v in vertices:
                if v not in G.active:
                    print("Podane wierzchołki nie stanowią podzbioru wierzchołków obecnie wybranego grafu")
                    cond = True
                    break

        return (True, vertices)
    except Exception: return (False, None)

def print_state(graph_index, production_index, vertices):
    result = f"""
STAN SYMULACJI
Graf początkowy: {"brak" if graph_index == -1 else f"g{graph_index}"}
Wybrane wierzchołki: {"brak" if len(vertices) == 0 else ", ".join(map(str, vertices))}
        """
    print(result)

def save_sequence(seq):
    
    filename = input("Podaj nazwę pliku, do którego chcesz zapisać sekwencję (bez rozszerzenia): ")

    try:
        with open(f"sequences/{filename}", "wb") as f:
            pickle.dump(seq, f)
    except Exception as e:
        print(e)

def print_sequence(seq):
    if len(seq) == 0:
        print("Pusta sekwencja")
        return

    result = f"\nObecna sekwencja produkcji z grafem początkowym g{seq[0]}:" 

    for i in range(1, len(seq)):
        result += f"\nProdukcja p{seq[i][0]} na {'wierzchołku' if len(seq[i][1]) == 1 else 'wierzchołkach'} {', '.join(map(str, seq[i][1]))}"

    print(result)

def produce_from_sequence(graphs: list[Graph], productions: list[Production], filename):
    seq = []
    try:
        with open(f"sequences/{filename}", "rb") as f:
            seq = pickle.load(f)
    except Exception:
        print(f"Nie udało się załadować sekwencji z pliku \"{filename}\"")
        return None
    G = graphs[seq[0]]

    for i in range(1, len(seq)):
        production_index, vertices = seq[i]
        G.transform(productions[production_index], vertices)

    return seq

def show_help():
    message = """
Możliwe akcje:
h - wyświetl możliwe akcje
g - wyświetl dostępne grafy początkowe
gw - wybierz graf spośród dostępnych
go - pokaż obecnie wybrany graf
v - wybierz wierzchołki do produkcji
p - wyświetl dostępne produkcje
pw - wykonaj produkcję
so - pokaż sekwencję produkcji wykonaną na obecnym grafie
ss - zapisz obecną sekwencję do pliku
sw - odtwórz sekwencję produkcji z pliku
q - zakończ działanie programu
"""
    print(message)


if __name__ == "__main__":
    graph_index = -1
    production_index = -1
    vertices = []
    run = True
    graph_chosen = False
    vertices_chosen = False
    production_chosen = False
    sequence = []

    show_help()
    while run:
        get_action = True
        print_state(graph_index, production_index, vertices)
        while get_action:
            get_action = False
            match input("Wybierz jedną z akcji: "):
                case "h": show_help()
                case "g": show_graphs()
                case "p": show_productions()
                case "v":
                    vertices_chosen = False
                    vertices = []
                    while not vertices_chosen:
                        if graph_index == -1 :
                            print("Najpierw wybierz graf, na którym chcesz wykonać produkcję")
                            break
                        vertices_chosen, vertices = choose_vertices(graphs[graph_index])

                case "gw":
                    graph_index = -1
                    graph_chosen = False
                    while not graph_chosen:
                        graph_chosen, graph_index = choose_graph(graphs)
                    sequence = [graph_index]

                case "go":
                    if not graph_chosen: print("Najpierw wybierz graf początkowy")
                    else: draw(graphs[graph_index].to_nx())
                case "pw":
                    match (graph_chosen, vertices_chosen):
                        case (False, False): print("Najpierw wybierz graf oraz jego wierzchołki, na których będzie wykonywana produkcja")
                        case (True, False): print("Najpierw wybierz wierzchołki do produkcji")
                        case (True, True):
                            production_chosen = False
                            production_index = -1
                            while not production_chosen:
                                production_chosen, production_index = choose_production(productions)

                            G = graphs[graph_index]
                            P = productions[production_index]
                            G.transform(P, vertices)
                            draw(G.to_nx())
                            sequence.append((production_index, vertices))
                            vertices = []

                case "so": print_sequence(sequence)
                case "ss": save_sequence(sequence)
                case "sw":
                    filename = input("Podaj nazwę pliku, z którego chcesz wczytać sekwencję: ")
                    loaded_sequence = produce_from_sequence(graphs, productions, filename)
                    if loaded_sequence is not None:
                        sequence = loaded_sequence
                        graph_index = loaded_sequence[0]
                        graph_chosen = True

                case "q": run = False
                case _: get_action = True
