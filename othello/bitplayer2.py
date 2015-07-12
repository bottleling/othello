import memory,constants
import bitutility as bu
DEPTH = 6
HWEIGHTS = [20,10,5,-15,-25]

class BitPlayer2:

    def __init__(self, color):
        '''
        Make sure to store the color of your player ('B' or 'W')
        You may init your data structures here, if any
        '''
        print 'BitPlayer 2 init!' #print name of class to ensure that right class is used
        self.color = color #color is 'B' or 'W'
        self.numberOfPly = 0

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

        self.numberOfPly +=1
        colorValue = 1 if color == 'W' else -1
        bitBoards = bu.convertToBitBoards(board)
        x=self.negamax(bitBoards,DEPTH,colorValue, -99999, 99999, None)[1]
        coordinates=None
        if x!=None:
            coordinates = divmod(x, constants.BRD_SIZE)
        print "Move: ", coordinates

        return coordinates

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

    def getMemoryUsedMB(self):
        '''
        You do not need to add to this code. Simply have it return 0
        '''
        return 0.0
    

    def negamax(self, bitBoards, depth, colorValue, alpha, beta, bestIndex):
        myColor = 'W' if colorValue == 1 else 'B'
        oppColor = 'B' if colorValue ==1 else 'W'
        myBoard, oppBoard = bu.whoseBoard(bitBoards, myColor)
        myMoves = bu.getIndexesOfTrue(bu.getValidMoves(bitBoards,myColor))
        # print "my color:", myColor
        # print [divmod(x,8) for x in myMoves]
        heuristic = self.heuristic2 if self.numberOfPly > 8 else self.heuristic1
        #heuristic = self.heuristic1
        if self.isBoardFull(bitBoards) or depth == 0: return (colorValue * heuristic(bitBoards,myColor,myMoves),bestIndex)
        oppMoves = bu.getIndexesOfTrue(bu.getValidMoves(bitBoards,oppColor))
        if len(myMoves) == 0 :
            if len(oppMoves)==0: return (colorValue * heuristic(bitBoards,myColor,myMoves),bestIndex)
            return (-99999, None)

        for corner in (0,7,56,63):
            if corner in myMoves:
                return (colorValue * heuristic(bitBoards,myColor,myMoves),corner)

        maxVal = -99999
        bestPosition = myMoves[0]
        alphaPosition = myMoves[0]
        for position in myMoves:
            myBoardCopy = myBoard
            myBoardCopy = bu.setBit(myBoardCopy,position,1)
            x = -1*self.negamax( (oppBoard, myBoardCopy) , depth-1, -1*colorValue, -1*beta, -1*alpha, position)[0]
            if x > alpha:
                alpha = x
                alphaPosition = position
            if alpha > beta:
                return (alpha, alphaPosition)
            if x > maxVal:
                maxVal = x
                bestPosition = position
            
        return (maxVal, bestPosition)

    
    def isBoardFull(self,bitBoards):
        if bu.numberOfTrue(bu.getSpacesBoard(bitBoards)) == 0:
            return True
        return False

    
    def heuristic1(self, bitBoards, myColor, myMoves):
        myBoard, oppBoard = bu.whoseBoard(bitBoards, myColor)
        cornerDisks = bu.getNumberOfCornerDisks(myBoard)
        edgeDisks = bu.getNumberOfEdgeDisks(myBoard) - bu.getNumberOfEdgeDisks(oppBoard)
        availableMoves = len(myMoves)
        cDisks = bu.getNumberOfCDisks(myBoard)
        xDisks = bu.getNumberOfXDisks(myBoard)

        return HWEIGHTS[0]*cornerDisks + HWEIGHTS[1]*edgeDisks + HWEIGHTS[2]*availableMoves + HWEIGHTS[3] * cDisks + HWEIGHTS[4] * xDisks

    def heuristic2(self, bitBoards, myColor, myMoves):
        weight = [[99,-8,8,6,6,8,-8,99],
        [-8,-24,-4,-3,-3,-4,-24,-8],
        [8,-4,7,4,4,7,-4,8],
        [6,-3,4,0,0,4,-3,6],
        [6,-3,4,0,0,4,-3,6],
        [8,-4,7,4,4,7,-4,8],
        [-8,-24,-4,-3,-3,-4,-24,-8],
        [99,-8,8,6,6,8,-8,99]]
        myBoard, oppBoard = bu.whoseBoard(bitBoards, myColor)
        myBoardIndexes = [divmod(x,8) for x in bu.getIndexesOfTrue(myBoard)]
        oppBoardIndexes = [divmod(x,8) for x in bu.getIndexesOfTrue(oppBoard)]
        myBoardWeight= 0
        oppBoardWeight  = 0
        for (i,j) in myBoardIndexes:
            myBoardWeight+= weight[i][j]
        for (i,j) in oppBoardIndexes:
            oppBoardWeight+= weight[i][j]
        return myBoardWeight - oppBoardWeight
