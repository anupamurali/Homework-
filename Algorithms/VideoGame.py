############################################################################################
# Vertex Class. Contains coordinates in grid, array of neighboring vertices, and whether   #
# vertex is a start or an end vertex.                                                      #
############################################################################################

class Vertex:
    def __init__(self,i,j):
        self.neighbors = []
        self.i = i
        self.j = j
        self.cellType = 0 # -1 if End, 1 if Start, 2 if Monster
        self.keysObtained = []
        
    # Check if otherVertex is adjacent to this vertex    
    def isAdjacent(self,otherVertex):
        return ((abs(self.i - otherVertex.i) + abs(self.j - otherVertex.j)) == 1)
        
    
#####################################
# Set up adjacency list of vertices #
#####################################

def setUpAdjList(grid,N,M):
    vertexList = []
    startVertex = None
    
    for i in range(N):
        for j in range(M):
            # Check if grid is empty and has no monster 
            if grid[i][j] != 'X':
                newVertex = Vertex(i,j)
                if grid[i][j] == 'S':
                    startVertex = newVertex
                    newVertex.cellType = 1
                elif grid[i][j] == 'E':
                    newVertex.cellType = -1
                elif grid[i][j] == 'M':
                    newVertex.cellType = 2

                vertexList.append(newVertex)
                
                for vertex in vertexList:
                    if newVertex.isAdjacent(vertex):
                        vertex.neighbors.append(newVertex)
                        newVertex.neighbors.append(vertex)

                        
    return (startVertex,vertexList)

    
################################################
# Find shortest path from vertex to end vertex #
# Uses Breadth-First Search                    #
################################################

def shortestPath(vertex,vertexList,lives):
    dist = {}
    vis = {}
    livesList = {}
    visitedQueue = []
 #   print "there are "+str(lives)

    for v in vertexList:
        dist[v] = 1000000000
        livesList[v] = lives

    dist[vertex] = 0
    visitedQueue.append(vertex)
    vis[vertex] = lives

    while len(visitedQueue) > 0:
        u = visitedQueue.pop(0)
        
        for v in u.neighbors:
            if v not in vis: 
                dist[v] = dist[u] + 1

                if v.cellType == 2:
                    vis[v] = vis[u] - 1
                else:
                    vis[v] = vis[u]

                if vis[v] > 0:
                    visitedQueue.append(v)
                    
            elif v.cellType == 2:
                if vis[u] - 1 > vis[v]:
                    vis[v] = vis[u] -1
                    dist[v] = dist[u] + 1
                    if vis[v] > 0:
                        visitedQueue.append(v)
                    
            elif vis[v] < vis[u]:
                vis[v] = vis[u]
                dist[v] = dist[u] + 1
                if vis[v] > 0:
                   visitedQueue.append(v)

            if v.cellType == -1:
                return dist[v]

                
    return -1

        
def readInput():
    N,M,T = map(int, raw_input().split())

    inputGrid = []
    
    for i in range(N):
        newRow = map(str,raw_input().split())
        inputGrid.append(newRow)

    (start,vList) = setUpAdjList(inputGrid,N,M)
   
    print shortestPath(start,vList,T)

readInput()
      
