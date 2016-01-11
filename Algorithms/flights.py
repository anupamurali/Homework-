N,numEast,numWest,numFl = map(int,raw_input().split())
eastIndices = map(int,raw_input().split())
eastPop = map(int,raw_input().split())
westIndices = map(int,raw_input().split())
flights = []
flightDict = {}
for i in range(numFl):
    o,d,l,t = map(int,raw_input().split())
    flights.append((o,d,l,t))
    flightDict[(o,d)] = (l,t)

adjList = {}
othAdjList = {}
for i in flights:
    (o,d,l,t) = i
    if o not in adjList:
        adjList[o] = [d]
        othAdjList[o] = [d]
    else:
        adjList[o].append(d)
        othAdjList[o].append(d)

prev = {}
#print 'adjlist = ',adjList
def pathForG(G,v,end,vis,currPath):
    global prev
    #print v,end
    #print currPath
    vis.append(v)
    if v == end:
        if v in prev:
            #print 'yo'
            if (prev[v],v) not in currPath:
                currPath.append((u,v))
        return currPath
    else:
        for w in G[v]:
            #print 'this edge =',(v,w)
            if w not in vis:
                prev[w] = v
                #print 'vertex is ',w
                if w in prev:
                    if (prev[w],w) not in currPath:
                        currPath.append((prev[w],w))
                return pathForG(G,w,end,vis,currPath)
            #print 'adjlist = ',adjList
        return currPath

Prev = {}
def dfs(G,v,end):
    global Prev
    global N
    currPath = []
    noVisits = {}
    T = []
    if v == end:
        return []
    for i in range(N):
        noVisits[i] = 0
    T.append(v)
    count = 1
    noVisits[v] = 1
    while len(T) != 0:
        print T
        v = T.pop(0)
        for w in G[v]:
            print T
            print (v,w)
            if noVisits[w] == 0:
                count = count + 1
                noVisits[w] = count
                currPath.append((v,w))
                if w == end:
                    return currPath
                else:
                    T.append(w)
    return currPath
                
    
    
G = adjList
def maxFlowPathForT(start,end,population,T):
    flow = {}
    capacities = {}
    for i in flightDict:
        flow[i] = 0
        capacities[i] = flightDict[i][0]
    path = dfs(G,start,end)
    #print 'C=',capacities
    print path
    timeArray = []
    while path and (path != []):
        diff = {}
        for i in flightDict:
            if i in flow:
                if i[1] in G[i[0]] :
                    diff[i] = capacities[i] - flow[i]
        diffRel = {}
        for i in path:
            diffRel[i] = diff[i]
        m = min(diffRel,key=diffRel.get)
        time = 0
        for i in path:
            flow[i] = flow[i] + diff[m]
            time += flightDict[i][1]
            #print 'time is =',time
        timeArray.append(time)
        stuffToRemove = []
        for i in flow:
            if capacities[i] - flow[i] <= 0:
                (a,b) = i
                if b in G[a]:
                    G[a].remove(b)
                    #print G
        path = dfs(G,start,end)
        print path

    final = 0
    #print 'sink = ',othAdjList[start]
    for i in othAdjList[start]:
        #print 'finding final'
        final += flow[(start,i)]
        #print 'flow=',flow

    if final >= population:
        return max(timeArray)
    else:
        return final
        

def findSmallestT():
    start = eastIndices[0]
    end = westIndices[0]
    population = eastPop[0]
    #found = False
    T = 1
    print maxFlowPathForT(start,end,population,T)

findSmallestT()

