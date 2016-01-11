K = int(raw_input())
A = map(int,raw_input().split())
B = map(int,raw_input().split())
C = map(int,raw_input().split())
D = map(int,raw_input().split())
I = zip(A,B,C,D)
sortedI = sorted(I,key=lambda i:i[3])
largest = (-10000,-1,1000000000,10000000000)
sortedI.append(largest)

intervalDict = {}
def intervalsInGap(I):
    intervals = []
    (a,b,c,d) = sortedI[I]
    for i in range(I):
        (ai,bi,ci,di) = sortedI[i]
        if (ai >= b) and (di <= c):
            intervals.append(i)
    intervalDict[I] = intervals
    return intervals

def Prev(A):
    #print A[I]
    L = len(A)
    for i in reversed(xrange(L)):
        

def findP(A,x,y):
    P = {}
    L = len(A)
    #print A,'hiii'
    for i in range(L):
        P[i] = Prev(i,A,x,y)
    return P

def maxArray(A,j):
    W[j] = max(1+W[P[j]],W[j-1])
    
