from GIT.GoogleHashCode21.Guille.graph import Graph
import math

def read_data(filename):
    f = open(filename, "r")
    lines = f.readlines()
    n_seconds = lines[0].split(' ')[0]
    n_intersec = int(lines[0].split(' ')[1])
    n_streets = int(lines[0].split(' ')[2])
    n_cars = int(lines[0].split(' ')[3])
    punt = int(lines[0].split(' ')[4].strip())

    streets = []
    for i in range(n_streets):
        l = lines[i+1].split(" ")
        ini = int(l[0])
        fin = int(l[1])
        name = l[2].strip()
        time = int(l[3].strip())
        streets.append((fin,ini,time,name))

    streets_graph = Graph(streets, True)

    cars = {}
    streets = {}
    for i in range(n_cars):
        l = lines[n_streets + i +1].strip().split(" ")
        car = {'n_streets': int(l[0]), 'streets': l[1:]}
        for street in car['streets']:
            if street in streets.keys():
                streets[street] = streets[street] + 1
            else:
                streets[street] = 1
        cars[i] = car

    return n_seconds, n_intersec, n_streets, n_cars, punt, streets_graph, cars, streets

def calc_num_magico(name, street_local):
    ciclo = 7
    num_total_coches = sum(street_local.values())
    num_coches_calle = street_local[name]
    r = num_coches_calle / num_total_coches
    return str(math.ceil(ciclo*r))

filename = "f.txt"
n_seconds, n_intersec, n_streets, n_cars, punt, streets_graph, cars, streets = read_data("../input/" + filename)

print("Hola")
schedule = ""
fout = open("../out/" + filename, 'w')
contador = 0
for nodo in streets_graph._graph.keys():
    if len(streets_graph._graph.get(nodo)) == 1:
        fout.write(str(nodo) + "\n" + "1" + "\n" + str(streets_graph._graph.get(nodo).pop()[2]) + " 1\n")
        contador += 1
    else:
        street_local = {}
        for (ini, time, name) in streets_graph._graph.get(nodo):
            if name in streets:
                street_local[name] = streets[name]
        street_local = dict(sorted(street_local.items(), key=lambda item: item[1], reverse=True))
        if len(street_local) > 0:
            fout.write(str(nodo) + "\n" + str(len(street_local)) + "\n")
            contador += 1
        for (ini, time, name) in streets_graph._graph.get(nodo):
            if name in street_local:
                fout.write(str(name) + " " + calc_num_magico(name, street_local) + "\n");
fout.close()
f = open("../out/" + filename, 'r')
lines = f.readlines()
fout = open("../out/" + filename, 'w')
fout.write(str(contador) + "\n")
for line in lines:
    fout.write(line)
fout.close()

