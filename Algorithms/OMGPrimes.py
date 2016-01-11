M,N = map(int,raw_input().split())
nums = map(int,raw_input().split())

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
Gf = {}
cR = {}

# Get adjList-- it's a bipartite graph. S1 = odd vertices, S2 = even vertices
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
                        pairs[j] = ['E']
                        if -1 not in backpairs:
                            backpairs['E'] = [j]
                        else:
                            backpairs['E'].append(j)
                else:
                    pairs[i].append(j)
                    if j not in backpairs:
                        backpairs[j] = [i]
                    else:
                        backpairs[j].append(i)
                    backpairs[j].append(i)
                    # -1 is end vertex
                    if j not in pairs:
                        pairs[j] = ['E']
                        backpairs['E'].append(j)
    # -2 is start vertex
    pairs['S'] = []
    for i in pairs:
        if (i != 'S') and (i%2 == 0) :
            pairs['S'].append(i)
	    if i not in backpairs:
		backpairs[i] = ['S']
	    else:
		backpairs[i].append('S')
    return (pairs,backpairs)

(G,backG) = findPrimePairs()

def cBfs():
    vis = {}
    Q = []
    Q.append('S')
    vis['S'] = 1
    while len(Q) > 0:
	u = Q.pop(0)
        if u in G:
	    for v in Gf[u]:
		if (v not in vis):
		    vis[v] = 1
		    Q.append(v)
		    if v == 'E':
			return True
    return False

def initGf():
    for u in G:
        for v in G[u]:
            if u not in Gf:
                Gf[u] = [v]
            else:
                Gf[u].append(v)
    for u in backG:
        for v in backG[u]:
            if u not in Gf:
                Gf[u] = [v]
            else:
                Gf[u].append(v)
initGf()
		
# We will implement Ford Fulkerson to find max flow starting at S and going to E
f = {}
for u in G:
    for v in G[u]:
	f[(u,v)] = 0
	cR[(u,v)] = 1
	cR[(v,u)] = 1
	
# BFS from 'S' to 'E'
def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def bfs():
    parent = {}
    vis = {}
    queue = []
    queue.append('S')
    vis['S'] = 1
    while queue:
        u = queue.pop(0)
        if u == 'E':
            return backtrace(parent, 'S', 'E')
        for v in Gf.get(u, []):
	    if v not in vis:
		vis[v] = 1
		parent[v] = u # <<<<< record its parent
		if v == 'E':
		    return backtrace(parent, 'S', 'E')
		queue.append(v)
	    
        
def FF():
    flow = 0
    while (cBfs()):
	path = bfs()
	#print path
	if (not path) or (path == []):
	    break
	m = 1000000000
	l = len(path)
	for i in range(l-1):
	    u = path[i]
	    v = path[i+1]
	    m = min(cR[(u,v)],m)
	flow += m
	# Update flows 
	for i in range(l-1):
	    u = path[i]
	    v = path[i+1]
	    cR[(u,v)] -= m
	    if cR[(u,v)] <= 0:
		Gf[u].remove(v)
	    cR[(v,u)] += m
	
    return flow

print FF()
