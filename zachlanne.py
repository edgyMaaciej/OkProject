from math import sqrt


def distance(x1, x2, y1, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def closest_aviable(point, path, list):  # finds the closest point that hasn't been visited yet
    min = 0
    while min in path or min == point:
        min += 1
    for i in range(len(list)):
        if i not in path and i != point and list[point][min] >= list[point][i]:
            min = i
    return min


def recursive_path(point, path, distance, matrix):  # our greedy TSP solution
    path.append(point)  # adds current point to the path
    new_point = closest_aviable(point, path, matrix)
    if len(path) == len(matrix):  # if all vertex has been visited
        path.append(0)  # we add out startpoint
        for i in range(len(path)):
            path[i] += 1
        return path, distance + matrix[0][point]
    else:
        distance += matrix[point][new_point]
        return recursive_path(new_point, path, distance, matrix)


class Graph:
    def __init__(self, n, points):  # constructor
        self.matrix = [[0 for i in range(n)] for j in range(n)]  # adjacency matrix
        for i in range(len(points)):  # we fill our matrix with the distances
            [p, x, y] = points[i].split(' ')
            p, x, y = int(p) - 1, int(x), int(y)
            for j in range(i, len(points)):
                [p1, x1, y1] = points[j].split(' ')
                p1, x1, y1 = int(p1) - 1, int(x1), int(y1)
                self.matrix[p][p1] = self.matrix[p1][p] = distance(x, x1, y, y1)

    def findpath(self):
        return recursive_path(0, [], 0, self.matrix)


def main():
    contents = open("data.txt", "r").readlines()  # load data
    n = int(contents[0])  # number of vertex
    contents = contents[1:]  # coordinates of vertex (starts at one)
    graph = Graph(n, contents)
    path, distance = graph.findpath()  # our TSP solution,first arg is a list of vertex,second is a distance value
    print(path, distance)
    #test push

main()