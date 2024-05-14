import networkx as nx
import matplotlib.pyplot as plt

def generateRelationships(filename: str) -> str:
    edges = []

    with open(filename, "r") as file:
        lines = file.readlines()

        for x in lines:
            if x[0] == "\n" or x[0] == " " or x[0] == "/": #ignore whitespace and comments
                continue

            node = x.rstrip("\n").split(":")
            edges.append((node[0], node[1], {"weight": int(node[2])}))

    
    return edges

def getCentralities(graph) -> dict:
    nodes = list(graph.nodes)

    #setup centralities dictionary
    centralities = {}

    for x in nodes:
        centralities[x] = {"degree":0, "closeness":0, "betweenness":0}

    deg_centrality = nx.degree_centrality(graph)
    close_centrality = nx.closeness_centrality(graph)
    bet_centrality = nx.betweenness_centrality(graph)

    for x in list(deg_centrality.keys()):
        centralities[x]["degree"] = deg_centrality[x]

    for x in list(close_centrality.keys()):
        centralities[x]["closeness"] = close_centrality[x]

    for x in list(bet_centrality.keys()):
        centralities[x]["betweenness"] = bet_centrality[x]

    return centralities

def main():
    graph = nx.Graph()

    edges = generateRelationships("relationships.txt")

    #print(edges)
    graph.add_edges_from(edges)
    positions = nx.spring_layout(graph)
    elabels = nx.get_edge_attributes(graph,'weight')

    print(getCentralities(graph))

    nx.draw(graph, with_labels=True, node_size=1750, font_size="7", pos=positions)
    nx.draw_networkx_edge_labels(graph,positions,edge_labels=elabels)
    plt.show()

    


if __name__ == '__main__':
    main()