import pygame
import sys
import random

#game board measurments and configrations 
width = 800
height = 900

#board colors
BoardColor = (255, 192, 203)  
LineColor= (255, 105, 180)  
symbolColor= (255, 105, 180)  
TextColor = (255, 255, 255) 

#starting the game using pygame
pygame.init()
screen = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("Tic Tac Toe - MiniMax AI")
font1 = pygame.font.SysFont("helvetica", 40)
font2 = pygame.font.SysFont("helvetica", 60) 

screen.fill(BoardColor)  

#setting the board to start 
Board = [0] * 9   
GameOver = False 
Winner = ""
WinningLine= None         #check and store a winning line that consist of 3 cells either horizantal vertical or diagonal
Difficulty = "Difficult"  #Easy or Difficult
square= 600 // 3          #one square containing the player symbol X or O
LineWidth = 15 

# making the grid lines 
def DrawLines():
    for i in range(1,3): 
        pygame.draw.line(screen, LineColor, (100, i*square), (700, i*square), LineWidth)
        pygame.draw.line(screen, LineColor, (100 + i*square, 0), (100 + i*square, 600), LineWidth)

WinColor= (255, 20, 147)   
def DrawWinningLine(combo):
    a, b, c = combo
    row1 = a // 3
    row2 = c // 3
    col1 = a % 3
    col2 = c % 3
    x1 = 100 + col1*square + square // 2
    x2 = 100 + col2*square + square // 2
    y1 = row1*square + square // 2
    y2 = row2*square + square // 2
    pygame.draw.line(screen, WinColor, (x1, y1), (x2, y2), LineWidth) 


Radius= 80 
Circulewidth= 15
CrossWidth= 25
space = 55 

