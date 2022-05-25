import imp


import random
# Global Variables
board = {
    1:" ", 2: " " , 3: " ",
    4:" ", 5: " " , 6: " ",
    7:" ", 8: " " , 9: " "
}

winPositions = [ [1,2,3], [4,5,6], [7,8,9], [1,4,7],
    [2,5,8], [3,6,9], [1,5,9], [3,5,7] ]

player = 'O'
bot = 'X'

# Helpful Methods
def printBoard (board , start):
    str = ""
    for key , value in board.items():
        if (start): x = key
        else: x = value 

        if key%3 == 0:
            str += f" {x} \n"
            if not key == 9:
                str += f" --------- \n"
        else:
            str += f" {x} |"
    print (str);        

def isEmptyCell(position):
    if (board[position] == " "): return True
    else: return False 

def isDraw ():
    for key in board.keys():
        if board[key] == " ": return False
    return True

def isWin ():
    for arr in winPositions:
        if (board[arr[0]] == board[arr[1]] and board[arr[0]] == board[arr[2]] and not board[arr[0]] == " " ): return True
    return False

def checkWhoWin (symbol):
    for arr in winPositions:
        if (board[arr[0]] == board[arr[1]] and board[arr[0]] == board[arr[2]] and board[arr[0]] == symbol ): return True
    return False

def getValidPosition ():
    try:
        position = int(input())
    except:
        print("🟢 Only Integers are Allowed")
        position = getValidPosition()
    
    if (position > 9 or position < 1):
        print("🟢 Enter a Valid Number from 1 to 9") 
        position = getValidPosition()

    return position

def play (symbol,position):
    if (not isEmptyCell(position)): 
        print("This is not an Empty Cell ❌")
        print("Please choose another Position ")
        position = getValidPosition()
        print(" ")
        play(symbol,position) 
        return
    else:
        board[position] = symbol
        printBoard (board , False)
        if isDraw(): 
            print("Draw 🚩 \n")
            exit()
        if isWin():
            if(symbol == bot): 
                print("🤖 BOT wins the game 🎉🎉 \n")
            else:
                print("🧑 Player wins the game 🎉🎉 \n")
            exit()
        return

def playerMove ():
    print(f"Enter Cell Number - {player} - Turn")
    position = getValidPosition()
    print(" ")
    play(player,position) 
    return

# Second Player
def secondPlayerMove ():
    print(f"Enter Cell Number - {bot} - Turn")
    position = getValidPosition()
    print(" ")
    play(bot,position) 
    return

# DUMMY Bot
def botMoveDummy ():
    n = random.randint(1,9)
    if(board[n] == " "):
        play(bot , n)
    else:
        botMoveDummy()
    return

# Intelligent Bot
def botMove ():
    bestScore = -1000000
    bestMove = 0

    for key in board.keys():
        if(board[key] == " "):
            board[key] = bot
            score = minimax(board , 0 ,False)
            board[key] = " "
            if(score > bestScore):
                bestScore = score
                bestMove = key
    play(bot , bestMove)
    return

# Minmax Algorithm Implementation
def minimax(board , depth , isMaximizing):
    if checkWhoWin(bot):
        return 1
    if checkWhoWin(player):
        return -1
    if isDraw():
        return 0
    
    if isMaximizing:
        bestScore = -1000000
        for key in board.keys():
            if(board[key] == " "):
                board[key] = bot
                score = minimax(board , 0 ,False)
                board[key] = " "
                if(score > bestScore):
                    bestScore = score
        return bestScore

    else:
        minScore = 1000000
        for key in board.keys():
            if(board[key] == " "):
                board[key] = player
                score = minimax(board , 0 ,True)
                board[key] = " "
                if(score < minScore):
                    minScore = score
        return minScore


# Main APP 
print("----------------------------------------------")
print("🤖 Hello Let's Play Tic-Tac-Toe Game Together 🤖")
print("----------------------------------------------")
print("1. Play with a Dummy Bot 💩 \n2. Play with an Intelligent Bot 🦾🤖 \n3. Two Players 🤝")
choice = int(input())
print("----------------------------------------------")

if(choice):
    print ("🟢 Choose Number of any Cell to Play\n")
    printBoard (board , True)
    print("----------------------------------------------")

    while not isWin():
        if choice == 1: botMoveDummy()
        elif choice == 2: botMove()
        else: secondPlayerMove()
        playerMove()

