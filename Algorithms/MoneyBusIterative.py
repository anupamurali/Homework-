def swapSourceToBeginning(edgeArray,E):
    if edgeArray[0][0] != 0:
        for i in range(E):
            if edgeArray[i][0] == 0:
                notSource = edgeArray[0]
                edgeArray[0] = edgeArray[i]
                edgeArray[i] = notSource
                
# Given edges, return dictionary with keys as start edges
# with array of incident vertices as value (adjacency list)
def getNeighbors(edges):
    neighbors = {}
    for e in edges:
        (start,end) = e
        if start not in neighbors:
            neighbors[start] = [end]
        else:
            neighbors[start].append(end)

    return neighbors

# Given adjacency list, number of passengers, and edge lengths,
# find longest path
def longestPath(adjList,passengers,edges,edgeArray,N,E):
    cost = {}
    prev = {}
    nextVertex = {}
    
    # Initialize cost
    for v in range(N):
        if v == 0:
            cost[v] = passengers[v]
        else:
            cost[v] = -1000000000000000
            
    for i in range(1,N):
        for e in edgeArray:
            (u,v) = e
            if cost[u] - edges[e] + passengers[v] > cost[v]:
                cost[v] = cost[u] - edges[e] + passengers[v]
     
    if cost[N-1] == -1000000000000000:
        return 'none'

    for e in edges:
        (u,v) = e
        if cost[u] - edges[e] + passengers[v] > cost[v]:
            return 'infinity'

    return cost[N-1]
    
def readInput():
    N,E = map(int,raw_input().split())
    passengersArray = []
    edges = {}

    passengersArray = map(int,raw_input().split())

    for i in range(E):
        I,J,L = map(int,raw_input().split())
        edges[(I-1,J-1)] = L

    edgeArray = edges.keys()
    swapSourceToBeginning(edgeArray,E)

    # Dictionary containing edges as tuples that map to their "prices"
    edgePrices = {}

    for e in edges:
        (start,end) = e
        weight = edges[e]
        if start == 0:
            edgePrices[(start,end)] = passengersArray[start] + passengersArray[end] - weight
        else:
            edgePrices[(start,end)] = passengersArray[end] - weight
   
        
    neighbors = getNeighbors(edges)

    costliestPath = longestPath(neighbors,passengersArray,edges,edgeArray,N,E)
    
    print costliestPath
    

readInput()
    