# printing X/O symbols on Board 
def XO():
    #for each spot on the tic tac toe board, set up the cordinates of the rows and cols to start
    for i in range(9): 
        row = i // 3 
        col = i % 3

        #if this position in the Board have a value of 1 then its taken by player X , draw the X symbol by drawing two lines
        if Board[i] == 1:   
            pygame.draw.line(screen, symbolColor,
                                (100+col*square+space, row*square+space),
                                (100+col*square+square-space, row*square+square-space),
                                CrossWidth)
            pygame.draw.line(screen, symbolColor,
                                (100+col*square+space, row*square+square-space),
                                (100+col*square+square-space, row*square+space),
                                CrossWidth)

        #if this position is not taken by Player X check if its taken by player O, if the position have the value 2 then it i staken by player O, draw the circule 
        elif Board[i] == 2:  
            pygame.draw.circle(screen, symbolColor,
                                (100+col*square+square//2, row*square+square//2),
                                Radius, Circulewidth) 

#printing the match/game info 
def Text():
    PlayersLabel = font1.render("Player: X     VS     AI: O", True, TextColor)
    screen.blit(PlayersLabel, (width // 2 - PlayersLabel.get_width() // 2, 650))

    #setting up the difficulty options (easy mode or difficult mode)
    EasyColor = (100, 200, 100) if Difficulty == "Easy" else (50, 50, 50)
    DifficultColor = (200, 50, 50) if Difficulty == "Difficult" else (50, 50, 50)

    pygame.draw.rect(screen, EasyColor, (200, 720, 150, 60), border_radius=10)
    pygame.draw.rect(screen, DifficultColor, (450, 720, 150, 60), border_radius=10)

    EasyLabel = font1.render("Easy", True, TextColor)
    DifficultLabel = font1.render("Difficult", True, TextColor)

    screen.blit(EasyLabel, (275 - EasyLabel.get_width() // 2, 735))
    screen.blit(DifficultLabel, (525 - DifficultLabel.get_width() // 2, 735))

    #setting the draw and play again option
    pygame.draw.rect(screen, (50, 50, 50), (width // 2 - 100, 800, 200, 60), border_radius=10)
    RestartLabel = font1.render("Play Again!", True, (255, 255, 0))
    screen.blit(RestartLabel, (width // 2 - RestartLabel.get_width() // 2, 810))

    #if there is a winner , print the winnig message message 
    if Winner:
        WinnerMsg = font2.render(Winner, True, TextColor)
        screen.blit(WinnerMsg, (width // 2 - WinnerMsg.get_width()//2, 840)) 


#Starting the game logic


#check for available movments by checking any empty cell (returning the index of cells containing 0)
def AvailableMoves(b):
    return [i for i, Available in enumerate(b) if Available == 0] 

#board layout is going to be like this :
# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8 

#check for any winning lines possible >> rows,cols and the two diagnol lines
def CheckWinningLines(Board, p):
    WinningLines = [
        (0,1,2) , (3,4,5), (6,7,8), #rows 
        (0,3,6) , (1,4,7) , (2,5,8), #cols
        (0,4,8) , (2,4,6) #diagnol lines 
    ]

    #check if any of the winning lines contain the same player in all of the positions , if so the line is a winning line ; return the combo , or return nothing
    for combo in WinningLines:
        a, b, c = combo
        if Board[a] == Board[b] == Board[c] == p: 
            return combo 
    return None

#check for draw state, if no empty cells are in the board (no cell have 0) means all spots are taken by one of the players
def CheckDraw(b):
    return 0 not in b  


#the Implemntation of the MiniMax algorithm 
def MiniMax(b, depth, MaxPlayer):
    #check for the boared state 
    if CheckWinningLines(b, 2): 
        return 10 - depth #AI wins return positive score
    if CheckWinningLines(b, 1): 
        return depth - 10 #Human wins return negative score
    if CheckDraw(b): 
        return 0 

    #if its the Max player turn aka AI , set best to a very small number for then maximazing the value , AI check all availables moves and how human will play accordinglly to each of the moves next turn (assuming optimally) and picks movment with the maximum score
    if MaxPlayer:
        best = -1000
        for m in AvailableMoves(b):                 #loop over all possible moves for the max player 
            b[m] = 2                                #placeholder to test all the other movments against 
            score = MiniMax(b, depth + 1, False)    #recursivly call the function but here its the min player turn (human player) simulate the player move based on the previous move here 
            b[m] = 0                                #remove the mark of the max player last move to test a diffrent available mode
            best = max(best, score)                 # check the score against the best score and take the maximum to keep record of the actual best move to make 
        return best 

    #we set best for a very big number to start minimazing , this is the part for the min player turn (human player)
    else:                                            
        best = 1000
        for m in AvailableMoves(b):                 #just like the Max turn , but the oppisiot to minimize this player advantages 
            b[m] = 1
            score = MiniMax(b, depth + 1, True)     #we call the function recusvly to the max player turn to check for the movments based on this current move
            b[m] = 0                                #undo the move above , its important to do this since this function simulates all moves possible but makes no actual move in the game 
            best = min(best, score)                 #return the worst possible case meaning the case with the min score as best
        return best


#here the AI decides on its next move based on the value of each move using the above MiniMax algorithm  
def AI():
    # Random moves based on the empty spots on the board , no much testing 
    if Difficulty == "Easy":
        available = AvailableMoves(Board)
        if available:
            move = random.choice(available)
            Board[move] = 2

    # Difficult mode makes smarter choices and better moves using MiniMax algorithm
    else: 
        best_score = -1000
        move = None
        for m in AvailableMoves(Board):
            Board[m] = 2
            #using MiniMax algorithm the AI evaluate all possible moves and picks the moves with the better score
            score = MiniMax(Board, 0, False)
            Board[m] = 0
            if score > best_score:    
                best_score = score
                move = m
        if move is not None:
            Board[move] = 2

#restaring the game by returning all varibales to their original state
def Restart():
    global Board, GameOver, Winner, WinningLine, Difficulty
    Board = [0] * 9 
    GameOver = False 
    Winner = ""
    WinningLine = None


#print the grid to start the game 
DrawLines()
gameOn = True
while gameOn:
    #quiting game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 

        #Restart option display 
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if width // 2 - 100 <= x <= width // 2 + 100 and 800 <= y <= 860:
                Restart()
            if not GameOver or all(cell == 0 for cell in Board): #if the game is not on aor no places are empty in the game 
                if 200 <= x <= 350 and 720 <= y <= 780:
                    Difficulty = "Easy"
                    Restart()
                elif 450 <= x <= 600 and 720 <= y <= 780:
                    Difficulty = "Difficult"
                    Restart()


        if event.type == pygame.MOUSEBUTTONDOWN and not GameOver: #ignore any clicks outside board
            x, y = event.pos
            if y > 600 or x < 100 or x > 700:
                continue  

            row = y // square
            col = (x - 100) // square
            index = row * 3 + col
            if Board[index] == 0: #if spot is empty player can play in it 
                Board[index] = 1 
                #check for any winning line/draw state after the move with the current board state and display it and end the game by setting GameOver to True
                win = CheckWinningLines(Board, 1)
                if win:
                    WinningLine = win
                    Winner = "YOU WIN!"
                    GameOver = True
                elif CheckDraw(Board):
                    Winner = "DRAW!"
                    GameOver = True

                #if no, then AI playes its turn check for any winning line/draw state after the move with the current board state and display it and end the game by setting GameOver to True
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

    #setting the board by drawing all the grid lines, symbols, text and if any player wins the line on the winning line
    screen.fill(BoardColor) 
    DrawLines()
    XO()
    if WinningLine:
        DrawWinningLine(WinningLine)
    Text()
    pygame.display.update()


