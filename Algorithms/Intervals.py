def findNumGroups(startEndList,K):
    numGroups = []
    depth = 0
    for i in range(2*K):
        if startEndList[i] == 1:
            depth = depth + 1
            numGroups.append(depth)
        elif startEndList[i] == 0:
            depth = depth - 1
            numGroups.append(depth)

    return max(numGroups)
        

def readInput():
    lst = map(int,raw_input().split())
    K = lst[0]

    startTimes = map(int,raw_input().split())
    endTimes = map(int,raw_input().split())

    times = []
    
    for i in startTimes:
        times.append((i,1))
    for i in endTimes:
        times.append((i,0))

    sortedTimes = sorted(times,key=lambda times:(times[0],times[1]))
    startEndList = list(i[1] for i in sortedTimes)
    
    numGroups = findNumGroups(startEndList,K)
    
    intervals = zip(startTimes,endTimes)
    
    print numGroups

readInput()
