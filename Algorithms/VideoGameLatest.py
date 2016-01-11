
def findStart(grid,N,M):
    for i in range(N):
        for j in range(M):
            if grid[i][j] == 'S':
                return (i,j)

def findNeighbors(i,j,N,M):
    neighbors = []
    if i > 0:
        neighbors.append((i-1,j))
    if j > 0:
        neighbors.append((i,j-1))
    if i < N-1:
        neighbors.append((i+1,j))
    if j < M-1:
        neighbors.append((i,j+1))

    return neighbors
            
def shortestPath(start,grid,lives,N,M):
    Q = []
    visitedList = {}

    distances = {}
    startVertex = (start[0],start[1],lives,False,False,False,False,False)
    distances[startVertex] = 0
    Q.append(startVertex)
    visitedList[startVertex] = True

    while len(Q) > 0:
        u = Q.pop(0)
        neighbors = findNeighbors(u[0],u[1],N,M)

        for coord in neighbors:
            i = coord[0]
            j = coord[1]
            newLives = u[2]
            key1 = u[3]
            key2 = u[4]
            key3 = u[5]
            key4 = u[6]
            key5 = u[7]
            newDist = distances[u]

            if 'G' in grid[i][j]:
                gateNum = int(grid[i][j][1])
                v = (i,j,u[2],u[3],u[4],u[5],u[6],u[7])
                if v not in visitedList:
                    if v[gateNum+2]:
                        distances[v] = distances[u]+1
                        visitedList[v] = True
                        Q.append(v)
            elif grid[i][j] == 'E':
                newDist = newDist+1
                v = (i,j,u[2],u[3],u[4],u[5],u[6],u[7])
                distances[v] = newDist
                visitedList[v] = True
                Q.append(v)
                return distances[v]
            elif grid[i][j] != 'X':
                if grid[i][j] == 'O' or grid[i][j] == 'S':
                    newDist = newDist + 1
                elif grid[i][j] == 'M':
                    newLives = newLives - 1
                    newDist = newDist + 1
                elif 'K' in grid[i][j]:
                    keyNum = int(grid[i][j][1])
                    newDist = newDist + 1
                    if keyNum == 1:
                        key1 = True
                    elif keyNum == 2:
                        key2 = True
                    elif keyNum == 3:
                        key3 = True
                    elif key4 == 4:
                        key4 = True
                    elif key5 == 5:
                        key5 = True

                v = (i,j,newLives,key1,key2,key3,key4,key5)
                distances[v] = newDist

                if v not in visitedList and newLives > 0:
                    visitedList[v] = True
                    Q.append(v)

    return -1
                
            
                


def readInput():
    N,M,T = map(int, raw_input().split())

    inputGrid = []
    
    for i in range(N):
        newRow = map(str,raw_input().split())
        inputGrid.append(newRow)

    start = findStart(inputGrid,N,M)
        
    print shortestPath(start,inputGrid,T,N,M)
   
readInput()
      
