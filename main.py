from openpyxl import Workbook

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

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

    
    centralities = {}

    for x in nodes: #setup centralities dictionary
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

def saveCentralities(centralities)->None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Centralities"

    ws.cell(row=1, column=1, value="Building")
    ws.cell(row=1, column=2, value="Degree")
    ws.cell(row=1, column=3, value="Closeness")
    ws.cell(row=1, column=4, value="Betweenness")
    index = 2
    for x in list(centralities.keys()):
        ws.cell(row=index, column=1, value=x)
        ws.cell(row=index, column=2, value=centralities[x]['degree'])
        ws.cell(row=index, column=3, value=centralities[x]['closeness'])
        ws.cell(row=index, column=4, value=centralities[x]['betweenness'])
        index += 1

    wb.save("centralities.xlsx")

def determineOptimalPath(graph, startNode: str, nodes: list)->list:
    if startNode not in nodes:
        return [] #ensure startNode is part of nodes list

    currentNode = startNode
    nodes.pop(nodes.index(startNode)) #remove starting node from list

    path = [startNode]

    while len(nodes) > 0:
        shortest = ("", 9999)
        for x in nodes: #find nearest neighbor from currentNode
            length = nx.shortest_path_length(graph, currentNode, x, "weight")
            if length < shortest[1]:
                shortest = (x, length)
        nodes.pop(nodes.index(shortest[0]))

        add = nx.shortest_path(graph, currentNode, shortest[0], "weight")
        add.pop(0)

        path = path + add
        currentNode = shortest[0]

    return path

def main():
    graph = nx.Graph()

    edges = generateRelationships("relationships.txt")

    graph.add_edges_from(edges)
    #positions = nx.spring_layout(graph, k=5/math.sqrt(graph.order()))
    positions = nx.nx_agraph.graphviz_layout(graph, prog="neato")
    elabels = nx.get_edge_attributes(graph,'weight')

    test = ["Faura", "Berchman", "SEC-A", "Bellarmine"]
    print(determineOptimalPath(graph, "Faura", test))

    #print(nx.approximation.traveling_salesman_problem(graph, weight='weight'))

    '''centralities = getCentralities(graph)
    saveCentralities(centralities)''' #need only to run once

    plt.figure(1,figsize=(16,9)) #16:9 ratio

    nx.draw(graph, with_labels=True, node_size=4000, font_size="11", pos=positions)
    nx.draw_networkx_edge_labels(graph,positions,edge_labels=elabels, font_size="9")
    plt.show()

if __name__ == '__main__':
    main()