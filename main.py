import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os.path
import operator
import math
#from ortools.constraint_solver import pywrapcp
#from ortools.constraint_solver import routing_enums_pb2
#import tabu
#import pantsf
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
        messagebox.showinfo("Error", "No file chosen, please click on a valid test file")

    else:
        with open(filename) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        totalnodes = getNum(content[3])
        global capacityLimit
        capacityLimit = getNum(content[5])
        system = buildCoords(content,totalnodes)
        heuritic(system)

        metaheuristic(system)
        print(routes_meta)

        exact(system)

        print(routes_exact)


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

    #print(routes)
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


def metaheuristic(system):

    def distance(x1, y1, x2, y2):
        # Manhattan distance
        dist = abs(x1 - x2) + abs(y1 - y2)

        return dist

    class CreateDistanceCallback(object):
        """Create callback to calculate distances between points."""

        def __init__(self, locations):
            """Initialize distance array."""
            size = len(locations)
            self.matrix = {}

            for from_node in range(size):
                self.matrix[from_node] = {}
                for to_node in range(size):
                    x1 = locations[from_node][0]
                    y1 = locations[from_node][1]
                    x2 = locations[to_node][0]
                    y2 = locations[to_node][1]
                    self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

        def Distance(self, from_node, to_node):
            return self.matrix[from_node][to_node]

    # Demand callback
    class CreateDemandCallback(object):
        """Create callback to get demands at each location."""

        def __init__(self, demands):
            self.matrix = demands

        def Demand(self, from_node, to_node):
            return self.matrix[from_node]

    def tabu():
        global routes_meta
        routes_meta = []
        # Create the data.
        data = create_data_array()
        #print(data)
        locations = data[0]
        demands = data[1]
        num_locations = len(locations)
        depot = 0  # The depot is the start and end point of each route.
        num_vehicles = 100

        # Create routing model.
        if num_locations > 0:
            routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot)
            search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
            # print(routing)

            # Setting first solution heuristic: the
            # method for finding a first solution to the problem.
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

            search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH

            # search_parameters.local_search_metaheuristic = routing_enums_pb2.solution_limit.10000

            search_parameters.time_limit_ms = 3000

            # print(search_parameters)

            # The 'PATH_CHEAPEST_ARC' method does the following:
            # Starting from a route "start" node, connect it to the node which produces the
            # cheapest route segment, then extend the route by iterating on the last
            # node added to the route.

            # Put a callback to the distance function here. The callback takes two
            # arguments (the from and to node indices) and returns the distance between
            # these nodes.

            dist_between_locations = CreateDistanceCallback(locations)
            dist_callback = dist_between_locations.Distance
            routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)

            # Put a callback to the demands.
            demands_at_locations = CreateDemandCallback(demands)
            demands_callback = demands_at_locations.Demand

            # Add a dimension for demand.
            slack_max = 0
            vehicle_capacity = capacityLimit
            fix_start_cumul_to_zero = True
            demand = "Demand"
            routing.AddDimension(demands_callback, slack_max, vehicle_capacity,
                                 fix_start_cumul_to_zero, demand)

            # Solve, displays a solution if any.
            assignment = routing.SolveWithParameters(search_parameters)
            if assignment:
                # Display solution.
                # Solution cost.
                print("\nTotal distance of all routes: " + str(assignment.ObjectiveValue()) + "\n")

                for vehicle_nbr in range(num_vehicles):
                    index = routing.Start(vehicle_nbr)
                    index_next = assignment.Value(routing.NextVar(index))
                    route = ''
                    route_dist = 0
                    route_demand = 0
                    rt = []

                    while not routing.IsEnd(index_next):
                        node_index = routing.IndexToNode(index)
                        node_index_next = routing.IndexToNode(index_next)
                        route += str(node_index) + " -> "
                        rt.append(node_index+1)
                        # Add the distance to the next node.
                        route_dist += dist_callback(node_index, node_index_next)
                        # Add demand.
                        route_demand += demands[node_index_next]
                        index = index_next
                        index_next = assignment.Value(routing.NextVar(index))

                    node_index = routing.IndexToNode(index)
                    node_index_next = routing.IndexToNode(index_next)

                    rt.append(node_index+1)
                    rt.append(node_index_next+1)
                    #print(rt)
                    route += str(node_index) + " -> " + str(node_index_next)
                    route_dist += dist_callback(node_index, node_index_next)

                    rt.append(route_demand)
                    routes_meta.append(rt)


                    #print "Route for vehicle " + str(vehicle_nbr) + ":\n\n" + route + "\n"
                    #print "Distance of route " + str(vehicle_nbr) + ": " + str(route_dist)
                    #print "Demand met by vehicle " + str(vehicle_nbr) + ": " + str(route_demand) + "\n"


                #print(routes)

                h = 0
                while h <= len(routes_meta)-1:
                    if routes_meta[h][0] == 1 and routes_meta[h][1] == 1:

                        del routes_meta[h]
                        h -= 1
                    h += 1

                #print(routes)
                #return routes


            else:
                print('No solution found.')
        else:
            print('Specify an instance greater than 0.')

    def create_data_array():
        locations = []

        i = 0
        while i <= len(system)-1:
            x = system[i][1]
            y = system[i][2]
            temp = [int(x),int(y)]
            locations.append(temp)

            i += 1


        demands = []

        i = 0
        while i <= len(system)-1:

            x = system[i][3]
            demands.append(int(x))

            i += 1


        data = [locations, demands]
        return data
    tabu()


