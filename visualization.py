import networkx as nx
import matplotlib.pyplot as plt

color_map = {
    "A": "red",
    "B": "yellow",
    "C": "orange",
    "D": "green",
    "E": "blue"
}

def draw(NX):
    labels = dict()
    attributes = nx.get_node_attributes(NX, "label")
    colors = []
    for node in NX.nodes():
        #labels[node] = f"{node} {attributes[node]}"
        labels[node] = node
        colors.append(color_map[attributes[node]])

    pos = nx.planar_layout(NX)
    nx.draw(NX, pos , node_color = colors, alpha=0.5)
    nx.draw_networkx_labels(NX, pos, labels=labels)
    plt.show()
