M,N = map(int,raw_input().split())
nums =  sorted(map(int,raw_input().split()))

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

"""def findEdges():
    pairs = []
    for i in nums:
        for j in nums:
            if (i != j) and ((int(i) + int(j)) in primeList):
                    if i % 2 == 0:
                        pairs.append((i,j))
                    else:
                        pairs.append((j,i))
    return pairs"""

# Get adjList-- it's a bipartite graph. S1 = odd vertices, S2 = even vertices
def findPrimePairs():
    pairs = {}
    for i in nums:
        for j in nums:
            if (i != j) and ((i + j) in primeList) and (i % 2 == 0):
                if i not in pairs:
                    pairs[i] = [j]
                    # -2 is end vertex
                    if j not in pairs:
                        pairs[j] = [-2]
                else:
                    pairs[i].append(j)
                    # -2 is end vertex
                    if j not in pairs:
                        pairs[j] = [-2]
    # -1 is start vertex
    pairs[-1] = []
    for i in pairs:
        if int(i) % 2 == 0:
            pairs[-1].append(i)

    return pairs


G = findPrimePairs()
#print E

def getEdges(path):
    tuplePath = []
    n = len(path)
    for i in range(0,n-1):
        tuplePath.append((path[i],path[i+1]))
    return tuplePath


def cBfs():
    vis = {}
    Q = []
    Q.append(-1)
    vis[-1] = 1
    while len(Q) > 0:
	u = Q.pop(0)
        if u in G:
	    for v in G[u]:
		if v not in vis:
		    vis[v] = 1
		    Q.append(v)
		    if v == -2:
			return True
    return False

# BFS from -1 to -2
def bfs():
    Q = []
    Q.append([-1])
    while len(Q) > 0:
        path = Q.pop(0)
        u = path[-1]
        if u == -2:
            return getEdges(path)
        for v in G[u]:
            newPath = list(path)
            if v not in newPath:
                newPath.append(v)
            Q.append(newPath)
    return []
#print G
# Ford Fulkerson on G to find max-flow, which is also maximum matching
def FF():
    maxFlow = 0
    f = {}
    for u in G:
        for v in G[u]:
            f[(u,v)] = 0
            f[(v,u)] = 0
    path = bfs()
    while path and path != []:
        print path
        d = {}
        for e in f:
            d[e] = 1 - f[e]
            #print d
        pathD = {}
        for e in path:
            pathD[e] = d[e]
        m = min(pathD,key=pathD.get)
        maxFlow += d[m]
        for e in path:
            (u,v) = e
            f[e] += d[m]
            f[(v,u)] -= d[m]

        # Find residual graph
        for u in G:
            for v in G[u]:
                if (1 - f[(u,v)] <= 0):
                    if v in G[u]:
                        G[u].remove(v)
        print G
        path = bfs()
    return maxFlow

print 'graph = ',G
found = False
if not cBfs():
    print 0
    found = True

if not found:
    print FF() 

