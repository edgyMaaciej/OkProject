from math import sqrt,inf
import random
import time
import multiprocessing
import concurrent.futures
def randompick(distance,trail,tabu): #based on probability
    a,b = 1,13 #a=trail factor,b=distance factor
    probability = [] #numerical value of each city
    for i in (range(len(distance))):
        if i in tabu:
            probability.append(0)
        else:
            try:
                x = (trail[i]**a)*(distance[i]**(-b))
            except:
                x = inf
            probability.append(x)

    for i in range(1,len(distance)):
        probability[i]+=probability[i-1]

    pick = 0
    while(True):

        pick = 0
        pick_index = random.uniform(0,probability[-1])
        if(pick_index==probability[-1]):
            pick= len(distance)-1
        while pick_index > probability[pick]:
            pick+=1
        if(pick not in tabu):
            #blokada przed wpisaniem zlego miasta
            break
        if(len(tabu)==len(distance)-1):
            pick=probability[0]
            break
    return pick

def parallelpart(argss):
    list_of_distances = argss[0]
    list_of_visited_cities = argss[1]
    level_of_trail = argss[2]
    for i in range(len(list_of_distances)-1):
        current_city = list_of_visited_cities[-1]
        y = randompick(list_of_distances[current_city],level_of_trail[current_city],list_of_visited_cities)
        list_of_visited_cities.append(y)
    return list_of_visited_cities

def antcolony(graph):
    best_ant = inf
    start = time.time()
    MIN_LEN = inf
    MIN_PATH = []
    N = len(graph.matrix)
    ant_count = N
    percentage_best_ants=ant_count//10
    vapor_factor = 1.1
    trail = []
    delta_trail = []
    ants =[]
    for i in range(N):
        trail.append([])
        delta_trail.append([])
        for j in range(N):
            trail[i].append(1)
            delta_trail[i].append(0)
        ants.append(i)

    while(True): #limit to 3 minuty wiec bez fora
        index = 0
        LEN = []
        visited_cities = [[] for i in range(ant_count)]

        for k in range(ant_count):
            visited_cities[k].append(ants[k])
        argss = [ [ graph.matrix,visited_cities[ant],trail] for ant in range(ant_count)]
        with concurrent.futures.ProcessPoolExecutor() as pool:
             tmp = pool.map(parallelpart,argss)

        visited_cities = list(tmp)
        for ant in range(ant_count):
            visited_cities[ant].append(visited_cities[ant][0])
            LEN.append(sum( [ graph.matrix[ visited_cities[ant][i] ][visited_cities[ant][i+1]] for i in range(len(graph.matrix))]))
            if LEN[ant] <= LEN[index]:
                index = ant
        stack = []

        for i in range(ant_count):
            if LEN[i] < MIN_LEN:
                #print(MIN_LEN,MIN_PATH)
                MIN_LEN = LEN[i]
                MIN_PATH = visited_cities[i]

                if len(stack) < percentage_best_ants :
                    stack.append(i)
                else :
                    stack.pop(0)
                    stack.append(i)

        for ant in range(len(stack)):
            for i in range(N):
                delta_trail[visited_cities[stack[ant]][i]][visited_cities[stack[ant]][i+1]]+=(1/LEN[stack[ant]])

        for i in range(N) :
            for j in range(N):
                trail[i][j] = vapor_factor*trail[i][j] + delta_trail[i][j]


        if time.time() - start > 180:
            #print("minely 3 minuty i elo")
            break

        delta_trail = [[0 for i in range(N)] for j in range(N)]
    return MIN_LEN,MIN_PATH