import math
prime = 2795209
pow10Dict = {}

def modPow10P(n):
    if n in pow10Dict:
        return pow10Dict[n]
    elif n <= 6:
        pow10Dict[n] = 10**n
        return pow10Dict[n]
    else:
        if n % 2 == 0:
            pow10Dict[n] = (modPow10P(int(math.ceil(n/2)))*modPow10P(int(math.floor(n/2))))%prime
            return pow10Dict[n]
        else:
            pow10Dict[n] = (10*modPow10P(n-1))%prime
            return pow10Dict[n]
        
def modP(N):
    L = len(N)
    T = 0
    for i in xrange(L):
        T = T + ((ord(N[L-i-1])-ord('0'))*modPow10P(i))%prime
    return str(T)

def findFinalMod(N):
    prevN = N
    N = modP(N)
    while prevN != N:
        prevN = N
        N = modP(N)
    return N
#print findFinalMod('90643571395')
        
import random
s = []
for i in range(2500):
    a = random.randint(1,9)
    s.append(a)

    #print str(s)
    #print modP(str(s))
    
def checkMult2(N,M,P):
    n1 = findFinalMod(N)
    m1 = findFinalMod(M)
    a1 = findFinalMod(P)
    nm1 = findFinalMod(str(int(n1)*int(m1)))
    if (nm1 != a1):
        return False
    else:
        return True
    
def readInput():
    K = int(raw_input())
    NMP = []
    for i in range(K):
        N,M,P = raw_input().split()
        NMP.append((N,M,P))

    for i in NMP:
        (N,M,P) = i
        if checkMult2(N,M,P):
            print 'yes'
        else:
            print 'no'

readInput()
