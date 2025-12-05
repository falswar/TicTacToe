import pygame
import sys


# constant 
# game boared measurments and configrations 
width = 800
height = 900
rows = 3
cols = 3

BoardColor = (255, 192, 203)  
LineColor= (255, 105, 180)  
SympolColor= (255, 105, 180)  
TextColor = (255, 255, 255) 


#starting the game 
pygame.init()
screen = pygame.display.set_mode((width, height)) 

#game display 
pygame.display.set_caption("Tic Tac Toe - MiniMax AI")
font1 = pygame.font.SysFont("helvetica", 40)
font2 = pygame.font.SysFont("helvetica", 60) 
# other fonts to try are :
#consolas , georgia , garamond , impact , segoe ui , verdana 
screen.fill(BoardColor)  


#setting the boared to start 
Board = [0] * 9  # 0 is empty and 1 means its the human while 2 means its the computer (AI) 
# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8 

GameOver = False 
Winner = ""
WinningLine= None  #check and store a winning line that consist of 3 cells either horizantal vertical or diagonal 

square= 600 // 3 
lineW = 15
# make grid 
def DrawLines():
    for i in range(1, 3): 
        pygame.draw.line(screen, LineColor, (100, i*square), (700, i*square), lineW)
        pygame.draw.line(screen, LineColor, (100 + i*square, 0), (100 + i*square, 600), lineW)

WinColor= (255, 20, 147)   
#winning grid 
def draw_win_line(combo):
    a, b, c = combo
    row1 = a//3
    row2 = c//3
    col1 = a%3
    col2 = c%3

    x1 = 100 + col1*square + square // 2
    x2 = 100 + col2*square + square // 2
    y1 = row1*square + square // 2
    y2 = row2*square + square // 2

    pygame.draw.line(screen, WinColor, (x1, y1), (x2, y2), lineW) 

#boared constatnts
Radius= 80
Circulewidth= 15
CrossWidth= 25
space = 55 


# printing X/O sypmols on Board 
def XO():
    #for each spot on the tic tac toe Board (3*3 Board means 9 spots)
    #set up the cordinates of the rows and cols to start
    for i in range(9): 
        row = i // 3 
        col = i % 3
        #if this position in the Board have a value of 1 then its taken by player X
        if Board[i] == 1:  # X
            pygame.draw.line(screen, SympolColor,
                                (100+col*square+space, row*square+space),
                                (100+col*square+square-space, row*square+square-space),
                                CrossWidth)
            pygame.draw.line(screen, SympolColor,
                                (100+col*square+space, row*square+square-space),
                                (100+col*square+square-space, row*square+space),
                                CrossWidth)
        #if this position is not taken by Player X check if its taken by player O, if the position have the value 2 then it i staken by plater O
        elif Board[i] == 2:  # O
            pygame.draw.circle(screen, SympolColor,
                                (100+col*square+square//2, row*square+square//2),
                                Radius, Circulewidth) 

#printing match info 
def Text():
    PlayersLabel = font1.render("Player: X     VS     AI: O", True, TextColor)
    screen.blit(PlayersLabel, (width // 2 - PlayersLabel.get_width() // 2, 650))

    pygame.draw.rect(screen, (50, 50, 50), (width // 2 - 100, 720, 200, 60), border_radius=10)
    RestartLabel = font1.render("Play Again!", True, (255, 255, 0))
    screen.blit(RestartLabel, (width // 2 - RestartLabel.get_width() // 2, 730))
    #if there is a winner , print the winnig message message 
    if Winner:
        WinnerMsg = font2.render(Winner, True, TextColor)
        screen.blit(WinnerMsg, (width // 2 - WinnerMsg.get_width()//2, 840)) 



#starting the game logic here


#check for available movments by checking any empty cell (returning the index of cells containing 0)
def AvailableMoves(b):
    return [i for i, Available in enumerate(b) if Available == 0] 



#check for any winning lines possible so fisrt second and third row , col and the two diagnol lines 
def CheckWinningLines(Board, p):
    WinningLines = [
        (0,1,2) , (3,4,5), (6,7,8), #rows 
        (0,3,6) , (1,4,7) , (2,5,8), #cols
        (0,4,8) , (2,4,6) #diagnol lines 
    ]

    for combo in WinningLines:
        a, b, c = combo
        if Board[a] == Board[b] == Board[c] == p: #check if any of the winning lines contain the same player in all of the positions 
            return combo #so if the compnation of the line is a winning compnation return the combo , or return nothing if its not a winning compnation
    return None

#check for draw state
def CheckDraw(b):
    return 0 not in b  # if no empty cells are in the boared ( no cell have 0) means all spots are taken 


#the implemnation of the MiniMax algorithm 
def MiniMax(b, depth, MaxPlayer):
    #check for the boared state , is it winning or is it a draw or nothing?
    if CheckWinningLines(b, 2): return 10 - depth #AI wins return positive score
    if CheckWinningLines(b, 1): return depth - 10 #Human wins return negative score
    #we are tryign to maxsimize AI score and minimizw human score 
    if CheckDraw(b): return 0 
#if its the Max player aka AI , set best to a very small number for then maximasing the value 
#AI check all availables moves and how human will play next turn (optimally) and picks movment with maximum score
    if MaxPlayer:
        best = -999
        for m in AvailableMoves(b):
            b[m] = 2
            score = MiniMax(b, depth + 1, False)
            b[m] = 0
            best = max(best, score)
        return best
    else: #we set best for a very bif number to start minimazing 
        best = 999
        for m in AvailableMoves(b):
            b[m] = 1
            score = MiniMax(b, depth + 1, True)
            b[m] = 0
            best = min(best, score)
        return best
    
#here the AI decides on its next move based on the value of each move 
def AI():
    best_score = -999
    move = None
    for m in AvailableMoves(Board):
        Board[m] = 2
        score = MiniMax(Board, 0, False)
        Board[m] = 0
        if score > best_score:
            best_score = score
            move = m
    if move is not None:
        Board[move] = 2

#restaring the game 
def Restart():
    global Board, GameOver, WinnerText, WinningCombo
    Board = [0] * 9
    GameOver = False
    WinnerText = ""
    WinningCombo = None

#print the grid 
DrawLines()

gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart Button
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if width // 2 - 100 <= x <= width // 2 + 100 and 720 <= y <= 780:
                Restart()

        if event.type == pygame.MOUSEBUTTONDOWN and not GameOver:
            x, y = event.pos

            if y > 600 or x < 100 or x > 700:
                continue  # ignore clicks outside board

            row = y // square
            col = (x - 100) // square
            index = row * 3 + col

            if Board[index] == 0:
                Board[index] = 1  # player move

                win = CheckWinningLines(Board, 1)
                if win:
                    WinningLine = win
                    Winner = "YOU WIN!"
                    GameOver = True
                elif CheckDraw(Board):
                    Winner = "DRAW!"
                    GameOver = True
                else:
                    AI()
                    win = CheckWinningLines(Board, 2)
                    if win:
                        WinningLine = win
                        Winner = "AI WINS!"
                        GameOver = True
                    elif CheckDraw(Board):
                        Winner = "DRAW!"
                        GameOver = True

    screen.fill(BoardColor)
    DrawLines()
    XO()
    Text()
    if WinningLine:
        draw_win_line(WinningLine)
    pygame.display.update()