def exact(system):

    def distance(x1, y1, x2, y2):
        # Manhattan distance
        dist = abs(x1 - x2) + abs(y1 - y2)

        return dist

    class CreateDistanceCallback(object):
        """Create callback to calculate distances between points."""

        def __init__(self, locations):
            """Initialize distance array."""
            size = len(locations)
            self.matrix = {}

            for from_node in range(size):
                self.matrix[from_node] = {}
                for to_node in range(size):
                    x1 = locations[from_node][0]
                    y1 = locations[from_node][1]
                    x2 = locations[to_node][0]
                    y2 = locations[to_node][1]
                    self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

        def Distance(self, from_node, to_node):
            return self.matrix[from_node][to_node]

    # Demand callback
    class CreateDemandCallback(object):
        """Create callback to get demands at each location."""

        def __init__(self, demands):
            self.matrix = demands

        def Demand(self, from_node, to_node):
            return self.matrix[from_node]

    def exact():
        global routes_exact
        routes_exact = []
        # Create the data.
        data = create_data_array()
        #print(data)
        locations = data[0]
        demands = data[1]
        num_locations = len(locations)
        depot = 0  # The depot is the start and end point of each route.
        num_vehicles = 100

        # Create routing model.
        if num_locations > 0:
            routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot)
            search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
            # print(routing)

            # Setting first solution heuristic: the
            # method for finding a first solution to the problem.
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)


            search_parameters.local_search_operators.use_tsp_opt = True


            # print(search_parameters)

            # The 'PATH_CHEAPEST_ARC' method does the following:
            # Starting from a route "start" node, connect it to the node which produces the
            # cheapest route segment, then extend the route by iterating on the last
            # node added to the route.

            # Put a callback to the distance function here. The callback takes two
            # arguments (the from and to node indices) and returns the distance between
            # these nodes.

            dist_between_locations = CreateDistanceCallback(locations)
            dist_callback = dist_between_locations.Distance
            routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)

            # Put a callback to the demands.
            demands_at_locations = CreateDemandCallback(demands)
            demands_callback = demands_at_locations.Demand

            # Add a dimension for demand.
            slack_max = 0
            vehicle_capacity = capacityLimit
            fix_start_cumul_to_zero = True
            demand = "Demand"
            routing.AddDimension(demands_callback, slack_max, vehicle_capacity,
                                 fix_start_cumul_to_zero, demand)

            # Solve, displays a solution if any.
            assignment = routing.SolveWithParameters(search_parameters)
            if assignment:
                # Display solution.
                # Solution cost.
                print("\nTotal distance of all routes: " + str(assignment.ObjectiveValue()) + "\n")

                for vehicle_nbr in range(num_vehicles):
                    index = routing.Start(vehicle_nbr)
                    index_next = assignment.Value(routing.NextVar(index))
                    route = ''
                    route_dist = 0
                    route_demand = 0
                    rt = []

                    while not routing.IsEnd(index_next):
                        node_index = routing.IndexToNode(index)
                        node_index_next = routing.IndexToNode(index_next)
                        route += str(node_index) + " -> "
                        rt.append(node_index+1)
                        # Add the distance to the next node.
                        route_dist += dist_callback(node_index, node_index_next)
                        # Add demand.
                        route_demand += demands[node_index_next]
                        index = index_next
                        index_next = assignment.Value(routing.NextVar(index))

                    node_index = routing.IndexToNode(index)
                    node_index_next = routing.IndexToNode(index_next)

                    rt.append(node_index+1)
                    rt.append(node_index_next+1)
                    #print(rt)
                    route += str(node_index) + " -> " + str(node_index_next)
                    route_dist += dist_callback(node_index, node_index_next)

                    rt.append(route_demand)
                    routes_exact.append(rt)


                    #print "Route for vehicle " + str(vehicle_nbr) + ":\n\n" + route + "\n"
                    #print "Distance of route " + str(vehicle_nbr) + ": " + str(route_dist)
                    #print "Demand met by vehicle " + str(vehicle_nbr) + ": " + str(route_demand) + "\n"


                #print(routes)

                h = 0
                while h <= len(routes_exact)-1:
                    if routes_exact[h][0] == 1 and routes_exact[h][1] == 1:

                        del routes_exact[h]
                        h -= 1
                    h += 1

                #print(routes)
                #return routes


            else:
                print('No solution found.')
        else:
            print('Specify an instance greater than 0.')

    def create_data_array():
        locations = []

        i = 0
        while i <= len(system)-1:
            x = system[i][1]
            y = system[i][2]
            temp = [int(x),int(y)]
            locations.append(temp)

            i += 1


        demands = []

        i = 0
        while i <= len(system)-1:

            x = system[i][3]
            demands.append(int(x))

            i += 1


        data = [locations, demands]
        return data
    exact()

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
routes_meta = []
routes_exact = []
root.mainloop()