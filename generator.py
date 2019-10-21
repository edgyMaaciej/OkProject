import random

n=int(input("Podaj ilosc wierzcholkow"))
x=[]
y=[]
file = open("testfile.txt","w")

for i in range (n):

    new_x=random.randint(1,100)
    new_y=random.randint(1,100)
    while x.__contains__(new_x) and y.__contains__(new_y):
        new_x = random.randint(1, 100)
        new_y = random.randint(1, 100)
    x.append(new_x)
    y.append(new_y)

for i in range (n):
    napis= str(i+1)+" "+str(x[i])+" "+str(y[i])+"\n"
    file.write(str(napis))
