from math import sqrt,inf
import random
import time

def randompick(distance,trail,tabu): #based on probability
    a,b = 1,10 #a=trail factor,b=distance factor
    score = [] #numerical value of each city
    for i in (range(len(distance))):
        if i in tabu:
            score.append(0)
        else:
            x = (trail[i]**a)*(distance[i]**(-b))
            score.append(x)

    probability = [score[i] / sum(score) for i in range(len(distance))]
    for i in range(1,len(distance)):
        probability[i]+=probability[i-1]
    probability = [round(x,7) for x in probability]
    pick_index = random.uniform(0,1)
    pick = 0 #the city we chooose
    while pick_index >  probability[pick]:
        pick+=1
    return pick


def antcolony(graph):
    start = time.time()
    NC = 100
    MIN_LEN = inf
    MIN_PATH = []
    counter = 0 #to break out of the loop if no progress is noticed
    N = len(graph.matrix)
    ant_count = min(15,N) #probably not the best solution,for testing
    vapor_factor = 0.7
    trail = [[1 for i in range(N)] for j in range(N)]
    delta_trail = [[0 for i in range(N)] for j in range(N)]
    ants = [i for i in range(N)]
    for trials in range(NC):
        index = 0
        flag = False
        LEN = []
        visited_cities = [[] for i in range(ant_count)]

        for k in range(ant_count):
            visited_cities[k].append(ants[k])
        for times in range(N-1):
            for ant in range(ant_count):
                i = visited_cities[ant][-1]
                y = randompick(graph.matrix[i],trail[ant],visited_cities[ant])
                visited_cities[ant].append(y)
        for ant in range(ant_count):
            visited_cities[ant].append(visited_cities[ant][0])
            LEN.append(sum( [ graph.matrix[ visited_cities[ant][i] ][visited_cities[ant][i+1]] for i in range(len(graph.matrix))]))
            if LEN[ant] <= LEN[index]:
                index = ant

            for i in range(N):
                delta_trail[visited_cities[ant][i]][visited_cities[ant][i+1]]+=(1/LEN[ant])



        for i in range(ant_count):
            if LEN[i] < MIN_LEN:
                MIN_LEN = LEN[i]
                MIN_PATH = visited_cities[i]
                flag = True
                counter = 0



        for i in range(N) :
            for j in range(N):
                trail[i][j] = vapor_factor*trail[i][j] + delta_trail[i][j]
        if not(flag):
            counter+=1
        if counter > NC*0.7:
            break
        if time.time() - start > 600:
            break

        delta_trail = [[0 for i in range(N)] for j in range(N)]

        #print(MIN_LEN)
    return MIN_LEN,MIN_PATH




