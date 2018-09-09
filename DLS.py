import sys

'''
@author: Dac Thanh Doan
@created: 23 Aug, 2017

'''

class DLSNode:
    def __init__(self, state, cost, parent, level, path):
        self.__state = state
        self.__cost = cost
        self.__successors = []
        self.__parent = parent
        self.__level = level #level is used to check if DLS has reached bound or not
        self.__path = path
        self.__identifier = None
        self.__operator = None
    
    #####################
    #Some getters to retrieve data from the node
    def getState(self):
        return self.__state
    
    def getCost(self):
        return self.__cost
    
    def getParent(self):
        return self.__parent
    
    def getLevel(self):
        return self.__level
    
    def getPath(self):
        return self.__path
    
    def getSuccessors(self):
        return self.__successors
    
    def setIdentifier(self, iden):
        self.__identifier = iden
        
    def getIdentifier(self):
        return self.__identifier
    
    def getOperator(self):
        return self.__operator
    
    def setOperator(self, op):
        return self.__operator
    #####################
    
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
                        newState[i], newState[ePos] = newState[ePos], newState[i]#swap 'E' and the cell on position i
                        if (abs(ePos - i) == 1): #if the cell is adjacent to E then actionCost = 1
                            actionCost = 1
                        else:
                            actionCost = abs(ePos - i) - 1
                        newState = ''.join(newState)
                        if (ePos - i > 0):
                            direction = 'L'
                        else:
                            direction = 'R'
                        num = abs(ePos - i)
                        operator = str(num)+direction
                        self.setOperator(operator)
                        outputLine = operator + ' ' + newState + ' ' + str(self.__cost + actionCost) + '\n' 
                        path = self.__path + outputLine
                        generatedNode = DLSNode(newState, actionCost + self.__cost, self.__state, self.__level+1, path) #make a new node: cost = actionCost + cost(parent), level(newNode) = level(parent) + 1
                        #also save the state of parent to the newly generated node     
                        self.__successors.append(generatedNode)
                        
    def reachGoal(self):
        stateLen = len(self.__state)
        wCount = 0
        firstBlack = 0
        for i in range(0,stateLen):
            if (self.__state[i] == 'B'):
                firstBlack = i
                break
        for i in range(firstBlack, stateLen):
            if (self.__state[i] == 'W'):
                wCount+=1
        return (wCount == 0)
                        
'''
A Stack is implemented for the OPEN list of DLS graph search algorithm as Stack is FIFO (First In First Out) as DLS
'''
class Stack:
    def __init__(self):
        self.__stack = []
        
    '''
    push an element to the stack
    @param: elem is the element to be pushed in
    '''
    def push(self, elem):
        self.__stack.append(elem)
        
    '''
    pop the last element out of stack
    @return: the last element of the stack. stack size is decremented by 1
    '''
    def pop(self):
        return self.__stack.pop()
    
    '''
    get the current size of the stack
    @return: size of the stack
    '''
    def getStackSize(self):
        return len(self.__stack)
    
    '''
    check if the stack is empty
    @return: true if stack is empty, false otherwise
    '''
    def isEmpty(self):
        return (len(self.__stack) == 0)
    
    '''
    retrieve data of the element in position i of stack
    @param: i is the index of wanted element
    @return: the data of element in position i of the stack
    '''
    def getItem(self, i):
        return self.__stack[i]
        
        
class DLS:
    def __init__(self, start):
        self.__closed = []
        self.__currentNode = DLSNode(start, 0, None, 0, 'start' + ' ' + start + ' 0\n') #For start node: state = startState, g = 0, h = h, f = g+h = h, parent = None
        self.__currentNode.setIdentifier('N0')
        self.__open = Stack()
        self.__open.push(self.__currentNode)
        self.__result = None
        
    def search(self, bound, flag):
        bound = bound
        success = False
        iden = 0
        while (not self.__open.isEmpty()): #while OPEN is not empty           
            n = self.__open.pop() #Expanding
            
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
                print(n.getState(),' ',n.getCost(), ' ',n.getLevel())
            ########################################
            
            ######## DIAGNOSTIC MODE 4 (Expanding)#############
            if (flag == 4):
                for i in range(self.__open.getStackSize()):
                    print(self.__open.getItem(i).getState(), end=' ')
                for i in range(0, len(self.__closed)):
                    print(self.__closed[i].getState())
            ########################################
            
            if (n.reachGoal()): #If node n has reached goal state then return n
                return n
            if (n.getLevel() <= bound): #If node n has not reached bound then generate its successors
                n.GenerateSuccessors() #Generating
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
                    for j in range(1,self.__open.getStackSize()): #check if generated node in OPEN
                        if (generatedNodes[i].getState() == self.__open.getItem(j).getState()): #If generatedNode in open list
                            inOpen = True
                            break
                    if (inOpen):
                        continue
                    else:
                        iden+=1
                        identifier = 'N' + str(iden)
                        generatedNodes[i].setIdentifier(identifier)
                        self.__open.push(generatedNodes[i]) #If not in OPEN then push it in
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
                            print(generatedNodes[i].getCost())
                        ########################################
                        ######## DIAGNOSTIC MODE 5 (Generating)#############
                        if (flag == 5): 
                            print(0)
                        ########################################
                        ######## DIAGNOSTIC MODE 6 (Generating)#############
                        if (flag == 6): 
                            print(generatedNodes[i].getCost())
                        ########################################
            self.__closed.append(n)       
        if (not success):
            exit("Failed to find the goal state")
            