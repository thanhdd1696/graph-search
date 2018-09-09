import sys

'''
@author: Dac Thanh Doan
@created: 23 Aug, 2017

'''

'''
Heuristic function: to calculate F scores in A* algorithm.
H = number of white cells on the right side of the first black cell in puzzle
@param: targetState is the puzzle state whose H we want to find
@return: H the heuristic of the puzzle state
'''
def HeuristicFunction(targetState):
        stateLen = len(targetState)
        wCount = 0
        firstBlack = 0
        for i in range(0,stateLen):
            if (targetState[i] == 'B'):
                firstBlack = i
                break
        for i in range(firstBlack, stateLen):
            if (targetState[i] == 'W'):
                wCount+=1
        return wCount

class astarNode:
    def __init__(self, state, gScores, hScores, fScores, parent, tracingPath):
        self.__state = state
        self.__gScores = gScores
        self.__hScores = hScores
        self.__fScores = fScores
        self.__successors = []
        self.__parent = parent
        self.__path = tracingPath
        self.__identifier = None
        self.__operator = None
    
    ########################
    #Some getters and setters to retrieve or update data information
    
    def getState(self):
        return self.__state
    
    def getFScores(self):
        return self.__fScores
    
    def setGScores(self, g):
        self.__gScores = g
        
    def setFScores(self, f):
        self.__fScores = f
        
    def updateFScores(self):
        self.__fScores = self.__gScores + self.__hScores
    
    def getGScores(self):
        return self.__gScores
    
    def getParent(self):
        return self.__parent
    
    def getHScores(self):
        return self.__hScores
    
    def getSuccessors(self):
        return self.__successors
    
    def getPath(self):
        return self.__path
    
    def setPath(self, path):
        self.__path = path
        
    def setIdentifier(self, iden):
        self.__identifier = iden
        
    def getIdentifier(self):
        return self.__identifier
    
    def setOperator(self, op):
        self.__operator = op
        
    def getOperator(self):
        return self.__operator
    #########################
    
    '''
    Method GenerateSuccessors(): generates the possible next states of current puzzle
    Each new state represents a new node in the graph search algorithm
    '''
    def GenerateSuccessors(self):
        if (len(self.__successors) == 0):
            ePos = 0 #ePos stores the position of E (empty cell) 
            for i in range(0, len(self.__state)):
                if (self.__state[i] == 'E'):
                    ePos = i
                    break
            for i in range(ePos - 3, ePos + 4): #Consider 3 cells on the right and 3 cells on the left:
                if ((i >= 0) and (i < len(self.__state))):
                    if (i != ePos):
                        newState = list(self.__state) 
                        newState[i], newState[ePos] = newState[ePos], newState[i] #swap 'E' and the cell on position i
                        if (abs(ePos - i) == 1): #if the cell is adjacent to E then actionCost = 1
                            actionCost = 1 
                        else:
                            actionCost = abs(ePos - i) - 1 #else actionCost is equal to the number of cells that 'E' hopped over
                        newState = ''.join(newState)
                        
                        if (ePos - i > 0):
                            direction = 'L'
                        else:
                            direction = 'R'
                        num = abs(ePos - i)
                        operator = str(num)+direction #the operator applied to generate the node
                        self.setOperator(operator)
                        estimatedH = HeuristicFunction(newState) #calculate heuristic
                        outputLine = operator + ' ' + newState + ' ' + str(self.__gScores + actionCost) + '\n' 
                        path = self.__path + outputLine
                        generatedNode = astarNode(newState, actionCost + self.__gScores, estimatedH, actionCost + self.__gScores + estimatedH, self.__state, path) #make a new node: G = actionCost + G(parent), H = HeuristicFunction(state), F = G + H
                        #also save the state of parent to the newly generated node        
                        self.__successors.append(generatedNode)
                        
    def reachGoal(self):
        return (self.__hScores == 0)
            
