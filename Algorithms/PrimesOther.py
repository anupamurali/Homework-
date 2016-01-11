M,N = map(int,raw_input().split())
nums =  [43, 88, 250, 290, 319, 312, 501, 177, 358, 24, 221, 30, 98, 591, 4, 66, 76, 37, 131, 6, 450, 188, 384, 241, 85, 291, 12, 505, 523, 480, 33, 183, 504, 419, 454, 44, 272, 104, 374, 133, 172, 427, 81, 190, 225, 458, 349, 418, 337, 266, 592, 444, 170, 306, 175, 296, 571, 542, 204, 362, 245, 150, 38, 431, 344, 451, 268, 564, 479, 158, 478, 534, 235, 205, 74, 28, 495, 403, 477, 402, 259, 262, 550, 34, 101, 73, 206, 132, 322, 224, 538, 410, 239, 153, 380, 200, 77, 369, 256, 559, 544, 125, 216, 128, 367, 575, 243, 353, 141, 305, 387, 393, 308, 541, 159, 396, 371, 144, 63, 255, 274, 377, 232, 90, 8, 270, 519, 149, 409, 439, 460, 594, 109, 389, 146, 332, 529, 96, 147, 512, 123, 57, 124, 187, 506, 459, 134, 449, 531, 487, 540, 569, 502, 244, 483, 82, 434, 372, 412, 385, 110, 563, 360, 152, 265, 189, 258, 32, 490, 67, 467, 155, 493, 27, 340, 545, 248, 113, 554, 597, 596, 279, 489, 31, 435, 168, 50, 593, 433, 48, 333, 193, 240, 75, 1, 103, 261, 581, 185, 560, 311, 357, 298, 548, 466, 328, 211, 482, 26, 330, 236, 271, 423, 356, 518, 51, 196, 421, 395, 578, 513, 58, 532, 135, 589, 442, 492, 60, 375, 565, 509, 192, 269, 417, 71, 530, 440, 378, 47, 416, 199, 587, 568, 137, 457, 408, 222, 64, 413, 447, 208, 576, 515, 230, 425, 61, 166, 180, 84, 511, 108, 346, 15, 195, 10, 286, 562, 320, 19, 105, 486, 405, 181, 359, 585, 201, 586, 257, 315, 100, 83, 580, 65, 106, 336, 35, 198, 173, 324, 283, 462, 234, 223, 91, 553, 294, 2, 182, 157, 426]

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

def findEdges():
    pairs = []
    for i in nums:
        for j in nums:
            if (i != j) and ((i + j) in primeList):
                    if i % 2 == 0:
                        pairs.append((i,j))
                    else:
                        pairs.append((j,i))
    return pairs

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
        if i % 2 == 0:
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
            return path
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
        l = len(path)
        d = {}
        for e in f:
            d[e] = 1 - f[e]
        pathD = {}
        for i in range(l-1):
            e = (path[i],path[i+1])
            pathD[e] = d[e]
        m = min(pathD,key=pathD.get)
        maxFlow += d[m]
        for i in range(l-1):
            e = (path[i],path[i+1])
            f[e] += d[m]
            f[(path[i+1],path[i])] -= d[m]

        # Find residual graph
        for u in G:
            for v in G[u]:
                if (1 - f[(u,v)] <= 0):
                    if v in G[u]:
                        G[u].remove(v)
        path = bfs()
    return maxFlow

found = False
if not cBfs():
    print 0
    found = True

if not found:
    print FF()
