import networkx as nx
import matplotlib.pyplot as plt

def client_to_graph(clients):
    G = nx.Graph()
    i = 0
    for client in clients:
        G.add_node(i)
        i += 1
    i = 0
    for client1 in clients:
        for j in range(i+1, len(clients)):
            client2 = clients[j]
            likes1 = client1[0]
            dislikes1 = client1[1]
            likes2 = client2[0]
            dislikes2 = client2[1]
            incompatible = False
            for like in likes1:
                incompatible = incompatible or like in dislikes2
            for like in likes2:
                incompatible = incompatible or like in dislikes1
            if incompatible and not G.has_edge(i, j):
                G.add_edge(i, j)
        i += 1
        print(str(i) + "/" + str(len(clients)))
    return G


def print_graph(graph):
    nx.draw(graph)
    plt.savefig("grafo.png")


def ingredients_by_independent_set(client_graph, clients):
    client_numbers = nx.maximal_independent_set(client_graph)
    print("Maximum independent set found")
    print(client_numbers)
    chosen_ingredients = []
    for index in client_numbers:
        client = clients[index]
        for like in client[0]:
            if like not in chosen_ingredients:
                chosen_ingredients.append(like)
    return 0, chosen_ingredients
