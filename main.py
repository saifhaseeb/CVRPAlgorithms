import time
import setup
import operator

def heuristic(system):

    print(system)

    global capacityLimit
    global routes_huer

    def mergeFeasibility(routes, nodeA, nodeB, routeA, routeB):
        global capacityLimit

        # if not in same route
        if routeA != routeB:
            if routes[routeA] != "null" and routes[routeB] != "null":
                # if capacity of the 2 routes is under the limit
                if int(routes[routeA][-1]) + int(routes[routeB][-1]) <= capacityLimit:
                    # if node a is at the start or end
                    if routes[routeA][1] == nodeA or routes[routeA][-3] == nodeA:
                        # if node b is at the start or end
                        if routes[routeB][1] == nodeB or routes[routeB][-3] == nodeB:
                            return True

        return False

    def mergeRoutes(routes, routeA, routeB, nodeA, nodeB, locationA, locationB):

        # merge a into b
        # if A is on the left
        if nodeA == routes[routeA][1]:
            # if b is on the right
            if nodeB == routes[routeB][-3]:
                # print("al,br")
                j = 0
                while j <= len(routes[routeA]) - 4:
                    routes[routeB].insert(locationB + 1 + j, routes[routeA][locationA + j])
                    # print(routes)
                    j += 1
                routes[routeB][-1] += routes[routeA][-1]
                routes[routeA] = 'null'
                # print(routes[routeB])

            # if b is on the left
            elif nodeB == routes[routeB][1]:
                # print("aL,bL")
                j = 0
                while j <= len(routes[routeA]) - 4:
                    routes[routeB].insert(1, routes[routeA][locationA + j])
                    # print(routes)
                    j += 1
                routes[routeB][-1] += routes[routeA][-1]
                routes[routeA] = 'null'
                # print(routes[routeB])

        # if A is on the right
        if nodeA == routes[routeA][-3]:
            # if b is on the right
            if nodeB == routes[routeB][-3]:
                # print("aR,bR")
                j = 0
                while j <= len(routes[routeA]) - 4:
                    routes[routeB].insert(locationB + 1 + j, routes[routeA][locationA - j])
                    # print(routes)
                    j += 1
                routes[routeB][-1] += routes[routeA][-1]
                routes[routeA] = 'null'
                # print(routes[routeB])
            # if b is on the left
            elif nodeB == routes[routeB][1]:
                # print("aR,bL")
                j = 0
                # print(routeA)
                while j <= len(routes[routeA]) - 4:
                    routes[routeB].insert(1, routes[routeA][locationA - j])
                    j += 1
                routes[routeB][-1] += routes[routeA][-1]
                routes[routeA] = 'null'
                # print(routes[routeB])


    start = time.clock()
    depotX = system[0][1]
    depotY = system[0][2]

    k = len(system)

    i = 2
    routes = []

    while i <= k:
        x = [1,i,1,int(system[i-1][3])]
        routes.append(x)
        i += 1

    savings = []

    i = 1
    while i <= k+1:

        j = i+1

        while j < k:
            nodeix = system[i][1]
            nodeiy = system[i][2]
            nodejx = system[j][1]
            nodejy = system[j][2]


            d1 = setup.eucDistance(depotX,depotY,nodeix,nodeiy)
            d2 = setup.eucDistance(depotX,depotY,nodejx,nodejy)
            d3 = setup.eucDistance(nodeix,nodeiy,nodejx,nodejy)


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

            mergeRoutes(system,routes,routeA,routeB,nodeA,nodeB,locationA,locationB)


        i += 1

    strippedRoutes = list(filter(('null').__ne__,routes))
    #print(strippedRoutes)
    routes_huer = strippedRoutes

    elapsed = time.clock() - start
    print(elapsed)


    #print(routes)

