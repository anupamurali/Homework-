N,K,T = map(int,raw_input().split())
A = map(int,raw_input().split())
B = map(int,raw_input().split())

ADict = {}
BDict = {}

for i in range(0,T+1):
    count = 0
    for j in A:
        if i == j:
            count = count + 1
    ADict[i] = float(count)/float(N)

for i in range(0,T+1):
    count = 0
    for j in B:
        if i == j:
            count = count + 1

    BDict[i] = float(count)/float(N)

PBEqDict = {}

for i in range(0,T+1):
    PBEqDict[(i,1)] = BDict[i]
    
def PBEqual(x,k):
    
    if (x,k) in PBEqDict:
        return PBEqDict[(x,k)]
    else:
        total = float(0)
        for i in range(0,T+1):
            total = float(total) + float(BDict[i]*PBEqual(x-i,k-1))
        PBEqDict[(x,k)] = total
    
PAGDict = {}

for i in range(0,T+1):
    PAGDict[(i,1)] = ADict[i]

def PAGreater(x,k):
    print PAGDict
    print (x,k)
    
    if x == 0:
        if N > 0:
            return float(1)
        else:
            return float(0)
        
    if (x,k) in PAGDict:
        print 'here'
        return PAGDict[(x,k)]
    else:
        total = float(0)
        for i in range(0,T+1):
            total = float(total) + float(ADict[i]*PAGreater(x-i,k-1))

        PAGreater[(x,k)] = PAGreater[(x,k-1)] + total


def findProbability():
    totalProb = 0
    for i in range(0,2*N*T+1):
        totalProb = float(totalProb) + float(PAGreater(int(i/2),K)*PBEqual(i,K))

    return totalProb

total = findProbability()

print total


