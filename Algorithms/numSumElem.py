N,K,T = map(int,raw_input().split())
A = map(int,raw_input().split())
B = map(int,raw_input().split())

def findSumDict(arr):
    sumDict = {}
    sumDict[(0,0,0)] = 1
    for i in xrange(T):
        count = 0
        for j in xrange(N):
            if i == arr[j]:
                count = count + 1
        if count > 0:
            sumDict[(j+1,arr[j],1)] = count

    return sumDict

ADict = findSumDict(A)
BDict = findSumDict(B)


def numSumA(n,x,k):
    if k < 0 or x < 0:
        return 0
    elif n == 0:
        if x == 0 and k == 0:
            return 1
        else:
            return 0
    else:
        if (n,x,k) in ADict:
            return ADict[(n,x,k)]
        else:
            ADict[(n,x,k)] = numSumA(n-1,x,k) + numSumA(n-1,x-A[n-1],k-1)
            return ADict[(n,x,k)]

        
def numSumB(n,x,k):
    if k < 0 or x < 0:
        return 0
    elif n == 0:
        if x == 0 and k == 0:
            return 1
        else:
            return 0
    else:
        if (n,x,k) in BDict:
            return BDict[(n,x,k)]
        else:
            BDict[(n,x,k)] = numSumB(n-1,x,k) +  numSumB(n-1,x-B[n-1],k-1)
            return BDict[(n,x,k)]

total = 0
foundDictA = {}
foundDictB = {}
K_T = K*T
for i in xrange(K_T+1):
    if i in foundDictA:
        ANum = foundDictA[i]
    else:
        ANum = numSumA(N,i,K)
    if 2*i <= K_T:
        for j in xrange(2*i+1):
            if j in foundDictB:
                total = total +ANum*foundDictB[j]
            else:
                foundDictB[j] = numSumB(N,j,K)
                total = total + ANum*foundDictB[j]
    else:
        for j in xrange(K_T+1):
            if j in foundDictB:
                total = total + ANum*foundDictB[j]
            else:
                foundDictB[j] = numSumB(N,j,K)
                total = total + ANum*foundDictB[j]
            
from math import factorial

def C(n,k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

denominator = C(N,K)*C(N,K)

import sys
sys.stdout.write("%.8f" % (float(total)/float(denominator)))