'''
This class implements the OPEN in A*. Using heap will reduce the time complexity of insertion/deletion to O(logN)
'''
class Heap:
    def __init__(self):
        self.__heapList = ["root"]
        
    '''
    Method isEmpty(): checks if the heap is empty
    @return true if heap is empty, false otherwise
    '''
    def isEmpty(self):
        return (len(self.__heapList) <= 1)
    
    '''
    Method getHeapSize():
    @return: size of the heap
    '''
    def getHeapSize(self):
        return len(self.__heapList)
    
    '''
    Method getItem():
    @param: i is index of the wanted element
    @return: node at index i in heap
    '''
    def getItem(self, i):
        if(not self.isEmpty()):
            return self.__heapList[i]
        
    '''
    Method UpHeap(): brings the newly updated item to the correct position in the heap
    @return: void    
    '''
    def UpHeap(self,i):
        while ((i>1) and (self.__heapList[i].getFScores() < self.__heapList[i//2].getFScores())):
            self.__heapList[i], self.__heapList[i//2] = self.__heapList[i//2], self.__heapList[i]
            i = i//2
    
    '''
    Method: insertNode():
    @param: newNode: the node to be inserted into heap
    @return: void
    '''
    def insertNode(self, newNode):
        self.__heapList.append(newNode)
        i = len(self.__heapList) - 1
        while ((i > 1) and (self.__heapList[i].getFScores() < self.__heapList[i//2].getFScores())):
            self.__heapList[i], self.__heapList[i//2] = self.__heapList[i//2], self.__heapList[i]
            i = i//2
            
    '''
    Method retrieveNode(): this method retrieves the node on top of the heap
    @return: returnedNode is the node on the top of the heap
    '''
    def retrieveNode(self):
        if (not self.isEmpty()):
            last = len(self.__heapList) - 1
            self.__heapList[1], self.__heapList[last] = self.__heapList[last], self.__heapList[1]
            returnedNode = self.__heapList.pop()
            i = 1
            while ((i < (len(self.__heapList)//2)) and ((self.__heapList[i].getFScores() > self.__heapList[i*2].getFScores())  or (self.__heapList[i].getFScores() > self.__heapList[i*2 + 1].getFScores()))):
                if (self.__heapList[i*2 + 1].getFScores() < (self.__heapList[i*2].getFScores())):
                    self.__heapList[i*2 + 1], self.__heapList[i] = self.__heapList[i], self.__heapList[i*2 + 1]
                    i = i*2 + 1
                else:
                    self.__heapList[i*2], self.__heapList[i] = self.__heapList[i], self.__heapList[i*2]
                    i = i*2
        return returnedNode
    
    #checkHeap() is for testing purpose
    def checkHeap(self):
        check = True
        for i in range(2,len(self.__heapList)):
            if (self.__heapList[i].getFScores() < self.__heapList[i//2].getFScores()):
                check = False
        return check
        
class Astar:
    
    def __init__(self, start):
        self.__closed = []
        h = HeuristicFunction(start)
        self.__currentNode = astarNode(start, 0, h, h, None, 'start' + ' ' + start + ' 0\n') #For start node: state = startState, g = 0, h = h, f = g+h = h, parent = none, operator = none
        self.__currentNode.setIdentifier("N0")
        self.__open = Heap()
        self.__open.insertNode(self.__currentNode)
        self.__result = None
        
    def search(self, flag):
        solution = ''
        success = False
        expansionOrder = 0
        iden = 0
        while (not self.__open.isEmpty()): #while OPEN is not empty 
            n = self.__open.retrieveNode() #Expanding
            ######## DIAGNOSTIC MODE 1 (Expanding)#############
            if (flag == 1): 
                print(n.getIdentifier())
            ########################################
            
            ######## DIAGNOSTIC MODE 2 (Expanding)#############
            if (flag == 2): 
                print(expansionOrder)
                expansionOrder+=1
            ########################################
            
            ######## DIAGNOSTIC MODE 3 (Expanding)#############
            if (flag == 3): 
                print(n.getState(),' ',n.getGScores(), ' ', n.getHScores(), ' ', n.getFScores())
            ########################################
            
            ######## DIAGNOSTIC MODE 4 (Expanding)#############
            if (flag == 4):
                
                for i in range(1,self.__open.getHeapSize()):
                    print(self.__open.getItem(i).getState(), end=' ')
                
                for i in range(0, len(self.__closed)):
                    print(self.__closed[i].getState())
                
            ########################################
            
            if (n.reachGoal()): #goal state: hScores = 0 when all white cells are on the left of all black cells
                success = True
                return n
            n.GenerateSuccessors() 
            generatedNodes = n.getSuccessors()
            for i in range(0, len(generatedNodes)): 
                inClosed = False
                inOpen = False
                for j in range(0, len(self.__closed)): #check if generated node in CLOSED 
                    if (generatedNodes[i].getState() == self.__closed[j].getState()):
                        inClosed = True
                        break
                if (inClosed): #If generated node is already in CLOSED, discard it and continue
                    continue
                    
                for j in range(1,self.__open.getHeapSize()): #check if generated node in OPEN
                    if (generatedNodes[i].getState() == self.__open.getItem(j).getState()): #If generatedNode in open list
                        inOpen = True
                        if (generatedNodes[i].getGScores() < self.__open.getItem(j).getGScores()): #If f(generatedNode) < f(openNode)
                            #then update the F and G of the node 
                            self.__open.getItem(j).setGScores(generatedNodes[i].getGScores())
                            self.__open.getItem(j).updateFScores()
                            self.__open.getItem(j).setPath(generatedNodes[i].getPath()) #Update the path of that node
                            self.__open.UpHeap(j)
                            break
                if (not inOpen): #Generating new nodes
                    iden+=1
                    identifier = 'N' + str(iden)
                    generatedNodes[i].setIdentifier(identifier)
                    self.__open.insertNode(generatedNodes[i]) #If not in OPEN then push it in
                    ######## DIAGNOSTIC MODE 1 (Generating)#############
                    if (flag == 1): 
                        print(generatedNodes[i].getOperator())
                    ########################################
                    ######## DIAGNOSTIC MODE 2 (Generating)#############
                    if (flag == 2): 
                        print(generatedNodes[i].getIdentifier())
                    ########################################
                    ######## DIAGNOSTIC MODE 3 (Generating)#############
                    if (flag == 3): 
                        print(generatedNodes[i].getParent())
                    ########################################
                    ######## DIAGNOSTIC MODE 4 (Generating)#############
                    if (flag == 4): 
                        print(generatedNodes[i].getGScores())
                    ########################################
                    ######## DIAGNOSTIC MODE 4 (Generating)#############
                    if (flag == 5): 
                        print(generatedNodes[i].getHScores())
                    ########################################
                    ######## DIAGNOSTIC MODE 4 (Generating)#############
                    if (flag == 4): 
                        print(generatedNodes[i].getFScores())
                    ########################################
            self.__closed.append(n)
        if (not success):
            exit("Failed to find the goal state")
            