###############################################
# Find the Nth term of a recurrence relations #
###############################################

import math

####################################
# Multiplies two matrices          #
# As found on Stack Overflow       #
####################################

def multMatrices(A,B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        print "Cannot multiply the two matrices. Incorrect dimensions."
        return

    # Create the result matrix
    # Dimensions would be rows_A x cols_B
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += ((A[i][k] % 1000)*(B[k][j] % 1000) % 1000)
    return C



###############################################
# Multiplies two matrices with same dimension #
###############################################

def multIdenticalMatrices(A,B,K):
    C = [[0 for row in range(K)] for col in range(K)]

    for i in range(K):
        for j in range(K):
            for k in range(K):
                C[i][j] += ((A[i][k] % 1000)*(B[k][j] % 1000) % 1000)

    return C
    


################################################
# Returns an identity matrix with dimensions k #
################################################

def identityMatrix(k):

    idMatrix = []

    for i in range (0,k):
        newRow = []
        
        for j in range (0,k):
            if i == j:
                newRow.append(1)
            else:
                newRow.append(0)
        idMatrix.append(newRow)

    return idMatrix


###########################
# Exponentiate matrix     #
###########################

def expoMatrix(A,k,size,expArray={}):
    
    if k == 0:
        return identityMatrix(size)

    elif k == 1:
        return A
   
    else:
        lesser = math.floor(float(k)/2)
        greater = math.ceil(float(k)/2)

        if lesser in expArray:
            firstHalf = expArray[lesser]
        else:
            firstHalf = expoMatrix(A,lesser,size)
            expArray[lesser] = firstHalf

        if greater in expArray:
            secondHalf = expArray[greater]
        else:
            secondHalf = expoMatrix(A,greater,size)
            expArray[greater] = secondHalf
            
        return multIdenticalMatrices(firstHalf,secondHalf,size)


#########################################
# Set up matrix used for initial values #
#########################################

def setUpInitialValuesMatrix(initValues,K):
    initVals = []

    for i in range(0,K):
        newVal = []
        newVal.append(initValues[K-i-1])
        initVals.append(newVal)

    return initVals
    



#########################################
# Set up matrix used for the recursion  #
#########################################

def setUpCoefficientMatrix(coeffs,K):

    coeffMatrix = []
    firstRow = []
    
    for i in range(0,K):
        firstRow.append(coeffs[i])

    coeffMatrix.append(firstRow)

    for j in range(0,K-1):
        newRow = []
        for k in range(0,K):
            if j == k:
                newRow.append(1)
            else:
                newRow.append(0)
            
        coeffMatrix.append(newRow)


    return coeffMatrix


def readInput():

    # Read input from user
    K,N = map(int, raw_input().split())
    
    initialValues = map(int, raw_input().split())
    initValueMatrix = setUpInitialValuesMatrix(initialValues,K)
    
    coeffs = map(int,raw_input().split())
    coeffMatrix = setUpCoefficientMatrix(coeffs,K)
    
    exponentiatedMatrix = expoMatrix(coeffMatrix,N,K)
    
    finalMatrix = multMatrices(exponentiatedMatrix,initValueMatrix)

    print finalMatrix[K-1][0] % 1000   
        

readInput()

    

        
        
