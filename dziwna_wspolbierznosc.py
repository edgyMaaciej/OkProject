from math import sqrt,inf
import random
import time
import multiprocessing
import concurrent.futures
import numpy as np

def randompick(distance,trail,tabu): #based on probability
    a,b = 1,10 #a=trail factor,b=distance factor
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
    ant_count = argss[3]
    current_thread = argss[4]
    thread_counter = argss[5]

    # print([ i for i in range(current_thread*ant_count//thread_counter,((current_thread+1)*ant_count//thread_counter))])
    for i in range(len(list_of_distances) - 1):
        for ant in range(current_thread * ant_count // thread_counter,
                         ((current_thread + 1) * ant_count // thread_counter)):
            current_city = list_of_visited_cities[ant][-1]
            #print(i,ant,list_of_visited_cities[ant])
            y = randompick(list_of_distances[current_city], level_of_trail[current_city], list_of_visited_cities[ant])
            list_of_visited_cities[ant].append(y)
    list_of_visited_cities = list_of_visited_cities[current_thread * ant_count // thread_counter: (
                (current_thread + 1) * ant_count // thread_counter)]

    # print([i[0] for i in list_of_visited_cities])
    return list_of_visited_cities
def antcolony(graph):
    best_ant = inf
    start = time.time()
    MIN_LEN = inf
    MIN_PATH = []
    N = len(graph.matrix)
    ant_count = min(60,N)
    percentage_best_ants=ant_count//10
    vapor_factor = 0.7
    trail = []
    delta_trail = []
    ants =[]
    ThreadCount = 4
    for i in range(N):
        trail.append([])
        delta_trail.append([])
        for j in range(N):
            trail[i].append(1)
            delta_trail[i].append(0)
        ants.append(i)
    counter = 0
    while(True): #limit to 3 minuty wiec bez fora
        counter+=1
        index = 0
        LEN = []
        visited_cities = [[] for i in range(ant_count)]

        for k in range(ant_count):
            visited_cities[k].append(ants[k])
        """argss = [ [ graph.matrix,visited_cities[ant],trail] for ant in range(ant_count)]
        with concurrent.futures.ProcessPoolExecutor() as pool:
             tmp = pool.map(parallelpart,argss)"""
        """for i in range(N-1):
            for ant in range(ant_count):
                current_city = visited_cities[ant][-1]
                y = randompick(graph.matrix[current_city],trail[current_city],visited_cities[ant])
                visited_cities[ant].append(y)"""
        argss = [[graph.matrix, visited_cities, trail, ant_count, current_thread, ThreadCount] for
                 current_thread in range(ThreadCount)]
        with concurrent.futures.ProcessPoolExecutor() as pool:
            tmp = pool.map(parallelpart, argss)

        #visited_cities = list(tmp)
        visited_cities = []
        for t in list(tmp):
            visited_cities.extend(list(t))
        for ant in range(ant_count):
            visited_cities[ant].append(visited_cities[ant][0])
            LEN.append(sum( [ graph.matrix[ visited_cities[ant][i] ][visited_cities[ant][i+1]] for i in range(len(graph.matrix))]))
            if LEN[ant] <= LEN[index]:
                index = ant
        stack = []

        for i in range(ant_count):
            if LEN[i] < MIN_LEN:
                print(MIN_LEN)
                MIN_LEN = LEN[i]
                MIN_PATH = visited_cities[i]

            if len(stack) < percentage_best_ants :
                    stack.append(i)
            elif max([LEN[ant] for ant in stack]) > LEN[i]:
                index_of_ant = 0
                maxtmp = max([LEN[ant] for ant in stack])

                for id in stack:
                    if LEN[id] == maxtmp:
                        index_of_ant = id
                stack.remove(index_of_ant)
                stack.append(i)

        for ant in stack:
            for i in range(N):
                delta_trail[visited_cities[ant][i]][visited_cities[ant][i+1]]+=((100)/LEN[ant])

        for i in range(N) :
            for j in range(N):
                trail[i][j] = vapor_factor*trail[i][j] + delta_trail[i][j]

        print (MIN_LEN,np.amax(trail),len(stack))
        if time.time() - start > 180:
            #print("minely 3 minuty i elo")60
            break

        delta_trail = [[0 for i in range(N)] for j in range(N)]
    print(counter)
    return MIN_LEN,MIN_PATH
