from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os.path
import math
import main

from tkinter.scrolledtext import ScrolledText

# main base window
# [depot, ......., capacity]


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

# emtpy modules for design



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
        system[i].append(x[1])
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
    dist = abs(x1 - x2) + abs(y1 - y2)

    return dist

def calcRouteDist(route,system):

    totalDist = 0
    for i in range(0,len(route)):
        for j in range(0,len(route[i])-2):
            #print('i:' + str(i))
            #print('j' + str(j))
            #print('route: ' + str(route[i][j]))
            x1 = system[route[i][j]-1][1]
            y1 = system[route[i][j]-1][2]
            x2 = system[route[i][j+1]-1][1]
            y2 = system[route[i][j+1]-1][2]

            totalDist += eucDistance(x1,y1,x2,y2)

    print(totalDist)


def openFile():
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
        #print(content)
        totalnodes = getNum(content[3])
        capacityLimit = getNum(content[5])
        print(capacityLimit)
        system = buildCoords(content, totalnodes)
        print(system)

def heuristic():
    global system
    main.heuristic(system)
    print(routes_heur)
    calcRouteDist(routes_heur, system)
    #return 0

def metaheuristic():
    main.metaheuristic(system)
    print(routes_meta)
    calcRouteDist(routes_meta, system)
    #return 0

def exact():
    main.exact(system)
    calcRouteDist(routes_exact, system)
    print(routes_exact)
    #return 0

# set up global vars
capacityLimit = 0
routes_heur = []
routes_meta = []
routes_exact = []
system = []

# create base window root and notebook widget instance
root = Tk()
root.title('CVRP Algorithms')
nb = ttk.Notebook(root)

# first page, which would get widgets gridded into it
page1 = ttk.Frame(nb)

# adding more pages and titles for them
page2 = ttk.Frame(nb)
page3 = ttk.Frame(nb)

nb.add(page1, text='Clarke-Wright')
nb.add(page2, text='Tabu Search')
nb.add(page3, text='Exact Solver')
nb.pack(expand=1, fill="both")


# button to open a file
b = Button(root, text="Open VRP File", command=openFile)
b.pack()


# quit button for entire program
tkButtonQuit = Button(root, text="Quit", command=quit)
tkButtonQuit.pack()


# buttons for running algorithms in tabs
heuristicLaunch = Button(page1, text="Run heuristic algorithm", command=heuristic())
metaHeuristicLaunch = Button(page2, text="Run metaheuristic algorithm", command=metaheuristic())
exactSolverLaunch = Button(page3, text="Run exact solver algorithm", command=exact())
heuristicLaunch.pack()
metaHeuristicLaunch.pack()
exactSolverLaunch.pack()


# center the window to middle of screen and run program
centerwindow(800, 650)
app = Base(root)
root.mainloop()


