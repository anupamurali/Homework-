K = int(raw_input())
A = map(int,raw_input().split())
B = map(int,raw_input().split())
C = map(int,raw_input().split())
D = map(int,raw_input().split())
I = zip(A,B,C,D)
sortedI = sorted(I,key=lambda i:i[3])

# is j nested in i?
def isContained(i,j):
    (a,b,c,d) = sortedI[i]
    (ai,bi,ci,di) = sortedI[j]
    if (b <= ai) and (di <= c):
        return True
    return False

def intervalsInGap(I):
    intervals = []
    for i in range(I):
        if isContained(I,i):
            intervals.append(i)
    return intervals

W = {}
W[0] = 1
M = {}
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

def maxArray(X):
    O = {}
    O[0] = 1
    L = len(X)
    if (tuple(X) in M):
        return M[tuple(X)]
    elif L == 0:
        M[tuple(X)] = 0
        return M[tuple(X)]
    elif L == 1:
        M[tuple(X)] = 1
        return M[tuple(X)]
    else:
        P = prevArray(X)
        for i in range(1,L):
            if i in P:
                O[i] = max(W[i]+O[P[i]],O[i-1])
            else:
                #print 'hi',i,W[i]
                O[i] = max(W[i],O[i-1])
        M[tuple(X)] = O[L-1]
        #print O
        return M[tuple(X)]
    
for i in range(1,K):
    X = intervalsInGap(i)
    W[i] = 1 + maxArray(X)


W[max(W.keys(), key=lambda x: W[x])] 
print maxArray(range(K))
#print sorted-

#print M    
#print W
#print maxArray(range(K))
