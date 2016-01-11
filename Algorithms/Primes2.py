M,N = map(int,raw_input().split())
nums =  sorted(map(int,raw_input().split()))

def findPrimes(n):
    """ Input n>=6, Returns a list of primes, 2 <= p < n """
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * (n/3)
    for i in xrange(1,int(n**0.5)/3+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k/3      ::2*k] = [False] * ((n/6-k*k/6-1)/k+1)
        sieve[k*(k-2*(i&1)+4)/3::2*k] = [False] * ((n/6-k*(k-2*(i&1)+4)/6-1)/k+1)
    return [2,3] + [3*i+1|1 for i in xrange(1,n/3-correction) if sieve[i]]

primeList = findPrimes(2*M)
# Find all pairs that sum up to primes
def findPrimePairs():
    pairs = []
    for i in nums:
        for j in nums:
            if (i != j) and ((i + j) in primeList):
                if (j,i) not in pairs:
                    pairs.append((i,j))
    return pairs

def hasEdge(p1,p2):
    if p1[0] == p2[0]:
        return True
    elif p1[0] == p2[1]:
        return True
    elif p1[1] == p2[0]:
        return True
    elif p1[1] == p2[1]:
        return True
    else:
        return False




def findAdj(E):
    adjList = {}
    for i in E:
        adjList[i] = []
    for i in E:
        for j in E:
            if i != j:
                if hasEdge(i,j):
                    adjList[i].append(j)

    return adjList

edges = findPrimePairs()
adjList = findAdj(edges)
lenList = {}

for i in adjList:
    lenList[i] = len(adjList[i])

print lenList

def findMax():
    optPairs = []
    while (len(adjList) > 0):
        opt = min(lenList, key=lenList.get)
        optPairs.append(opt)
        #print 'pre = ',adjList
        if opt in lenList:
            adjList.pop(opt)
            lenList.pop(opt)
            #print opt
        #print 'post =',adjList
        stuffToRemove = []
        for u in adjList:
            if hasEdge(u,opt):
                stuffToRemove.append(u)
            for v in adjList[u]:
                if hasEdge(v,opt):
                    if v in lenList:
                        lenList[u] =- 1

                        #print 'to remove: ',stuffToRemove
        print lenList
        
        for i in stuffToRemove:
            if i in adjList:
                adjList.pop(i)
                lenList.pop(i)

        print 'post =',adjList
            
    return optPairs

print findMax()
