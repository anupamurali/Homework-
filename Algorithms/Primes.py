M,N = map(int,raw_input().split())
nums = sorted(map(int,raw_input().split()))

def findPrimes(n):
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * (n/3)
    for i in xrange(1,int(n**0.5)/3+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k/3      ::2*k] = [False] * ((n/6-k*k/6-1)/k+1)
        sieve[k*(k-2*(i&1)+4)/3::2*k] = [False] * ((n/6-k*(k-2*(i&1)+4)/6-1)/k+1)
    return [2,3] + [3*i+1|1 for i in xrange(1,n/3-correction) if sieve[i]]

primeList = findPrimes(2*M)

def findPrimePairs():
    pairs = {}
    backpairs = {}
    for i in nums:
        for j in nums:
            if (i != j) and ((i + j) in primeList) and (i % 2 == 0):
                if i not in pairs:
                    pairs[i] = [j]
                    if j not in backpairs:
                        backpairs[j] = [i]
                    else:
                        backpairs[j].append(i)
                    # -1 is end vertex
                    if j not in pairs:
                        pairs[j] = [-1]
                        if -1 not in backpairs:
                            backpairs[-1] = [j]
                        else:
                            backpairs[-1].append(j)
                else:
                    pairs[i].append(j)
                    if j not in backpairs:
                        backpairs[j] = [i]
                    else:
                        backpairs[j].append(i)
                    backpairs[j].append(i)
                    # -1 is end vertex
                    if j not in pairs:
                        pairs[j] = [-1]
                        backpairs[-1].append(j)
    # -2 is start vertex
    pairs[-2] = []
    for i in pairs:
        if int(i) % 2 == 0 and (int(i) != -2) :
            pairs[-2].append(i)

    return (pairs,backpairs)

(G,backG) = findPrimePairs()
#print G

def getEdges(path):
    tuplePath = []
    n = len(path)
    for i in range(0,n-1):
        tuplePath.append((path[i],path[i+1]))
    return tuplePath


def cBfs():
    vis = {}
    Q = []
    Q.append(-2)
    vis[-2] = 1
    while len(Q) > 0:
	u = Q.pop(0)
        if u in G:
	    for v in Gf[u]:
		if v not in vis:
		    vis[v] = 1
		    Q.append(v)
		    if v == -1:
			return True
    return False

# BFS from -2 to -1
def bfs(Gf,cR):
    Q = []
    Q.append([-2])
    while len(Q) > 0:
        path = Q.pop(0)
        u = path[-1]
        if u == -1:
            return path
        for v in Gf[u]:
            newPath = list(path)
            print newPath
            if v not in newPath:
                newPath.append(v)
            Q.append(newPath)
    return []

f = {}
c = {}
for u in G:
    for v in G[u]:
        f[(u,v)] = 0
        c[(u,v)] = 1
        
# Residual graph
cR = {}
Gf = {}
def initGf():
    for u in G:
        for v in G[u]:
            if u not in Gf:
                Gf[u] = [v]
                cR[(u,v)] = c[(u,v)] - f[(u,v)]
            else:
                Gf[u].append(v)
                cR[(u,v)] = c[(u,v)] - f[(u,v)]
    for u in backG:
        for v in backG[u]:
            if u not in Gf:
                Gf[u] = [v]
                cR[(u,v)] = f[(v,u)]
            else:
                Gf[u].append(v)
                cR[(u,v)] = f[(v,u)]
initGf()
#print Gf
def updateGf():
    toRemove = {}
    for u in G:
        for v in G[u]:
            cR[(u,v)] = c[(u,v)] - f[(u,v)]
            if cR[(u,v)] <= 0:
                toRemove[(u,v)] = 1
    for u in backG:
        for v in backG[u]:
            cR[(u,v)] = f[(v,u)]
            if cR[(u,v)] <= 0:
                toRemove[(u,v)] = 1
    for i in toRemove:
        (u,v) = i
        if v in Gf[u]:
            Gf[u].remove(v)
vis = {}
def FF():
    global Gf
    path = bfs(Gf,cR)
    flow = 0
    while path and (path != []):
        l = len(path)
        cP = {}
        for i in range(l-1):
            u = path[i]
            v = path[i+1]
            cP[(u,v)] = cR[(u,v)]
        m = cP[min(cP,key=cP.get)]
        flow += m
        for i in range(l-1):
            e = (path[i],path[i+1])
            if (path[i] in G) and (path[i+1] in G[path[i]]):
                f[e] += m
                cR[e] -= m
            if (path[i] in backG) and (path[i+1] in backG[u]):
                cR[e] += m
        
                #updateGf()
        path = bfs(Gf,cR)
    return flow
    

found = False
if (not cBfs()):
    found = True
    print 0
if not found:
    print FF()
