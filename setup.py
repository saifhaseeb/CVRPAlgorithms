from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# main base window


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


root = Tk()
root.title('CVRP Algorithms')
nb = ttk.Notebook(root)

# first page, which would get widgets gridded into it
page1 = ttk.Frame(nb)

# second page
page2 = ttk.Frame(nb)
page3 = ttk.Frame(nb)
text = ScrolledText(page2)
text.pack(expand=1, fill="both")

nb.add(page1, text='Clarke-Wright')
nb.add(page2, text='Tabu Search')
nb.add(page3, text='Exact Solver')

nb.pack(expand=1, fill="both")
centerwindow(800, 650)
app = Base(root)
root.mainloop()
