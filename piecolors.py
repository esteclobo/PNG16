import math

def cores (n):
    leasth=360/n
    listah=[]
    listas=[]
    listal=[]
    for x in range(n):
        listah.append(leasth*x)
        if x % 2 == 0:
            listas.append(50)
        else:
            listas.append(100)
        listal.append(50)
    return listah,listas,listal
print (cores(2))
