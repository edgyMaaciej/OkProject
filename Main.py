from math import sqrt
from multiprocessing import freeze_support

import zachlanne
import TSP_concurrent
def printResults(greedySol, AcoSol):
    print("Algorytm zachłanny: \n" + str(greedySol) + "\n")
    print("Ant Colony Optimization: \n" + str(AcoSol) + "\n")
    jakosc = "Algorytm ACO okazał się lepszy o " + str(
        qualityComparedToGreedy(greedySol[0], AcoSol[0])) + "% względem algorytmu zachłannego"
    print(jakosc)
def qualityComparedToGreedy(greedyLen, AcoLen):
    return round((greedyLen*100/AcoLen)-100,2)

def distance(x1, x2, y1, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class Graph:
    def __init__(self,n,points): #constructor
        self.matrix = [[0 for i in range(n)] for j in range(n)] #adjacency matrix
        for i in range(len(points)): #we fill our matrix with the distances
            #[p, x, y,] = points[i].split(' ')
            kkk = points[i].split(' ')
            p = kkk[0]
            x = kkk[1]
            y = kkk[2]
            p, x, y = int(p)-1, int(x), int(y)
            for j in range(i, len(points)):
                #[p1, x1, y1] = points[j].split(' ')
                kkk = points[j].split(' ')
                p1 = kkk[0]
                x1 = kkk[1]
                y1 = kkk[2]
                p1, x1, y1 = int(p1)-1, int(x1), int(y1)
                self.matrix[p][p1] = self.matrix[p1][p] = distance(x, x1, y, y1)

if __name__ == '__main__':
    contents = open("berlin52.txt", "r").readlines() #load data
    i=0
    while i<5:
        if(i==0):
            contents = open("berlin52.txt", "r").readlines()  # load data
            print("wyniki dla berlin52:")
        if(i==1):
            contents = open("bier127.txt", "r").readlines()  # load data
            print("wyniki dla bier127:")
        if (i == 2):
            contents = open("tsp250.txt", "r").readlines()  # load data
            print("wyniki dla tsp250:")
        if (i == 3):
            contents = open("tsp500.txt", "r").readlines()  # load data
            print("wyniki dla tsp500:")
        #if (i == 4):
         #   contents = open("tsp1000.txt", "r").readlines()  # load data
          #  print("wyniki dla tsp1000:")
           # niestety dla TSP1000 nie dziala greedy bo jest za gleboka rekurencja,
        # a ACO muli tak ze nie jest w stanie wydac odpowiedzi
            #
        n = int(contents[0]) # number of vertex
        contents = contents[1:] #coordinates of vertex (starts at one)
        graph =Graph(n, contents)
        greedySol=zachlanne.Greedy_Solution(graph)
        AcoSol=TSP_concurrent.antcolony(graph)
        printResults(greedySol, AcoSol)
        print("---------------------------------------------------------------------")
        i=i+1