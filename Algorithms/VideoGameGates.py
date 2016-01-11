############################################################################################
# Vertex Class. Contains coordinates in grid, array of neighboring vertices, and whether   #
# vertex is a start or an end vertex.                                                      #
############################################################################################

class Vertex:
    def __init__(self,i,j):
        self.neighbors = []
        self.i = i
        self.j = j
        self.cellType = 0 # -1 if End, 1 if Start, 2 if Monster, 3 if Key, 4 if Gate
        self.ind = -1 # -1 if not a key/gate, numbered otherwise
        self.keysAndLives = []
        self.visitable = True
        
        
    # Check if otherVertex is adjacent to this vertex    
    def isAdjacent(self,otherVertex):
        return ((abs(self.i - otherVertex.i) + abs(self.j - otherVertex.j)) == 1)


        
def processKey(cellStr,vertex):
    vertex.cellType = 3
    vertex.ind = cellStr[1]

def processGate(cellStr,vertex):
    vertex.cellType = 4
    vertex.ind = cellStr[1]
    
def giveKeys(vList,ind):
    for v in vList:
        v.keysFound.append(ind)

# Are there any keys in v1 that are not in v2?
def hasAllKeys(v1,v2):
    for i in v1.keysFound:
        if i not in v2.keysFound:
            return False
    return True

def stateHasNotAppeared(keysAndLives,state):
    for superState in keysAndLives:
        if state == superState[0]:
            return False

    return True


# Set gates with these keys equal to true
def setGates(vertexList,ind):
    for v in vertexList:
        if v.cellType == 4 and v.ind == ind:
            v.visitable = True

########################################
# When setting a new keysFound list,   #
# if a gate has index not in the list  #
# make sure it is not visitable        #
########################################

def updateGates(vertexList,keyList):
    for v in vertexList:
        if v.cellType == 4:
            if not v.ind in keyList:
                v.visitable = False
            else:
                v.visitable = True

def resetGates(vertexList):
    for v in vertexList:
        if v.cellType == 4:
            v.visitable = False
            
        

# Once you got key, make corresponding gates visible
def makeGateVisitable(v,vertexList):
    for w in vertexList:
        if w.ind == v.ind:
            w.visitable = True
    

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
                # If it's a monster set cellType appropriately
                elif grid[i][j] == 'M':
                    newVertex.cellType = 2
                # Cell has key
                elif 'K' in grid[i][j]:
                    processKey(grid[i][j],newVertex)

                elif 'G' in grid[i][j]:
                    processGate(grid[i][j],newVertex)

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
    vis = {}
    visitedQueue = []
    #   print "there are "+str(lives)
    
    visitedQueue.append([vertex,[[False,False,False,False,False,lives],0]])
    vis[vertex] = lives

    
    while len(visitedQueue) > 0:
        lst = visitedQueue.pop(0)
        u = lst[0]
        print u.cellType
        prevState = lst[1]
        shouldAppend = True
        
        for v in u.neighbors:
            print v.cellType
            if v not in vis:
                currState = prevState
                currState[1] = prevState[1] + 1
                
                if v.cellType == 2:
                    currState[0][4] = currState[0][4] - 1
                    vis[v] = vis[u] - 1
                elif v.cellType == 3:
                    currState[0][v.ind-1] = True
                    vis[v] = vis[u]
                elif v.cellType == 4:
                    if not currState[0][v.ind-1]:
                        shouldAppend = False
                v.keysAndLives.append(currState)
            
                if currState[0][4] > 0 and shouldAppend:
                    visitedQueue.append((v,currState))
            
            elif v.cellType == 2:
                if stateHasNotAppeared(v.keysAndLives,prevState[0]):
                    currState = prevState
                    currState[0][4] = currState[0][4] - 1                        
                    if currState[0][4] > 0 and shouldAppend:
                        visitedQueue.append((v,currState))
        
            elif stateHasNotAppeared(v.keysAndLives,prevState[0]):
                currState = prevState
                if vis[v] > 0:
                    visitedQueue.append((v,currState))
    
            if v.cellType == -1:
                 print 'here'
                 return currState[1]
    
    
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
      
