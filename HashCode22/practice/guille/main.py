import itertools


def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    potencial_clients = int(lines.pop(0).strip())

    clients = []
    for i in range(0, len(lines), 2):
        if lines[i].startswith("0"):
            likes = []
        else:
            likes = lines[i][2::].strip().split(" ")

        if lines[i + 1].startswith("0"):
            dislikes = []
        else:
            dislikes = lines[i + 1][2::].strip().split(" ")

        clients.append({'like': likes, 'dislike': dislikes})

    likes = list(itertools.chain(*[d['like'] for d in clients]))
    dislikes = list(itertools.chain(*[d['dislike'] for d in clients]))

    return potencial_clients, clients, likes, dislikes


def save(best_pizza, f):
    f = open(f.replace('in', 'out'), "w")
    f.write(str(len(best_pizza)) + " ")
    f.write(' '.join(best_pizza))
    f.close()


def process(potencial_clients, clients, likes, dislikes):
    print(f"Potenciales clientes: {potencial_clients}")
    print(f"Número de ingredientes distintos: {len(set(likes + dislikes))}")

    best_pizza = []
    not_like = {}
    for client in clients:
        for like in client['like']:
            if like not in best_pizza:
                best_pizza.append(like)
        for dislike in client['dislike']:
            if dislike in not_like.keys():
                not_like[dislike] = not_like[dislike] + 1
            else:
                not_like[dislike] = 1

    for ingredient in not_like.keys():
        if ingredient in best_pizza and not_like[ingredient]/potencial_clients > 0.4:
            best_pizza.remove(ingredient)
    return best_pizza


if __name__ == "__main__":
    files = ['../in/a_an_example.in.txt', '../in/b_basic.in.txt', '../in/c_coarse.in.txt', '../in/d_difficult.in.txt',
             '../in/e_elaborate.in.txt']
    for f in files:
        potencial_clients, clients, likes, dislikes = read_file(f)
        best_pizza = process(potencial_clients, clients, likes, dislikes)
        save(best_pizza, f)
