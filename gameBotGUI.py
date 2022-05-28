import pygame
from pygame.locals import *

pygame.init()

##############################################################
################.Game Logic Helper Methods.###################
##############################################################

# Game Logic Variables
position = 0
player = 'X'
bot = 'O'
gameOver = False
winner = ' '
board = {
    1:" ", 2: " " , 3: " ",
    4:" ", 5: " " , 6: " ",
    7:" ", 8: " " , 9: " "
}
winPositions = [ [1,2,3], [4,5,6], [7,8,9], [1,4,7],
    [2,5,8], [3,6,9], [1,5,9], [3,5,7] ]


def printBoard (board):
    str = ""
    for key , value in board.items():
        if key%3 == 0:
            str += f" {value} \n"
            if not key == 9:
                str += f" --------- \n"
        else:
            str += f" {value} |"
    print (str); 

def isEmptyCell(position):
    if (board[position] == " "): return True
    else: return False 

def play (symbol,position):
        board[position] = symbol
        printBoard (board)
        isGameOver()
        return

def checkWhoWin (symbol):
    for arr in winPositions:
        if (board[arr[0]] == board[arr[1]] and board[arr[0]] == board[arr[2]] and board[arr[0]] == symbol ): return True
    return False

def isDraw ():
    for key in board.keys():
        if board[key] == " ": return False
    return True

def isGameOver ():
    global gameOver
    global winner

    ##check for Win
    for arr in winPositions:
        if (board[arr[0]] == board[arr[1]] and board[arr[0]] == board[arr[2]] and board[arr[0]] == 'X' ):
            gameOver = True
            winner = 'X'
            print(" 🟢 Player wins the game 🎉🎉 \n")
        if (board[arr[0]] == board[arr[1]] and board[arr[0]] == board[arr[2]] and board[arr[0]] == 'O' ):
            gameOver = True
            winner = 'O'
            print(" 🟢 Bot wins the game 🦾🤖 \n")

	##check for Draw
    if gameOver == False and isDraw():
        gameOver = True
        winner = ' '
        print(" 🟢 Draw 🚩 \n")

def resetGame():
    #Reset All Game Logic Variables
    global gameOver , player , position , board , winner
    position = 0
    gameOver = False
    player = 'X'
    winner = ' '
    for key in board.keys():
        board[key] = " "

def playerMove (position):
    play(player,position) 
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

##############################################################
####################.GUI Helper Methods.######################
##############################################################

# GUI Variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
LINE_WIDTH = 10
CELL_WIDTH = SCREEN_WIDTH // 3
POS = []
SCREEN_BG =  (35,39,42) 
LINE_COLOR =  (88,101,242)
X_COLOR = (94,197,118)
O_COLOR = (211,47,47)
MESG_COLOR =  (243,243,243)
RECT_COLOR = (94,197,118)
FONT = pygame.font.SysFont(None, 40)
again_rect = Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe Game 🤖')


def draw_board():
	screen.fill(SCREEN_BG)
	for x in range(1,3):
		pygame.draw.line(screen, LINE_COLOR, (0, CELL_WIDTH * x), (SCREEN_WIDTH,CELL_WIDTH * x), LINE_WIDTH)
		pygame.draw.line(screen, LINE_COLOR, (CELL_WIDTH * x, 0), (CELL_WIDTH * x, SCREEN_HEIGHT), LINE_WIDTH)

def draw_symbols():
    fakeBoard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Copy all the cells from the original Board into the Fake Board
    for i in range(len(fakeBoard)):
        for j in range(len(fakeBoard[i])):
            fakeBoard[i][j] = board[i*3+j+1]

    # Loop over the fake board and draw symbols on the screen
    for row in range(len(fakeBoard)):
        for col in range(len(fakeBoard[i])):
            if fakeBoard[row][col] == "X":
                pygame.draw.line(screen, X_COLOR, (col * 200 + 30, row * 200 + 30), (col * 200 + 170, row * 200 + 170), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, (col * 200 + 170, row * 200 + 30), (col * 200 + 30, row * 200 + 170), LINE_WIDTH)
            if fakeBoard[row][col] == "O":
                pygame.draw.circle(screen, O_COLOR, (col * 200 + 100, row * 200 + 100), 70, LINE_WIDTH)

def draw_gameover(winner):
    if winner != ' ':
        if winner == 'X':
            end_text = " Player wins!"
        else:
            end_text = "    BOT wins!"
    elif winner == ' ':
        end_text = "Draw, no wins!"

    end_img = FONT.render(end_text, True, MESG_COLOR)
    pygame.draw.rect(screen, RECT_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50))
    screen.blit(end_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    again_text = 'Play Again?'
    again_img = FONT.render(again_text, True, MESG_COLOR)
    pygame.draw.rect(screen, RECT_COLOR, again_rect)
    screen.blit(again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))


##############################################################
########################.Main App.############################
##############################################################
print("----------------------------------------------")
print("🤖 Hello Let's Play Tic-Tac-Toe Game Together 🤖")
print("----------------------------------------------")
run = True
while run:

    draw_board()
    draw_symbols()

    # Add Event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        # if The Game not finihed... 
        if not gameOver:
            if event.type == pygame.MOUSEBUTTONDOWN:  
                POS = pygame.mouse.get_pos()
                x = POS[1] // CELL_WIDTH
                y = POS[0] // CELL_WIDTH
                position = x*3+y+1
                if isEmptyCell(position):
                    playerMove(position)
                    if not gameOver: botMove()
                else: 
                    print("This is not an Empty Cell ❌ \n 🟢 Please choose another Position ")

    if gameOver:
        draw_gameover(winner)
		# check if Play Again btn clicked
        if event.type == pygame.MOUSEBUTTONDOWN:  
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                # Reset All Game Logic Variables
                resetGame()
                print("----------------------------------------------")
                print(" Let's play again 🦾🤖")
                print("----------------------------------------------")

	# Update display
    pygame.display.update()

pygame.quit()
