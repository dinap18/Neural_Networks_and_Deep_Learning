#Dina Pinchuck 


import copy
import random

VICTORY = 10 ** 20  # The value of a winning board (for max)
LOSS = -VICTORY  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # the length of winning seq.
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board
random.seed()

rows = 6
columns = 7


class game:
    board = []
    size = rows * columns
    playTurn = HUMAN

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''


def create(s):
    # Returns an empty board. The human plays first.
    # create the board
    s.board = []
    for i in range(rows):
        s.board = s.board + [columns * [0]]

    s.playTurn = HUMAN
    s.size = rows * columns
    s.val = 0.00001


def cpy(s1):
    # construct a parent DataFrame instance
    s2 = game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    # print("board ", s2.board)
    return s2


def value(s):
    # Returns the heuristic value of s
    dr = [-SIZE + 1, -SIZE + 1, 0, SIZE - 1]  # the next lines compute the heuristic val.
    dc = [0, SIZE - 1, SIZE - 1, SIZE - 1]
    val = 0.00001
    for row in range(rows):
        for col in range(columns):
            for i in range(len(dr)):
                t = checkSeq(s, row, col, row + dr[i], col + dc[i])
                if t in [LOSS, VICTORY]:
                    val = t
                    break
                else:
                    val += t
    if s.size == 0 and val not in [LOSS, VICTORY]:
        val = TIE
    return val


def checkSeq(s, r1, c1, r2, c2):
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VICTORY. If all O returns LOSS.
    # If empty returns 0.00001. If no Os returns 1. If no Xs returns -1.
    if r2 < 0 or c2 < 0 or r2 >= rows or c2 >= columns:
        return 0  # r2, c2 are illegal

    dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell
    dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell

    sum = 0

    for i in range(SIZE):  # summing the values in the seq.
        sum += s.board[r1 + i * dr][c1 + i * dc]

    if sum == COMPUTER * SIZE:
        return VICTORY

    elif sum == HUMAN * SIZE:
        return LOSS
    elif sum > 0 and sum < COMPUTER:
        return -1

    elif sum > 0 and sum % COMPUTER == 0:
        return 1
    return 0.00001  # not 0 because TIE is 0


def printState(s):
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows):
        print("\n|", end="")
        for c in range(columns):
            if s.board[r][c] == COMPUTER:
                print("X|", end="")
            elif s.board[r][c] == HUMAN:
                print("O|", end="")
            else:
                print(" |", end="")
    print()

    for i in range(columns):  # For numbers on the bottom
        print(" ", i, sep="", end="")

    print()

    val = value(s)

    if val == VICTORY:
        print("I won!")
    elif val == LOSS:
        print("You beat me!")
    elif val == TIE:
        print("It's a TIE")


def isFinished(s):
    # Seturns True iff the game ended
    return value(s) in [LOSS, VICTORY, TIE] or s.size == 0


def isHumTurn(s):
    # Returns True iff it is the human's turn to play
    return s.playTurn == HUMAN


def decideWhoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-MC / anything else-you : ")) == 1:
        s.playTurn = COMPUTER
    else:
        s.playTurn = HUMAN
    return s.playTurn


def makeMove(s, c):
    # Puts mark (for humaמ or computer) in col. c
    # and switches turns.
    # Assumes the move is legal.
    r = 0
    while r < rows and s.board[r][c] == 0:
        r += 1

    s.board[r - 1][c] = s.playTurn  # marks the board
    s.size -= 1  # one less empty cell
    if (s.playTurn == COMPUTER):
        s.playTurn = HUMAN
    else:
        s.playTurn = COMPUTER


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    flag = True
    while flag:
        c = int(input("Enter your next move: "))
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
        else:
            flag = False
            makeMove(s, c)


def inputRandom(s):
    # See if the agent can win block one move ahead
    for i in range(0, columns):  # this simple agent always plays min
        tmp = cpy(s)
        makeMove(tmp, i)
        if (value(tmp) == LOSS and s.board[0][i] == 0):  # if the agent should win
            makeMove(s, i)
            return
    # If no obvious move, then move random
    flag = True
    while flag:
        c = random.randrange(0, columns)
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
            printState(s)
        else:
            flag = False
            makeMove(s, c)


def inputHeuristic(s):
    # See if the agent can win or get more than one in a row
    temp = 1000
    tmp_col = 0
    for i in range(0, columns):  # this simple agent always plays min
        tmp = cpy(s)
        makeMove(tmp, i)
        if (value(tmp) < temp and s.board[0][i] == 0):  # so a "loss" is a win for this side
            tmp_col = i
            temp = value(tmp)
    makeMove(s, tmp_col)

#random agent adapted for mc agent - victory instead of loss
def inputRandomMC(s):
    # See if the agent can win block one move ahead
    for i in range(0, columns):  # this simple agent always plays min
        tmp = cpy(s)
        makeMove(tmp, i)
        if (value(tmp) == VICTORY and s.board[0][i] == 0):  # if the  mc agent should win
            makeMove(s, i)
            return
    # If no obvious move, then move random
    flag = True
    while flag:
        c = random.randrange(0, columns)
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
            #printState(s)
        else:
            flag = False
            makeMove(s, c)

#function for the mc agent to continue the game randomly until someone wins or a tie is reached
def random_mc(s):
    while not isFinished(s):#until a winner/ tie is found
        if s.playTurn==COMPUTER:
            inputRandomMC(s)# call the random agent for mc
        else: # the regular random agent
            inputRandom(s)
    if value(s)==VICTORY: # if the computer (mc-agent) won the game
        return COMPUTER
    if value(s)==LOSS:#if the other player won the game
        return HUMAN
    return 0 #we are only counting wins and losses and a tie / any other way the game ends doesnt matter



#function for mc agent
def inputMC(s):
    best = -1 #best column, starts at -1 because we don't have a -1 column
    best_ratio = 0 # the best win/loss ratio, so we know what move to make
    games_per_move = 100 #number of iterations / games to played (if possible) per column
    for c in range(7):
        if s.board[0][c]!=0: # if the column is full we can't continue there
            continue
        won = 0 #number of wins per column
        lost = 0 # number of losses per column
        for j in range(games_per_move):
            brd = cpy(s)# we need to copy the board so we dont mess it up when looking for the best move
            if brd.board[0][c]!=0:#illegal move -column is already full
                continue
            makeMove(brd, c)#making a move into the column on the copied board
            if (value(brd) == VICTORY and s.board[0][c] == 0):# if that move results in us winning then we can make the move on the original board and return from the function
                makeMove(s,c)
                return
            else:# else we will continue the game randomly is order to calculate the win/loss ratio to decide which move is the best
                winner=random_mc(brd)
                if winner==COMPUTER:#if the mc agent won
                    won+=1
                elif winner==HUMAN:#if the other agent won
                    lost+=1


        ratio = won / (lost + 1) #the ratio - lost + 1 so we don't end up dividing by zero
        if ratio > best_ratio or best == -1: #if we find a better ratio or we havent picked a column yet
            best = c
            best_ratio = ratio
    makeMove(s, best)#making the best move that we found
