from tkinter import *
from tkinter import ttk

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
