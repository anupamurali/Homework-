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
#print 'primes =',primeList
#print nums

# Find all pairs that sum up to primes
def findPrimePairs():
    pairs = {}
    for i in nums:
        for j in nums:
            if (i != j) and ((i + j) in primeList):
                if j in pairs:
                    if i in pairs[j]:
                        break
                elif i not in pairs:
                    pairs[i] = [j]
                else:
                    if j not in pairs[i]:
                        pairs[i].append(j)

    return pairs

adjList = findPrimePairs()

import random
import copy
def randMaxPairs(L):
    #print adjList
    lst = copy.deepcopy(L)
    vis = {}
    maxPairs = []
    same = False
    prev = 0
    while (not same) and (len(lst) > 0):
        K = len(lst)
        #print 'this is len = ',K
        if (prev == K):
            same = True
        prev = K
        i = random.randrange(K)
        count = 0
        select = 0
        for u in lst:
            if i == count:
                select = u
                break
            count += 1

        l = len(lst[select])
        #print select,l
        j = random.randrange(l)
        v = lst[select][j]
        if (select not in vis) and (v not in vis):
            maxPairs.append((select,v))
            vis[select] = 1
            vis[v] = 1
            if select in lst:
                lst.pop(select)
            if v in lst:
                lst.pop(v)

    return maxPairs

def greedyMaxPairs():
    vis = {}
    pairs = []
    for i in adjList:
        for j in adjList[i]:
            if (i not in vis) and (j not in vis):
                vis[i] = True
                vis[j] = True
                pairs.append((i,j))
    return len(pairs)

maxnum = 0
maxArr = []
print 'adj = ',adjList
for i in range(5000):
    curr = randMaxPairs(adjList)
    #print 'current =',curr
    #print len(curr)
    if len(curr) > maxnum:
        maxnum = len(curr)
        #maxArr = curr
        #print max

print max(maxnum,greedyMaxPairs())



        
#print randMaxPairs()
