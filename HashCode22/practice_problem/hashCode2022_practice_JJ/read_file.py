import os
import shutil


filepath = 'e_elaborate.in.txt'

def read_file():
    clients = []
    ingredient_set = set()
    with open(filepath, 'r') as f:
        num_clients = int(f.readline())
        for i in range(0, num_clients):
            client_tastes = []
            like_line = f.readline().replace('\n','')
            dislike_line = f.readline().replace('\n','')
            ingredients_liked = like_line.split(" ")[1:]
            ingredients_disliked = dislike_line.split(" ")[1:]
            client_tastes.append([ingredient for ingredient in ingredients_liked])
            client_tastes.append([ingredient for ingredient in ingredients_disliked])
            clients.append(client_tastes)
            for ingredient in ingredients_liked:
                ingredient_set.add(ingredient)
    return (clients, ingredient_set)