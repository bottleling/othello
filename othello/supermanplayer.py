import memory,constants,random,copy

DEPTH = 5
HWEIGHTS = (1,1,1)
class SupermanPlayer:

    def __init__(self, color):
        '''
        Make sure to store the color of your player ('B' or 'W')
        You may init your data structures here, if any
        '''
        print 'SupermanPlayer init!' #print name of class to ensure that right class is used
        self.validMoves = []
        self.opponentValidMoves = []
        self.color = color #color is 'B' or 'W'
        

    def chooseMove(self, board, prevMove): #REMEMBER TO CHECK IF FINDVALIDMOVES HAS BEEN CALLED BEFORE GETTING
        '''
        board is a two-dimensional list representing the current board configuration.
        board is a copy of the original game board, so you can do to it as you wish.
        board[i][j] is 'W', 'B', 'G' when row i and column j contains a
        white piece, black piece, or no piece respectively.
        As usual i, j starts from 0, and board[0][0] is the top-left corner.
        prevMove gives the i, j coordinates of the last move made by your opponent.
        prevMove[0] and prevMove[1] are the i and j-coordinates respectively.
        prevMove may be None if your opponent has no move to make during his last turn.
        '''       
        memUsedMB = memory.getMemoryUsedMB()
        if memUsedMB > constants.MEMORY_LIMIT_MB - 100: #If I am close to memory limit
            #don't allocate memory, limit search depth, etc.
            #RandomPlayer uses very memory so it does nothing
            pass

        dirs = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        color = self.color
       
        if   color == 'W': oppColor = 'B'
        elif color == 'B': oppColor = 'W'
        else: assert False, 'ERROR: Current player is not W or B!'
        colorValue = 1 if color == 'W' else -1
        v = self.negamax(board,DEPTH,colorValue)
        print "Move: ", v
        return v

    def negamax(self,board, depth, colorValue):
        if self.isGameOver(board) or depth == 0:
            return colorValue * self.heuristic(board,colorValue)
        maxVal = -9999999
        bestPosition = None
        opponentColor = 'B' if self.color == 'W' else 'W'
        self.findValidMoves(board,self.color,self.validMoves)
        self.findValidMoves(board, opponentColor, self.opponentValidMoves)
        for position in self.validMoves:
            boardCopy = copy.deepcopy(board)
            x = -1*self.negamax(boardCopy, depth-1, -1*colorValue)
            if x >= maxVal:
                maxVal = x
                bestPosition = position
        return bestPosition

    def gameEnd(self, board):
        '''
        This is called when the game has ended.
        Add clean-up code here, if necessary.
        board is a copy of the end-game board configuration.
        '''
        # no clean up necessary for random player
        pass

    def getColor(self):
        '''
        Returns the color of the player
        '''
        return self.color
    
    def getValidMoves(self,board):
        '''
        Returns the valid moves of the player
        '''
        return self.validMoves
    
    def getOpponentValidMoves(self,board):
        return self.opponentValidMoves
    
    def getMemoryUsedMB(self):
        '''
        You do not need to add to this code. Simply have it return 0
        '''
        return 0.0
    
    def findValidMoves(self, board, playerColor, moves):
        del moves[:]
        for row in xrange(0, len(board)):
            for col in xrange(0,len(board)):
                if board[row][col] == 'G':
                    opponentColor = 'B' if playerColor == 'W' else 'W'
                    for rowPosition in xrange(-1,2): #When rowPosition = 1, we will move down a row
                        for colPosition in xrange(-1,2):
                            if self.withinBoard(rowPosition+row, colPosition+col, len(board)) and not (rowPosition == 0 and colPosition == 0) :
                                #print "Blank at:",row, ", ", col, " Checking: ",rowPosition+row, ",", colPosition+col
                                if (board[rowPosition + row][colPosition + col] == opponentColor):
                                    #print "Found Opponent at:", rowPosition+row , " , ", colPosition + col
                                    r = row + rowPosition
                                    c = col + colPosition
                                    while True:
                                        r += rowPosition
                                        c += colPosition
                                        if self.withinBoard(r,c,len(board)):
                                            #print "Now Checking: ",  r , " , ", c, "color: ", board[r][c]
                                            if board[r][c] == playerColor:
                                                moves.append((row,col))
                                                break
                                            elif board[r][c] == 'G':
                                                break
                                        else:
                                            break
                else:
                    pass

    def withinBoard(self, r, c, b):
        if r >= b or r < 0 or c >= b or c < 0:
            return False
        return True

    def isGameOver(self,board): #has reached terminal node
        for row in xrange(0, len(board)):
            for col in xrange(0,len(board)):
                if board[row][col] == 'G':
                    return False
        # opponentColor = 'B' if self.Color == 'W' else 'W' 
        # self.findValidMoves(board, opponentColor, self.opponentValidMoves)
        if len(self.getValidMoves(board)) != 0 or len(self.getOpponentValidMoves(board)) != 0 :
            return False
        return True

    def heuristic(self,board,colorValue):
        cornerDisks = 0
        edgeDisks = 0
        availableMoves = 0
        #find number of disks in corners
        for i,j in ((0,0),(0,len(board)-1),(len(board)-1,0),(len(board)-1,len(board)-1)):
            if board[i][j] == self.color:
                cornerDisks+=1
        #find number of disks along edge, and subtract the opponent disk along the edge from this.
        opponentColor = 'B' if colorValue == 1 else 'W'
        for row in (0, len(board)-1):
            for col in xrange(0,len(board)):
                if board[row][col] == self.color:
                    edgeDisks+=1
                elif board[row][col] == opponentColor:
                    edgeDisks-=1
        for col in (0, len(board)-1):
            for row in xrange(0,len(board)):
                if board[row][col] == self.color:
                    edgeDisks+=1
                elif board[row][col] == opponentColor:
                    edgeDisks-=1        
        #find number of available moves
        availableMoves = len(self.getValidMoves(board))
        #find potential mobility (?)
        return HWEIGHTS[0]*cornerDisks + HWEIGHTS[1]*edgeDisks + HWEIGHTS[2]*availableMoves


    def validMove(self, board, pos, ddir, color, oppColor):
        newPos = (pos[0]+ddir[0], pos[1]+ddir[1])
        validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
        if not validPos: return False
        if board[newPos[0]][newPos[1]] != oppColor: return False

        while board[newPos[0]][newPos[1]] == oppColor:
            newPos = (newPos[0]+ddir[0], newPos[1]+ddir[1])
            validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
            if not validPos: break

        validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
        if validPos and board[newPos[0]][newPos[1]] == color:
            return True
        return False