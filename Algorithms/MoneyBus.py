# Get adjacency list of graph
def getNeighbors(edges):
    neighbors = {}
    for e in edges:
        (u,v) = e
        if v not in neighbors:
            neighbors[v] = [u]
        else:
            neighbors[v].append(u)

def readInput():
    N,E = map(int,raw_input().split())
    passengersArray = []
    edges = {}

    passengersArray = map(int,raw_input().split())

    for i in range(E):
        I,J,L = map(int,raw_input().split())
        edges[(I-1,J-1)] = L

    neighbors = getNeighbors(edges)
    
    return (neighbors,passengersArray,edges,N,E)

(adjList,passengers,edges,N,E) = readInput()
cost = {}
traversedEdges = {}
previous = {}
for e in edges:
    traversedEdges[e] = False

def costliestPath(u,k):
    if u == 0 and k == 0:
        cost[u] = passengers[u]
        return cost[u]
    elif u != 0 and k == 0:
        cost[u] = -1000000000000000
    else:
        maxLen = -1000000000000000
        for v in adjList[u]:
            if costliestPath(v,k-1) + passengers[v] - edges[(v,u)] > maxLen:
                print 'here'
                maxLen = costliestPath(v,k-1) + passengers[v] - edges[(v,u)]
                previous[u] = v

        if costliestPath(u,k-1) > maxLen:
            cost[u] = costliestPath(u,k-1)
            traversedEdges[(v,u)] = True
            return costliestPath(u,k-1)
        else:
            cost[u] = maxLen
            traversedEdges[(v,u)] = True
            return maxLen

def findCostliest():
    print traversedEdges
    print cost
    for e in traversedEdges:
        (u,v) = e
        print e
        if cost[u] - traversedEdges[e] + passengers[v] > cost[v]:
            return 'infinity'
    if cost[N-1] == -1000000000000000:
        return 'none'
    else:
        return cost[N-1]

                    
def main():
    print findCostliest()

main()
