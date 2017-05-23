import Tkinter as tk
from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox
import os.path
import operator
import math
#import pants
import random

def getNum(text):
    return int(''.join(ele for ele in text if ele.isdigit() or ele == '.'))

def findLargestNumber(text):
    ls = list()
    for w in text.split():
        try:
            ls.append(int(w))
        except:
            pass
    try:
        return max(ls)
    except:
        return None

def openFile():

    filename = askopenfilename(parent=root)
    extension = os.path.splitext(filename)[1][1:]

    if extension == '':
        tkMessageBox.showinfo("Error", "No file chosen, please click on a valid test file")

    else:
        with open(filename) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        totalnodes = getNum(content[3])
        global capacityLimit
        capacityLimit = getNum(content[5])
        system = buildCoords(content,totalnodes)
        heuritic(system)
        #metaheuristic(system)


def getGridSize(content):

    #print('Raj')
    flag = False
    i = 0
    k = len(content)
    largestnumberArray = []

    while not flag:
        while i < k:

            if content[i] == 'EOF':
                flag = True

            if content[i][0].isdigit():
                largestnumber = findLargestNumber(content[i])
                largestnumberArray.append(largestnumber)
                i += 1

            else:
                i += 1

        largestCoordinate = max(largestnumberArray)

    x = 0

    if largestCoordinate < 10000:
        x = 10000

    if largestCoordinate < 1000:
        x = 1000

    if largestCoordinate > 100:
        x = 100

    return x

def createGrid():

    x = [['.' for i in range(getGridSize())] for j in range(getGridSize())]
    return x

def buildCoords(content,totalnodes):
    system = []


    i = 0
    while i < totalnodes:
        x=content[7+i].split()
        system.append(x)
        i += 1

    k = getDemand(content)



    k += 1

    i = 0
    while i < totalnodes:
        x=content[k+i].split()
        system[i].append(x[1])
        i += 1

    print(system)

    return system



def getDemand(content):
    i = 0
    k = len(content)
    while i < k:
        if content[i] == "DEMAND_SECTION":
            return  i
        i += 1

def heuritic(system):
    global capacityLimit
    global routes
    depotX = system[0][1]
    depotY = system[0][2]

    k = len(system)

    i = 2
    routes = []

    while i <= k:
        x = [1,i,1,int(system[i-1][3])]
        routes.append(x)
        i += 1

    print(routes)
    savings = []

    i = 1
    while i <= k+1:

        j = i+1

        while j < k:
            nodeix = system[i][1]
            nodeiy = system[i][2]
            nodejx = system[j][1]
            nodejy = system[j][2]


            d1 = calcDist(depotX,depotY,nodeix,nodeiy)
            d2 = calcDist(depotX,depotY,nodejx,nodejy)
            d3 = calcDist(nodeix,nodeiy,nodejx,nodejy)


            savingscalc = 0
            savingscalc = d1 + d2 - d3


            x = [i+1,j+1,savingscalc]
            savings.append(x)

            j += 1
        i += 1

    savings.sort(key=operator.itemgetter(2),reverse=True)
    print(savings)

    #route merging

    i = 0
    while i <= len(savings)-1:

        nodeA = int(savings[i][0])
        nodeB = int(savings[i][1])

        p = 0

        while p < len(routes):
            h = 0
            while h < len(routes[p])-1:
                if routes[p][h] == nodeA:
                    routeA = p
                    locationA = h
                if routes[p][h] == nodeB:
                    routeB = p
                    locationB = h
                h += 1
            p += 1

        routeA = int(routeA)
        routeB = int(routeB)

        if mergeFeasibility(routes,nodeA,nodeB,routeA,routeB):

            mergeRoutes(routeA,routeB,nodeA,nodeB,locationA,locationB)


        i += 1

    strippedRoutes = list(filter(('null').__ne__,routes))
    print(strippedRoutes)

def mergeRoutes(routeA,routeB,nodeA,nodeB,locationA,locationB):
    global routes

    # merge a into b
    # if A is on the left
    if nodeA == routes[routeA][1]:
        # if b is on the right
        if nodeB == routes[routeB][-3]:
            #print("al,br")
            j = 0
            while j <= len(routes[routeA])-4:
                routes[routeB].insert(locationB+1+j,routes[routeA][locationA+j])
                #print(routes)
                j += 1
            routes[routeB][-1] += routes[routeA][-1]
            routes[routeA] = 'null'
            #print(routes[routeB])

        #if b is on the left
        elif nodeB == routes[routeB][1]:
            #print("aL,bL")
            j = 0
            while j <= len(routes[routeA]) - 4:
                routes[routeB].insert(1, routes[routeA][locationA + j])
                #print(routes)
                j += 1
            routes[routeB][-1] += routes[routeA][-1]
            routes[routeA] = 'null'
            #print(routes[routeB])

    # if A is on the right
    if nodeA == routes[routeA][-3]:
        #if b is on the right
        if nodeB == routes[routeB][-3]:
            #print("aR,bR")
            j = 0
            while j <= len(routes[routeA])-4:
                routes[routeB].insert(locationB+1+j,routes[routeA][locationA-j])
                #print(routes)
                j += 1
            routes[routeB][-1] += routes[routeA][-1]
            routes[routeA] = 'null'
            #print(routes[routeB])
        #if b is on the left
        elif nodeB == routes[routeB][1]:
            #print("aR,bL")
            j = 0
            #print(routeA)
            while j <= len(routes[routeA])-4:
                routes[routeB].insert(1,routes[routeA][locationA-j])
                j += 1
            routes[routeB][-1] += routes[routeA][-1]
            routes[routeA] = 'null'
            #print(routes[routeB])


    #print(routes)




def mergeFeasibility(routes,nodeA,nodeB,routeA,routeB):
    global capacityLimit

    #if not in same route
    if routeA != routeB:
        if routes[routeA] != "null" and routes[routeB] != "null":
            #if capacity of the 2 routes is under the limit
            if int(routes[routeA][-1]) + int(routes[routeB][-1]) <= capacityLimit:
                #if node a is at the start or end
                if routes[routeA][1] == nodeA or routes[routeA][-3] == nodeA:
                    #if node b is at the start or end
                    if routes[routeB][1] == nodeB or routes[routeB][-3] == nodeB:

                        return True

    return False




def calcDist(x1,y1,x2,y2):
    calc1 = int(x1) - int(x2)
    calc2 = int(y1) - int(y2)

    calc = calc1**2 + calc2**2

    calc = math.sqrt(calc)

    return calc

'''
def metaheuristic(system):
    print(system)

    nodes = []

    for _ in range(20):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        nodes.append((x, y))

    print(nodes)
    def euclidean(a, b):
        return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

    world = pants.World(nodes, euclidean)

    solver = pants.Solver()

    solution = solver.solve(world)

    print(solution.distance)
    print(solution.tour)  # Nodes visited in order
    print(solution.path)  # Edges taken in order
'''


root = Tk()
b = Button(root, text="Open VRP File", command=openFile)
b.pack()
capacityLimit = 0
routes = []
root.mainloop()