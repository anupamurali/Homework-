K = int(raw_input())
A = map(int,raw_input().split())
B = map(int,raw_input().split())
C = map(int,raw_input().split())
D = map(int,raw_input().split())
I = zip(A,B,C,D)
sortedI = sorted(I,key=lambda i:i[3])
otherI = sortedI
otherI.append((-10000,-1,1000000000,10000000000))


def isContained(i,j):
    (a,b,c,d) = sortedI[i]
    (ai,bi,ci,di) = sortedI[j]
    if (b <= ai) and (di <= c):
        return True
    return False

def intervalsInGap(I):
    intervals = []
    P = {}
    for i in range(I):
        while True:
            i = i-1
            if i == -1:
                P[I] = -1
                break
            if isContained(I,i):
                intervals.append(i)
                #print otherI,i,I
            if (otherI[i][3] <= otherI[I][0]) and isContained(I,i):
                P[I] = i
                break
    return (intervals,P)

def prevArray(X):
    P = {}
    L = len(X)
    start = X[0]
    for i in X:
        (a,b,c,d) = sortedI[i]
        for j in reversed(xrange(start,i)):
            (ai,bi,ci,di) = sortedI[j]
            if di <= a:
                P[i] = j
                break
    return P

W = {}
W[0] = 1
M = {}

def maxArray(X,P):
    O = {}
    L = len(X)
    if (tuple(X) in M):
        return M[tuple(X)]
    elif L == 0:
        M[tuple(X)] = 0
        return 0
    elif L == 1:
        O[X[0]] = 1
        M[tuple(X)] = 1
        return 1
    else:
        O[X[0]] = 1
        #P = prevArray(X)
        #previous = X[0]
        for i in X:
            if i == X[0]:
                O[i] = 1
            elif i not in P:
                print 'here'
                O[i] = max(W[i],O[previous])
            elif i != -1:
                O[i] = max(W[i]+O[P[i]],O[previous])
            else:
                O[i] = max(W[i],O[previous])
            previous = i
        M[tuple(X)] = O[X[L-1]]
        return M[tuple(X)]

for i in range(1,K):
    (X,P) = intervalsInGap(i)
    W[i] = 1 + maxArray(X,P)
(X,newP) = intervalsInGap(K)
print maxArray(range(K),newP)
