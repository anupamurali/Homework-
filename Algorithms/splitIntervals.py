K = int(raw_input())
A = map(int,raw_input().split())
B = map(int,raw_input().split())
C = map(int,raw_input().split())
D = map(int,raw_input().split())
I = zip(A,B,C,D)
sortedI = sorted(I,key=lambda i:i[3])

weights = {}

def weight(I):
    if I in weights:
        return weights[I]
    elif I == 0:
        weights[I] = 0
        return weights[I]
    else:
        (a,b,c,d) = sortedI[I]
        maxWeight = 0
        weights[I] = maxWeight
        for i in range(I):
            (ai,bi,ci,di) = sortedI[i]
            #print (sortedI[i],sortedI[I])
            if (ai >= b) and (di <= c) and (weight(i) >= maxWeight):
                maxWeight = weight(i)
                weights[I] = maxWeight + 1
        return weights[I]


for i in range(K):
    weights[i] = weight(i)

print sortedI
#print weights

P = {}
def Prev(I):
    (a,b,c,d) = sortedI[I]
    for i in reversed(xrange(I)):
        (ai,bi,ci,di) = sortedI[i]
        if (ai >= b) and (di <= c):
            #print 'hello 1'
            P[I] = i
            return P[I]
        elif (di <= a):
            print i,I
            #print 'hello again'
            P[I] = i
            return P[I]


for i in range(K):
    P[i] = Prev(i)

print P

FArray = {}

def F(I):
    if not(I):
        #print 'yoo'
        return 0
    elif I == 0:
        #print 'here'
        return 1
    elif I in FArray:
        #print 'hello there',I
        return FArray[I]
    else:
        FArray[I] = max(1 + weights[I] + F(Prev(I)),F(I-1))
        return FArray[I]
#print 'right here',weights
print F(K-1)

    
    
    
    

