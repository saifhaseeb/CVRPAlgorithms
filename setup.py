from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os.path

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

def heuristic():
    return 0

def metaheuristic():
    return 0

def exact():
    return 0

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
        messagebox.showinfo("Error", "No file chosen, please click on a valid test file")

    else:
        with open(filename) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        print(content)
        totalnode = getNum(content[3])

    def getGridSize():

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
