N,E,W,F = map(int,raw_input().split())
eastIndices = map(int,raw_input().split())
eastPop = map(int,raw_input().split())
eastCityInf = {}
for i in range(E):
    eastCityInf[eastIndices[i]] = eastPop[i]

westIndices = map(int,raw_input().split())
flights = {}
for i in range(F):
    o,d,l,t = map(int,raw_input().split())
    flights[(o,d)] = (l,t)

def getEdges(path):
    tuplePath = []
    n = len(path)
    for i in range(0,n-1):
        tuplePath.append((path[i],path[i+1]))
    return tuplePath

def bfs(g,start):
    print g
    Q = []
    Q.append([start])
    #print start
    while len(Q) > 0:
        path = Q.pop(0)
        u = path[-1]
        if u in westIndices:
            return getEdges(path)
        for v in g[u]:
            newPath = list(path)
            newPath.append(v)
            Q.append(newPath)
    return []

#normal adjacency list
FL = {}
for i in flights:
    if i[0] not in FL:
        FL[i[0]] = [i[1]]
    else:
        FL[i[0]].append(i[1])
        #print bfs(FL,0)

def FF(g,start):
    final = 0
    f = {}
    c = {}
    for i in flights:
        (u,v) = i
        f[i] = 0
        f[(v,u)] = 0
        c[i] = flights[i][0]
        path = bfs(g,start)
    while path and (path != []):
        d = [c[i] - f[i] for i in flights]
        pathD = {}
        for i in path:
            pathD[i] = d[i]
        m = min(pathD,key=pathD.get)
        final += m
        for i in path:
            (u,v) = i
            f[i] += m
            f[(v,u)] -= m
            
        # Find residual graph
        for i in flights:
            for i[0] in g:
                if i[1] in g[i[0]]:
                    if (c[i] - f[i] <= 0):
                        g[i[0]].remove(i[1])
        path = bfs(g,start)

G = {}
eastG = []
# Set up first two time layers (0 and 1)
for i in range(N):
    G[(i,0)] = []
    G[(i,1)] = []
    if i in eastIndices:
        eastG.append((i,0))
        eastG.append((i,1))

for i in flights:
    (o,d) = i
    if flights[i][1] <= 1:
        G[(o,0)].append((d,1))
stuffToAdd = []

def addLayer(g,time):
    for i in g:
        o = i[0]
        t = i[1]
        #print 'starts here ',o
        if o in FL:                
            for d in FL[o]:
                t1 = t + flights[(o,d)][1]
                if t1 <=  time:
                    if (d,t1) not in g[i]:
                        g[i].append((d,t1))
                    if (d,t1) not in g:
                        stuffToAdd.append((d,t1))
                    if d in eastIndices:
                        eastG.append((d,t1))
    for i in stuffToAdd:
        g[i] = []

        

# See if there is a path from east to west coast in G as it is now
T = 1
found = False
while found == False:
    for i in eastG:
        path = bfs(G,i)
        print path
        #print T
        if (not path) or (path == []):
            T += 1
            addLayer(G,T)
        else:
            flow = FF(G,i)
            print 'flow =',flow
            if eastCityInf[i] <= flow:
                found = True
            else:
                T += 1
                addLayer(G,T)

print T
                
