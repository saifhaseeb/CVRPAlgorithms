from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os.path
import math
import time
import itertools
import tkinter.scrolledtext as tkst

from main import heuristic
from main import metaheuristic
from main import exact

class Base(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title('CVRP Algorithms')
        self.pack(fill=BOTH, expand=1)


def centerwindow(w, h):

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def getNum(text):
    return int(''.join(ele for ele in text if ele.isdigit() or ele == '.'))


def buildCoords(content,totalnodes):

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

        if len(system[i]) == 3:
            system[i].append(0)
        system[i][3] = x[1]
        i += 1
    return system

def getDemand(content):
    i = 0
    k = len(content)
    while i < k:
        if content[i] == "DEMAND_SECTION":
            return  i
        i += 1

def eucDistance(x1, y1, x2, y2):
    dist = math.sqrt((int(x2) - int(x1)) ** 2 + (int(y2) - int(y1)) ** 2)
    return dist

def manDistance(x1, y1, x2, y2):
    # Manhattan distance
    dist = abs(int(x1) - int(x2)) + abs(int(y1) - int(y2))

    return dist

def calcRouteDist(route,system):

    totalDist = 0
    for i in range(0,len(route)):
        for j in range(0,len(route[i])-2):

            x1 = system[route[i][j]-1][1]
            y1 = system[route[i][j]-1][2]
            x2 = system[route[i][j+1]-1][1]
            y2 = system[route[i][j+1]-1][2]

            totalDist += eucDistance(x1,y1,x2,y2)

    return totalDist

def routeListToString(route):

    time = route.pop()
    dist = route.pop()

    routestring = []


    for i in range(len(route)):
        string = "Route " + str(i+1) +"\n"

        string += str(route[i][0])
        for j in range(0,len(route[i])-2):
            string += " -> " + str(route[i][j+1])

        string += " | Truck capacity = " + str(route[i][-1]) + "\n\n"
        routestring.append(str(string))

    time = '\n' + "Total time taken: " + str(time)

    dist = '\n' + "Total Distance: " + str(dist)

    routestring.append(str(time))
    routestring.append(str(dist))

    a = list(itertools.chain.from_iterable(routestring))

    x = "".join(a)

    return x

def openFile():
    global rootlabel
    global system
    global capacityLimit


    filename = askopenfilename(parent=root)
    extension = os.path.splitext(filename)[1][1:]

    if extension == '':
        messagebox.showinfo("Error", "No file chosen, please click on a valid test file")

    else:
        with open(filename) as f:
            content = f.readlines()

        content = [x.strip() for x in content]

        totalnodes = getNum(content[3])
        capacityLimit = getNum(content[5])

        system = []
        system = buildCoords(content, totalnodes)


def heuristic_setup():
    if len(system) == 0:
        print("no files selected")
        return 0

    start = time.clock()
    routes_heur = heuristic(system,capacityLimit)
    elapsed = time.clock() - start
    dist = calcRouteDist(routes_heur, system)
    routes_heur.append(dist)
    routes_heur.append(elapsed)

    x = routeListToString(routes_heur)

    editArea1.insert(END, '\n')
    editArea1.insert(END, x)

def metaheuristic_setup():
    if len(system) == 0:
        print("no files selected")
        return 0

    start = time.clock()
    routes_meta = metaheuristic(system, capacityLimit)
    elapsed = time.clock() - start

    dist = calcRouteDist(routes_meta, system)
    routes_meta.append(dist)
    routes_meta.append(elapsed)

    x = routeListToString(routes_meta)

    editArea2.insert(END, '\n')
    editArea2.insert(END, x)

def exact_setup():

    if len(system) == 0:
        print("no files selected")
        return 0

    start = time.clock()
    routes_exact = exact(system, capacityLimit)
    elapsed = time.clock() - start

    dist = calcRouteDist(routes_exact, system)
    routes_exact.append(dist)
    routes_exact.append(elapsed)

    x = routeListToString(routes_exact)

    editArea3.insert(END, '\n')
    editArea3.insert(END, x)

# set up global vars
capacityLimit = 0
system = []

# create base window root and notebook widget instance
root = Tk()
root.title('CVRP Algorithms')
nb = ttk.Notebook(root)

# first page, which would get widgets gridded into it
page1 = ttk.Frame(master = nb)

# adding more pages and titles for them
page2 = ttk.Frame(nb)
page3 = ttk.Frame(nb)

nb.add(page1, text='Clarke-Wright')
nb.add(page2, text='Tabu Search')
nb.add(page3, text='Exact Solver')
nb.pack(expand=1, fill="both",side='top')


# quit button for entire program
tkButtonQuit = Button(page1, text="Quit", command=quit)
tkButtonQuit.pack(side = 'bottom')

tkButtonQuit = Button(page2, text="Quit", command=quit)
tkButtonQuit.pack(side = 'bottom')

tkButtonQuit = Button(page3, text="Quit", command=quit)
tkButtonQuit.pack(side = 'bottom')

# button to open a file
b = Button(page1, text="Open VRP File", command=openFile)
b.pack(side = 'bottom')

b = Button(page2, text="Open VRP File", command=openFile)
b.pack(side = 'bottom')

b = Button(page3, text="Open VRP File", command=openFile)
b.pack(side = 'bottom')


# buttons for running algorithms in tabs
heuristicLaunch = Button(page1, text="Run heuristic algorithm", command=heuristic_setup)
metaHeuristicLaunch = Button(page2, text="Run metaheuristic algorithm", command=metaheuristic_setup)
exactSolverLaunch = Button(page3, text="Run exact solver algorithm", command=exact_setup)
heuristicLaunch.pack(side = 'bottom')
metaHeuristicLaunch.pack(side = 'bottom')
exactSolverLaunch.pack(side = 'bottom')


#page 1
editArea1 = tkst.ScrolledText(
    master = page1,
    width  = 20,
    height = 10,
    bg = '#ffffff'
)
editArea1.pack(padx=10, pady=10, expand=True, fill = "both" ,side = "top")
editArea1.insert(END,'Welcome to my FIT3036 project. Please press select file to input a cvrp problem')


#page 1
editArea2 = tkst.ScrolledText(
    master = page2,
    width  = 20,
    height = 10,
    bg = '#ffffff'
)
editArea2.pack(padx=10, pady=10, expand=True, fill = "both" ,side = "top")
editArea2.insert(END,'This page is for the Tabu Search')

#page 1
editArea3 = tkst.ScrolledText(
    master = page3,
    width  = 20,
    height = 10,
    bg = '#ffffff'
)
editArea3.pack(padx=10, pady=10, expand=True, fill = "both" ,side = "top")
editArea3.insert(END,'This page is for Exact Algorithm')





# center the window to middle of screen and run program
centerwindow(1000, 600)
app = Base(root)
root.mainloop()


