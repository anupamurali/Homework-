N,E,W,F = map(int,raw_input().split())
eastIndices = map(int,raw_input().split())
eastPop = map(int,raw_input().split())
eastCityInf = {}
totalPop = 0
for i in range(E):
    eastCityInf[eastIndices[i]] = eastPop[i]
    totalPop += eastPop[i]

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

def cBfs(g,start):
    vis = {}
    Q = []
    Q.append(start)
    vis[start] = 1
    while len(Q) > 0:
	u = Q.pop(0)
	if u in g:
	    for v in g[u]:
		if v not in vis:
		    vis[v] = 1
		    Q.append(v)
		    if v in westIndices:
			return True
    return False

def bfs(g,start):
    Q = []
    Q.append([start])
    while len(Q) > 0:
	    #print 'hello'
        path = Q.pop(0)
	#print path
        u = path[-1]
        if u[0] in westIndices:
            return getEdges(path)
        for v in g[u]:
            newPath = list(path)
	    if v not in newPath:
		newPath.append(v)
            Q.append(newPath)
    return []


#dictionary
#key = tuple of city and timestamp
#returns dictionary w/ key = tuples, returns flights that can be reached within this time
G = {}
eastG = []
allEdges = []
for i in range(N):
    if i in eastIndices:
	    G[(-1,0)] = [(i,0)]
	    allEdges.append(((-1,0),(i,0)))
	    flights[(-1,i)] = (eastCityInf[i],0)
for i in range(N):
    G[(i,0)] = [(i,1)]
    allEdges.append(((i,0),(i,1)))
for i in range(N):
    G[(i,1)] = []
stuffToAdd = []
for i in G:
    if i[0] != -1:
	for j in flights:
	    if j[0] == i[0]:
		if (i[1] + flights[j][1]) <= 1:
		    new = (j[1],i[1] + flights[j][1])
		    G[i].append((j[1],i[1] + flights[j][1]))
		    stuffToAdd.append((j[1],i[1] + flights[j][1]))
		    if (i,new) not in allEdges:
			allEdges.append((i,new))

for i in stuffToAdd:
    G[i] = []

def FF(g,start):
	#print 'hello'
    final = 0
    f = {}
    c = {}
    for i in allEdges:
        (u,v) = i
        f[i] = 0
        f[(v,u)] = 0
	if (u[0] != v[0]):
		c[i] = flights[(u[0],v[0])][0]
	else:
		c[i] = float('inf')
        path = bfs(g,start)
	#print path
	#print allEdges
    while path and (path != []):
        d = {}
	for i in allEdges:
	    d[i] = c[i] - f[i] 
        pathD = {}
        for i in path:
            pathD[i] = d[i]
        m = min(pathD,key=pathD.get)
        final += pathD[m]
        for i in path:
            (u,v) = i
            f[i] += d[m]
            f[(v,u)] -= d[m]
            
        # Find residual graph
        for i in allEdges:
	    if (c[i] - f[i] <= 0):
		if i[1] in g[i[0]]:
                    g[i[0]].remove(i[1])
		#print g
        path = bfs(g,start)
    return final

def addLayer(time):
    global G
    #print 'time=',time
    #print 'graph so far is = ',G
    for i in range(N):
	G[(i,time)] = []
	G[(i,time-1)].append((i,time))
	allEdges.append(((i,time-1),(i,time)))
    stuffToAdd = []
    for i in G:
	for j in flights:
	    if i[0] == j[0]:
		if (i[1] + flights[j][1]) <= time:
			#if time == 2:
			#print 'for 2',i,j,flights[j]
		    new = (j[1],i[1] + flights[j][1])
			#print new
		    if (new not in G[i]):
			G[i].append(new)
		    if (i,new) not in allEdges:
			    allEdges.append((i,new))
		    if (new not in G):
			stuffToAdd.append(new)


found = False
T = 1
FL = {}
for i in flights:
    if i[0] not in FL:
        FL[i[0]] = [i[1]]
    else:
        FL[i[0]].append(i[1])

for i in eastIndices:
    if (cBfs(FL,i) == False):
	found = True
	T = -1

while found == False:
    path = bfs(G,(-1,0))
    if (not path) or (path == []):
	T += 1
        addLayer(T)
    else:
        flow = FF(G,(-1,0))
        #print 'flow =',flow
        if totalPop <= flow:
                found = True
        else:
	    T += 1
            addLayer(T)

print T

