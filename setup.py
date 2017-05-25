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

#opens the file and loads it
def openFile():
    global rootlabel
    global nodeSystem
    global capacityLimit


    filename = askopenfilename(parent=root)
    extension = os.path.splitext(filename)[1][1:]

    if extension == '':
        messagebox.showinfo("Error", "No file chosen, please click on a valid test file")

    else:
        with open(filename) as f:
            importData = f.readlines()

        importData = [x.strip() for x in importData]

        totalnodes = getValue(importData[3])
        capacityLimit = getValue(importData[5])

        nodeSystem = []
        nodeSystem = buildCoords(importData, totalnodes)



def getValue(text):
    return int(''.join(ele for ele in text if ele.isdigit() or ele == '.'))

#builds the coordinate system
def buildCoords(content,totalnodes):

    i = 0
    while i < totalnodes:
        x=content[7+i].split()
        nodeSystem.append(x)
        i += 1

    k = getDemand(content)

    k += 1

    i = 0
    while i < totalnodes:
        x=content[k+i].split()

        if len(nodeSystem[i]) == 3:
            nodeSystem[i].append(0)
        nodeSystem[i][3] = x[1]
        i += 1
    return nodeSystem

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

#calculates the
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

    output_string = []


    for i in range(len(route)):
        string = "Route " + str(i+1) +"\n"

        string += str(route[i][0])
        for j in range(0,len(route[i])-2):
            string += " -> " + str(route[i][j+1])

        string += " | Truck capacity = " + str(route[i][-1]) + "\n\n"
        output_string.append(str(string))

    time = '\n' + "Total time taken: " + str(time)

    dist = '\n' + "Total Distance: " + str(dist)

    output_string.append(str(time))
    output_string.append(str(dist))

    a = list(itertools.chain.from_iterable(output_string))

    x = "".join(a)

    return x

def centerwindow(width, height):

    screen_width = root.winfo_screenwidth()  # width of the screen
    screen_heights = root.winfo_screenheight()  # height of the screen

    x = (screen_width / 2) - (width / 2)
    y = (screen_heights / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def heuristic_setup():
    if len(nodeSystem) == 0:
        print("Please select a file")
        return 0

    start = time.clock()
    heurRoutes = heuristic(nodeSystem, capacityLimit)
    elapsed = time.clock() - start
    dist = calcRouteDist(heurRoutes, nodeSystem)
    heurRoutes.append(dist)
    heurRoutes.append(elapsed)

    x = routeListToString(heurRoutes)

    editArea1.insert(END, '\n')
    editArea1.insert(END, x)

def metaheuristic_setup():
    if len(nodeSystem) == 0:
        print("Please select a file")
        return 0

    start = time.clock()
    metaRoutes = metaheuristic(nodeSystem, capacityLimit)
    elapsed = time.clock() - start

    dist = calcRouteDist(metaRoutes, nodeSystem)
    metaRoutes.append(dist)
    metaRoutes.append(elapsed)

    x = routeListToString(metaRoutes)

    editArea2.insert(END, '\n')
    editArea2.insert(END, x)

def exact_setup():

    if len(nodeSystem) == 0:
        print("Please select a file")
        return 0

    start = time.clock()
    exactRoutes = exact(nodeSystem, capacityLimit)
    elapsed = time.clock() - start

    dist = calcRouteDist(exactRoutes, nodeSystem)
    exactRoutes.append(dist)
    exactRoutes.append(elapsed)

    x = routeListToString(exactRoutes)

    editArea3.insert(END, '\n')
    editArea3.insert(END, x)

# set up global vars
capacityLimit = 0
nodeSystem = []




root = Tk()
root.title('CVRP Algorithms')
notebook = ttk.Notebook(root)






tab1 = ttk.Frame(master = notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

bar1 = Frame(tab1)
bar2 = Frame(tab2)
bar3 = Frame(tab3)



notebook.add(tab1, text='Heuristic')
notebook.add(tab2, text='Meta-heuristic ')
notebook.add(tab3, text='Exact')
notebook.pack(expand=1, fill="both", side='top')



bar1.pack()
bar2.pack()
bar3.pack()

heuristic_button = Button(bar1, text="Run heuristic solver", command=heuristic_setup)
metaHeuristic_button = Button(bar2, text="Run metaheuristic solver", command=metaheuristic_setup)
exactSolver_button = Button(bar3, text="Run exact solver ", command=exact_setup)


heuristic_button.pack(side ='left')
metaHeuristic_button.pack(side ='left')
exactSolver_button.pack(side ='left')




open_fileButton = Button(bar1, text="Open VRP File", command=openFile)
open_fileButton.pack(side ='left')

open_fileButton = Button(bar2, text="Open VRP File", command=openFile)
open_fileButton.pack(side ='left')

open_fileButton = Button(bar3, text="Open VRP File", command=openFile)
open_fileButton.pack(side ='left')


quit_button = Button(bar1, text="Quit", command=quit)
quit_button.pack(side ='left')

quit_button = Button(bar2, text="Quit", command=quit)
quit_button.pack(side ='left')

quit_button = Button(bar3, text="Quit", command=quit)
quit_button.pack(side ='left')


#text box page 1
editArea1 = tkst.ScrolledText(
    master = tab1,
    width  = 20,
    height = 10,
    bg = '#ffffff'
)
editArea1.pack(padx=10, pady=10, expand=True, fill = "both" ,side = "top")
editArea1.insert(END,'Welcome to my FIT3036 project. Please press select a vrp file by pressing the button bellow')


#text box page 2
editArea2 = tkst.ScrolledText(
    master = tab2,
    width  = 20,
    height = 10,
    bg = '#ffffff'
)
editArea2.pack(padx=10, pady=10, expand=True, fill = "both" ,side = "top")
editArea2.insert(END,'This page is for the Tabu Solver')

#text box page 3
editArea3 = tkst.ScrolledText(
    master = tab3,
    width  = 20,
    height = 10,
    bg = '#ffffff'
)
editArea3.pack(padx=10, pady=10, expand=True, fill = "both" ,side = "top")
editArea3.insert(END,'This page is for Exact solver')

bar = Frame(root)




centerwindow(1000, 600)
app = Base(root)
root.mainloop()


