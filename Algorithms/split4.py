K = int(raw_input())
A = map(int,raw_input().split())
B = map(int,raw_input().split())
C = map(int,raw_input().split())
D = map(int,raw_input().split())
I = zip(A,B,C,D)
sortedI = sorted(I,key=lambda i:i[3])
largest = (-10000,-1,1000000000,10000000000)
sortedI.append(largest)

# is j nested in i?
def isContained(i,j):
    (a,b,c,d) = sortedI[i]
    (ai,bi,ci,di) = sortedI[j]
    if (b <= ai) and (di <= c):
        return True
    return False

def intervalsInGap(I):
    intervals = []
    (a,b,c,d) = sortedI[I]
    for i in range(I):
        if isContained(I,i):
            intervals.append(i)
    return intervals

def prevArray(X):
    P = {}
    L = len(X)
    for i in reversed(xrange(L)):
        (a,b,c,d) = sortedI[i]
        for j in reversed(xrange(i)):
            (ai,bi,ci,di) = sortedI[j]
            if di <= a:
                P[i] = j
    return P

W = {}
W[0] = 1
OPT = {}
M = {}
