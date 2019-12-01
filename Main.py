from math import sqrt
import zachlanne
import TSP_heuristic
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

def main():
    contents = open("berlin52.txt", "r").readlines() #load data
    n = int(contents[0]) # number of vertex
    contents = contents[1:] #coordinates of vertex (starts at one)
    graph =Graph(n, contents)
    greedySol=zachlanne.Greedy_Solution(graph)
    AcoSol=TSP_heuristic.antcolony(graph)

    printResults(greedySol, AcoSol)

main()