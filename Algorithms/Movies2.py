# Read in inputs
N,K,T = map(int,raw_input().split())
A = map(int,raw_input().split())
B = map(int,raw_input().split())

# Possible ratings
Numbers = [i for i in range(0,T+1)]

# Distribution of ratings 
def findDist(arr):
    distDict = {}
    for i in Numbers:
        count = 0
        for j in arr:
            if i == j:
                count = count + 1

        distDict[i] = float(count)

    return distDict

# Number of sets of ratings of size k in arr that sum to x
count = 0
def numSum(arr,x,k,numElem,index,currSum):
    if len(arr) < index or currSum > x or numElem > k:
        return 
    for i in range(index,len(arr)):
        if (currSum + arr[i] == x) and (numElem == k):
            print 'here'
            count += 1
            print count
        elif (currSum + arr[i] < x) and numElem < k:
            print count
            print 'here again'
            numSum(arr,x,k,numElem + 1,i + 1,currSum + arr[i])

# Find distribution of ratings of A and B
ADist = findDist(A)
BDist = findDist(B)




