import random

n=int(input("Podaj ilosc wierzcholkow"))
x=[]
y=[]
file = open("testfile.txt","w")
for i in range (n):
   x.append(random.randint(1,100))
   y.append(random.randint(1,100))
for i in range (n):
    napis= str(i+1)+" "+str(x[i])+" "+str(y[i])+"\n"
    file.write(str(napis))

