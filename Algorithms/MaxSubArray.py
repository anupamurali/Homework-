def findIntervals(l,r,middle):
    if l < middle:
        if r <= middle:
            firstl = l
            firstr = r
            secondl = 1
            secondr = 0
        else:
            firstl = l
            firstr = middle
            secondl = 0
            secondr = r - (middle + 1)
    elif l == middle:
        firstl = 1
        firstr = 0
        secondl = 0 
        secondr = r - (middle + 1)
    else:
        firstl = 1
        firstr = 0
        secondl = l - (middle + 1)
        secondr = r - (middle + 1)

    return (firstl,firstr,secondl,secondr)

def findMaxSubArray(K,l1,r1,l2,r2,newDist):
    middle = pow(2,K-1)-1
    if l1 >= l2 and r1 <= r2:
        return r1 - l1
    if l2 >= l1 and r2 <= r1:
        return r2 - l2
    
    if l1 > l2 and r2 > l1:
        intersection = r2 - l1
    elif l2 > l1 and r1 > l2:
        intersection = r1 - l2
    else:
        intersection = 0

    newDist = max(intersection,newDist)
        
    if middle < newDist:
        return newDist

    (firstl1,firstr1,secondl1,secondr1) = findIntervals(l1,r1,middle)
    (firstl2,firstr2,secondl2,secondr2) = findIntervals(l2,r2,middle)
        
    if firstr1 - firstl1 > newDist:
        if firstr2 - firstl2 > newDist:
            newDist = max(newDist,findMaxSubArray(K-1,firstl1,firstr1,firstl2,firstr2,newDist))
        if secondr2 - secondl2 > newDist:
            newDist = max(newDist,findMaxSubArray(K-1,firstl1,firstr1,secondl2,secondr2,newDist))
    if secondr1 - secondl1 > newDist:
        if firstr2 - firstl2 > newDist:
            newDist = max(newDist,findMaxSubArray(K-1,secondl1,secondr1,firstl2,firstr2,newDist))
        if secondr2 - secondl2 > newDist:
            newDist = max(newDist,findMaxSubArray(K-1,secondl1,secondr1,secondl2,secondr2,newDist))

    return newDist
    
def readInput():
    K = map(int,raw_input().split())[0]
    l1,r1,l2,r2 = map(long,raw_input().split())

    print findMaxSubArray(K,l1,r1,l2,r2,0)

readInput()
