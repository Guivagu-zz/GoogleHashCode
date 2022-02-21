
from read_file import read_file
from write_file import write_file
import graph_solution
import functools

def main():
    clients, ingredient_set = read_file()
    #print(clients)
    #print(ingredient_set)
    #worthwile_ingredient_set, removed_ingredients = poda_ingredientes_inicial(clients, ingredient_set)
    #worthwile_clients = poda_clientes_inicial(clients, removed_ingredients)
    #print("Managing " + str(len(worthwile_ingredient_set)) + " ingredients out of " + str(len(ingredient_set)))
    #print("Managing " + str(len(worthwile_clients)) + " clients out of " + str(len(clients)))
    #score, tastes = backtracking_wrapper(worthwile_clients, list(worthwile_ingredient_set))
    #score, tastes = take_all(worthwile_clients, worthwile_ingredient_set)
    score, tastes = satisfy_easier_clients(clients, ingredient_set)
    #client_graph = graph_solution.client_to_graph(clients)
    #graph_solution.print_graph(client_graph)
    #print("Graph created")
    #score, tastes = graph_solution.ingredients_by_independent_set(client_graph, clients)
    #print(score)
    #print(tastes)
    write_file(tastes)


def backtracking_wrapper(clients, ingredient_set):
    score_with, final_chosen_ingredients_with = backtracking(clients, ingredient_set, [ingredient_set[0]], 1, 0)
    score_without, final_chosen_ingredients_without = backtracking(clients, ingredient_set, [], 1, 0)
    return (score_with, final_chosen_ingredients_with) if score_with > score_without else (score_without, final_chosen_ingredients_without)

def backtracking(clients, ingredient_set, chosen_ingredients, position, partial_score):
    score = calculate_score(clients, chosen_ingredients)
    if position >= len(ingredient_set):
        return (score, chosen_ingredients)
    else:
        score_with, final_chosen_ingredients_with = backtracking(clients, ingredient_set, chosen_ingredients+[ingredient_set[position]], position+1, score)
        score_without, final_chosen_ingredients_without = backtracking(clients, ingredient_set, chosen_ingredients, position+1, score)
        #print(score_with, final_chosen_ingredients_with)
        #print(score_without, final_chosen_ingredients_without)
        return (score_with, final_chosen_ingredients_with) if score_with > score_without else (score_without, final_chosen_ingredients_without)

def take_all(clients, ingredient_set):
    return 0, ingredient_set;


def satisfy_easier_clients(clients, ingredient_set):
    ordered_clients = order_clients_by_satisfactory_easiness(clients)
    current_score = 0
    chosen_ingredients = []
    i = 0
    for client in ordered_clients:
        likes = client[0]
        for liked_ingredient in likes:
            partial_score = calculate_score(clients, chosen_ingredients+[liked_ingredient])
            if partial_score >= current_score:
                if liked_ingredient not in chosen_ingredients:
                    chosen_ingredients.append(liked_ingredient)
                current_score = partial_score
        i = i+1
        print(str(i) + "/" + str(len(ordered_clients)))
    return current_score, chosen_ingredients


def order_clients_by_satisfactory_easiness(clients):
    return sorted(clients, key=functools.cmp_to_key(client_compare))


def client_compare(client1, client2):
    likes1 = client1[0]
    dislikes1 = client1[1]
    likes2 = client2[0]
    dislikes2 = client2[1]
    if (len(dislikes1) < len(dislikes2)) or (len(dislikes1)==len(dislikes2) and len(likes1)<len(likes2)):
        return -1
    else:
        return 1

def calculate_score(clients, chosen_ingredients):
    score = 0
    for client in clients:
        requirement = True
        likes = client[0]
        dislikes = client[1]
        for like in likes:
            requirement = requirement and like in chosen_ingredients
        for dislike in dislikes:
            requirement = requirement and dislike not in chosen_ingredients
        if requirement:
            score = score+1
    return score


'''
Solo nos quedamos con aquellos ingredientes que nos ofrezcan 
más o igual potenciales clientes de los que nos quitan
'''
def poda_ingredientes_inicial(clients, ingredient_set):
    gusta = {}
    for ingredient in ingredient_set:
        for client in clients:
            likes = client[0]
            dislikes = client[1]
            if ingredient in likes:
                if ingredient in gusta:
                    gusta[ingredient] = gusta[ingredient] + 1
                else:
                    gusta[ingredient] = 1
            elif ingredient in dislikes:
                if ingredient in gusta:
                    gusta[ingredient] = gusta[ingredient] - 1
                else:
                    gusta[ingredient] = -1
    return [ingredient for ingredient, score in gusta.items() if score >= 0], [ingredient for ingredient, score in gusta.items() if score < 0]

'''
Como hemos rechazado ingredientes de primeras, aquellos clientes
que necesiten de alguno de los ingredientes rechazados nunca
seran satisfechos, asi que los eliminamos para ahorrar tiempo
'''
def poda_clientes_inicial(clients, removed_ingredients):
    worthwile_clients = []
    for client in clients:
        likes = client[0]
        requirement = True
        for ingredient in removed_ingredients:
            requirement = requirement and ingredient not in likes
        if requirement:
            worthwile_clients.append(client)
    return worthwile_clients

main()