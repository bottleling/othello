'''ONLY WORKS FOR BOARD SIZE OF 8X8. NEED TO FIGURE OUT HOW TO CHANGE THE MASKS FOR DIFFERENT SIZE OF BOARDS'''
MAXBITS = 64
BRD_SIZE = 8
def prettyPrint(bitBoard):
    string = bin(bitBoard)[2:].zfill(MAXBITS)
    print string
    for i in xrange(0,BRD_SIZE):
        s = ""
        for j in xrange(0, BRD_SIZE):
            s = "%s %s" % (s, string[i*BRD_SIZE+j])
        print "%s\n"%s

def shiftDown(bitBoard):
    #print "Down: "
    bitBoard= bitBoard >> 8 & 0x00FFFFFFFFFFFFFF
    return bitBoard
def shiftUp(bitBoard):
    #print "Up: "
    bitBoard = bitBoard << 8 & 0xFFFFFFFFFFFFFF00
    return bitBoard
def shiftLeft(bitBoard):
    #print "Left: "
    bitBoard = bitBoard << 1 & 0xFEFEFEFEFEFEFEFE
    return bitBoard
def shiftRight(bitBoard):
    #print "Right: "
    bitBoard = bitBoard >> 1 & 0x7F7F7F7F7F7F7F7F
    return bitBoard
def shiftDownLeft(bitBoard):
    #print "Down, left:"
    bitBoard = bitBoard >> 7 & 0x00FEFEFEFEFEFEFE
    return bitBoard
def shiftDownRight(bitBoard):
    #print "Down, right: "
    bitBoard = bitBoard >> 9 & 0x007F7F7F7F7F7F7F
    return bitBoard
def shiftUpLeft(bitBoard):
    #print "up, left: "
    bitBoard = bitBoard << 9 & 0xFEFEFEFEFEFEFE00
    return bitBoard
def shiftUpRight(bitBoard):
    #print "up, right: "
    bitBoard = bitBoard << 7 & 0x7F7F7F7F7F7F7F00
    return bitBoard

def convertToBitBoards(board):
    '''Convert a board in 2dim array into bitboards'''
    whiteBoard = 0
    blackBoard = 0
    for row in xrange(0, len(board)):
        for col in xrange(0,len(board)):
            if board[row][col] == 'W':
                whiteBoard = setBit(whiteBoard,row*8+col,1)
            if board[row][col] == 'B':
                blackBoard = setBit(blackBoard,row*8+col,1) 
    return (whiteBoard, blackBoard)

def setBit(bitBoard, index, toset): 
    '''
    Set the bit at an index (counting from the most significant bit) to 1 or 0, of the bitBoard. 
    toset is 1 or 0, depending on whether you want to turn the bit on or off. 
    '''
    index = MAXBITS-1-index
    mask = 1 << index
    bitBoard &= ~mask
    if toset:
        bitBoard |= mask
    return bitBoard

def getSpacesBoard(bitBoards):
    whiteBoard, blackBoard = bitBoards
    return blackBoard^whiteBoard^0xFFFFFFFFFFFFFFFF

def getValidMoves(bitBoards, color):
    '''Returns a bitboard containing all valid moves for that color'''
    spacesBoard = getSpacesBoard(bitBoards)
    myBoard, oppBoard = whoseBoard(bitBoards,color)
    myMoves = []
    for x in xrange(1,9):
        if x == 1:
            alteration = shiftDown
        elif x == 2:
            alteration = shiftUp
        elif x == 3:
            alteration = shiftLeft
        elif x == 4:
            alteration = shiftRight
        elif x == 5:
            alteration = shiftDownLeft
        elif x == 6:
            alteration = shiftDownRight
        elif x == 7:
            alteration = shiftUpLeft
        elif x == 8:
            alteration = shiftUpRight
        
        myBoardAltered = alteration(myBoard)
        potentialMoves = myBoardAltered & oppBoard #Potential moves for me. this shows the positions of opponent where opponent is directly underneath my piece
        while potentialMoves != 0:
            potentialAltered = alteration(potentialMoves)
            potentialMoves = potentialAltered & oppBoard
            myMoves.append(potentialAltered & spacesBoard) #Valid moves for me in the direction specified by x

    result = myMoves[0]
    for b in xrange(1,len(myMoves)):
        result |= myMoves[b]
    return result

def whoseBoard(bitBoards, myColor):
    whiteBoard, blackBoard = bitBoards
    return (whiteBoard, blackBoard) if myColor == "W" else (blackBoard, whiteBoard)

def numberOfTrue(bitBoard):
    return bin(bitBoard).count("1")

def numberOfFalse(bitBoard):
    return bin(bitBoard).count("0")

def isBitTrue(bitBoard, index):
    return bitBoard & (1 << index)

def getIndexesOfTrue(bitBoard):
    binstring = bin(bitBoard)[2:].zfill(MAXBITS)
    indexes = []
    for index, value in enumerate(binstring):
        if int(value): indexes.append(index) 
    return indexes

def getNumberOfEdgeDisks(bitBoard):
    mask = 0b1111111110000001100000011000000110000001100000011000000111111111
    bitBoard &= mask
    return bin(bitBoard).count("1")
def getNumberOfCornerDisks(bitBoard):
    mask = 0b1000000100000000000000000000000000000000000000000000000010000001
    bitBoard &= mask
    return bin(bitBoard).count("1")
def getNumberOfCDisks(bitBoard):
    mask = 0b0100001010000001000000000000000000000000000000001000000101000010
    bitBoard &= mask
    return bin(bitBoard).count("1")
def getNumberOfXDisks(bitBoard):
    mask = 0b0000000001000010000000000000000000000000000000000100001000000000
    bitBoard &= mask
    return bin(bitBoard).count("1")

###TEST CONVERSION AND SETTING OF BITS###
# twodimarray = [['G','G','G','G','G','G','G','G'],['G','G','G','G','G','G','G','G'],['G','G','G','G','G','G','G','G'],['G','G','G','B','W','G','G','G'],
# ['G','G','G','W','B','G','G','G'],['G','G','G','G','G','G','G','G'],['G','G','G','G','G','G','G','G'],['G','G','G','G','G','G','G','G']]
# whitebb, blackbb = convertToBitBoards(twodimarray)

# print "White BB:"
# prettyPrint(whitebb)
# print "Black BB:"
# prettyPrint(blackbb)

# bitBoards = (whitebb,blackbb)
# print "Valid moves for Black:"
# result = getValidMoves(bitBoards,"B")
# indexes = getIndexesOfTrue(result)
# #prettyPrint(result)
# print indexes
# print "Valid moves for White:"
# result = findValidMoves(bitBoards,"W")
# prettyPrint(result)

###TEST BIT SHIFTS###
# bitBoard = 0b1111111110000000100000001000000010000000100000001000000010000100
# prettyPrint(bitBoard)
# prettyPrint(shiftDown(bitBoard))
# prettyPrint(shiftUp(bitBoard))
# prettyPrint(shiftLeft(bitBoard))
# prettyPrint(shiftRight(bitBoard))
# prettyPrint(shiftDownLeft(bitBoard))
# prettyPrint(shiftDownRight(bitBoard))
# prettyPrint(shiftUpLeft(bitBoard))
# prettyPrint(shiftUpRight(bitBoard))
#bitBoard = 0b1111111100000001100000000000000000000000000000000000000000000000
# print getNumberOfCornerDisks(bitBoard)
# print getNumberOfEdgeDisks(bitBoard)