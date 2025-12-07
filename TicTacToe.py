import pygame
import sys
import random
import math

# game board measurements and configurations
width = 500
height = 600

# board colors
BoardColor = (255, 192, 203)
LineColor = (255, 105, 180)
symbolColor = (255, 62, 163)
TextColor = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe - MiniMax AI")
font1 = pygame.font.SysFont("helvetica", 24)
font2 = pygame.font.SysFont("helvetica", 36)

screen.fill(BoardColor)

# -------------------- GAME STATE --------------------
Board = [0] * 9
GameOver = False
Winner = ""
WinningLine = None
Difficulty = "Difficult"       # "Easy" or "Difficult"
PlayerSymbol = "X"             # "X" or "O" (human)
GameState = "MENU"             # "MENU" or "PLAYING"
square = 360 // 3
LineWidth = 10
ShowMenu = False               # in-game ≡ menu open or not

# board vertical offset (so "Mode:" doesn't overlap)
BOARD_TOP = 60                 # board spans 60 → 60+360=420

# score stats
PlayerWins = 0
AIWins = 0

# animation for winning line & play again button
win_anim_progress = 1.0
pulse_phase = 0.0

# in-game menu button (≡)
menu_button_rect = pygame.Rect(width - 60, 10, 40, 30)

# menu panel: Restart / Start Page / Switch Difficulty
menu_panel_rect = pygame.Rect(width - 210, 50, 200, 150)
restart_option_rect = pygame.Rect(
    menu_panel_rect.x + 10, menu_panel_rect.y + 10,
    menu_panel_rect.width - 20, 35
)
startpage_option_rect = pygame.Rect(
    menu_panel_rect.x + 10, menu_panel_rect.y + 55,
    menu_panel_rect.width - 20, 35
)
switchmode_option_rect = pygame.Rect(
    menu_panel_rect.x + 10, menu_panel_rect.y + 100,
    menu_panel_rect.width - 20, 35
)

# Play Again button (after game over) – clearly below board
play_again_rect = pygame.Rect(width // 2 - 90, 470, 180, 55)

# ------- START MENU RECTS (difficulty + symbol + start) -------
menu_easy_rect  = pygame.Rect(70, 250, 150, 50)
menu_diff_rect  = pygame.Rect(280, 250, 150, 50)
menu_playX_rect = pygame.Rect(70, 320, 150, 50)
menu_playO_rect = pygame.Rect(280, 320, 150, 50)
menu_start_rect = pygame.Rect(130, 410, 240, 60)


# -------------------- DRAWING HELPERS --------------------
def DrawLines():
    for i in range(1, 3):
        # horizontal
        pygame.draw.line(
            screen, LineColor,
            (70, BOARD_TOP + i * square),
            (430, BOARD_TOP + i * square),
            LineWidth
        )
        # vertical
        pygame.draw.line(
            screen, LineColor,
            (70 + i * square, BOARD_TOP),
            (70 + i * square, BOARD_TOP + 3 * square),
            LineWidth
        )


WinColor = (255, 20, 147)


def DrawWinningLine(combo, progress=1.0):
    """Draw the winning line, optionally only a fraction of its full length (0–1)."""
    a, b, c = combo
    row1 = a // 3
    row2 = c // 3
    col1 = a % 3
    col2 = c % 3
    x1 = 70 + col1 * square + square // 2
    x2 = 70 + col2 * square + square // 2
    y1 = BOARD_TOP + row1 * square + square // 2
    y2 = BOARD_TOP + row2 * square + square // 2

    # clamp progress
    p = max(0.0, min(1.0, progress))
    x_mid = x1 + (x2 - x1) * p
    y_mid = y1 + (y2 - y1) * p

    pygame.draw.line(screen, WinColor, (x1, y1), (x_mid, y_mid), LineWidth)


Radius = 50
Circulewidth = 10
CrossWidth = 15
space = 35


def draw_X(row, col):
    pygame.draw.line(
        screen, symbolColor,
        (70 + col * square + space, BOARD_TOP + row * square + space),
        (70 + col * square + square - space, BOARD_TOP + row * square + square - space),
        CrossWidth
    )
    pygame.draw.line(
        screen, symbolColor,
        (70 + col * square + space, BOARD_TOP + row * square + square - space),
        (70 + col * square + square - space, BOARD_TOP + row * square + space),
        CrossWidth
    )


def draw_O(row, col):
    pygame.draw.circle(
        screen, symbolColor,
        (70 + col * square + square // 2, BOARD_TOP + row * square + square // 2),
        Radius, Circulewidth
    )


def XO():
    ai_symbol = "O" if PlayerSymbol == "X" else "X"
    for i in range(9):
        row = i // 3
        col = i % 3
        if Board[i] == 1:  # human
            if PlayerSymbol == "X":
                draw_X(row, col)
            else:
                draw_O(row, col)
        elif Board[i] == 2:  # AI
            if ai_symbol == "X":
                draw_X(row, col)
            else:
                draw_O(row, col)


def DrawMenuButton():
    pygame.draw.rect(screen, (255, 105, 180), menu_button_rect, border_radius=5)
    line_margin_x = 8
    line_margin_y = 6
    line_spacing = 8
    for i in range(3):
        y = menu_button_rect.y + line_margin_y + i * line_spacing
        pygame.draw.line(
            screen, (255, 255, 255),
            (menu_button_rect.x + line_margin_x, y),
            (menu_button_rect.x + menu_button_rect.width - line_margin_x, y),
            2
        )


def DrawMenuPanel():
    pygame.draw.rect(screen, (255, 182, 193), menu_panel_rect, border_radius=10)

    pygame.draw.rect(screen, (255, 105, 180), restart_option_rect, border_radius=8)
    pygame.draw.rect(screen, (255, 105, 180), startpage_option_rect, border_radius=8)
    pygame.draw.rect(screen, (255, 105, 180), switchmode_option_rect, border_radius=8)

    restart_label = font1.render("Restart Game", True, TextColor)
    start_label = font1.render("Go to Start Page", True, TextColor)
    mode_text = f"Switch to {'Easy' if Difficulty == 'Difficult' else 'Difficult'}"
    mode_label = font1.render(mode_text, True, TextColor)

    screen.blit(
        restart_label,
        (restart_option_rect.centerx - restart_label.get_width() // 2,
         restart_option_rect.centery - restart_label.get_height() // 2)
    )
    screen.blit(
        start_label,
        (startpage_option_rect.centerx - start_label.get_width() // 2,
         startpage_option_rect.centery - start_label.get_height() // 2)
    )
    screen.blit(
        mode_label,
        (switchmode_option_rect.centerx - mode_label.get_width() // 2,
         switchmode_option_rect.centery - mode_label.get_height() // 2)
    )


def DrawPlayAgainButton():
    global pulse_phase
    # pulsing outer glow
    glow = (math.sin(pulse_phase) + 1) / 2  # 0..1
    inflated = play_again_rect.inflate(int(16 * glow), int(10 * glow))
    pygame.draw.rect(screen, (255, 192, 203), inflated, border_radius=16)

    pygame.draw.rect(screen, (255, 105, 180), play_again_rect, border_radius=12)
    RestartLabel = font1.render("Play Again", True, TextColor)
    screen.blit(
        RestartLabel,
        (play_again_rect.centerx - RestartLabel.get_width() // 2,
         play_again_rect.centery - RestartLabel.get_height() // 2)
    )


def Text():
    # Mode info at the VERY top
    mode_label = font1.render(f"Mode: {Difficulty}", True, TextColor)
    screen.blit(mode_label, (20, 10))

    # Win stats instead of showing symbols
    score_label = font1.render(f"You: {PlayerWins}     VS     AI: {AIWins}", True, TextColor)
    screen.blit(score_label, (width // 2 - score_label.get_width() // 2, 430))

    if Winner:
        WinnerMsg = font2.render(Winner, True, TextColor)
        # toool el text
        screen.blit(WinnerMsg, (width // 2 - WinnerMsg.get_width() // 2, 530))


# -------------------- START MENU DRAWING --------------------
def DrawStartMenu():
    screen.fill(BoardColor)

    title = font2.render("Tic Tac Toe - Minimax AI", True, TextColor)
    screen.blit(title, (width // 2 - title.get_width() // 2, 80))

    subtitle = font1.render("Choose difficulty and your symbol", True, TextColor)
    screen.blit(subtitle, (width // 2 - subtitle.get_width() // 2, 130))

    # difficulty buttons - selected is darker pink
    easy_color = (255, 20, 147) if Difficulty == "Easy" else (255, 182, 193)
    diff_color = (255, 20, 147) if Difficulty == "Difficult" else (255, 182, 193)

    pygame.draw.rect(screen, easy_color, menu_easy_rect, border_radius=10)
    pygame.draw.rect(screen, diff_color, menu_diff_rect, border_radius=10)

    easy_label = font1.render("Easy", True, TextColor)
    diff_label = font1.render("Difficult", True, TextColor)

    screen.blit(easy_label, (menu_easy_rect.centerx - easy_label.get_width() // 2,
                             menu_easy_rect.centery - easy_label.get_height() // 2))
    screen.blit(diff_label, (menu_diff_rect.centerx - diff_label.get_width() // 2,
                             menu_diff_rect.centery - diff_label.get_height() // 2))

    # symbol buttons - selected is darker pink
    x_color = (255, 20, 147) if PlayerSymbol == "X" else (255, 182, 193)
    o_color = (255, 20, 147) if PlayerSymbol == "O" else (255, 182, 193)

    pygame.draw.rect(screen, x_color, menu_playX_rect, border_radius=10)
    pygame.draw.rect(screen, o_color, menu_playO_rect, border_radius=10)

    x_label = font1.render("Play as X", True, TextColor)
    o_label = font1.render("Play as O", True, TextColor)

    screen.blit(x_label, (menu_playX_rect.centerx - x_label.get_width() // 2,
                          menu_playX_rect.centery - x_label.get_height() // 2))
    screen.blit(o_label, (menu_playO_rect.centerx - o_label.get_width() // 2,
                          menu_playO_rect.centery - o_label.get_height() // 2))

    # start button - deep pink
    pygame.draw.rect(screen, (255, 20, 147), menu_start_rect, border_radius=12)
    start_label = font1.render("Start Game", True, TextColor)
    screen.blit(start_label, (menu_start_rect.centerx - start_label.get_width() // 2,
                              menu_start_rect.centery - start_label.get_height() // 2))


# -------------------- GAME LOGIC --------------------
def AvailableMoves(b):
    return [i for i, Available in enumerate(b) if Available == 0]


def CheckWinningLines(Board, p):
    WinningLines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for combo in WinningLines:
        a, b, c = combo
        if Board[a] == Board[b] == Board[c] == p:
            return combo
    return None


def CheckDraw(b):
    return 0 not in b


def MiniMax(b, depth, MaxPlayer):
    if CheckWinningLines(b, 2):
        return 10 - depth
    if CheckWinningLines(b, 1):
        return depth - 10
    if CheckDraw(b):
        return 0

    if MaxPlayer:  # AI = maximizing player (2)
        best = -1000
        for m in AvailableMoves(b):
            b[m] = 2
            score = MiniMax(b, depth + 1, False)
            b[m] = 0
            best = max(best, score)
        return best
    else:          # Human = minimizing player (1)
        best = 1000
        for m in AvailableMoves(b):
            b[m] = 1
            score = MiniMax(b, depth + 1, True)
            b[m] = 0
            best = min(best, score)
        return best


def AI():
    if Difficulty == "Easy":
        available = AvailableMoves(Board)
        if available:
            move = random.choice(available)
            Board[move] = 2
    else:
        best_score = -1000
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


def Restart():
    global Board, GameOver, Winner, WinningLine, ShowMenu, win_anim_progress
    Board = [0] * 9
    GameOver = False
    Winner = ""
    WinningLine = None
    ShowMenu = False
    win_anim_progress = 1.0


def StartGame():
    global GameState
    Restart()
    GameState = "PLAYING"
    # If player chose O, AI (as X) starts first.
    if PlayerSymbol == "O":
        AI()


# -------------------- MAIN LOOP --------------------
clock = pygame.time.Clock()
gameOn = True
while gameOn:
    dt = clock.tick(60) / 1000.0  # frame time (seconds)
    pulse_phase += dt * 4         # speed of pulsing

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- EVENTS ON START MENU ----------
        if GameState == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_easy_rect.collidepoint(x, y):
                    Difficulty = "Easy"
                elif menu_diff_rect.collidepoint(x, y):
                    Difficulty = "Difficult"
                elif menu_playX_rect.collidepoint(x, y):
                    PlayerSymbol = "X"
                elif menu_playO_rect.collidepoint(x, y):
                    PlayerSymbol = "O"
                elif menu_start_rect.collidepoint(x, y):
                    StartGame()

        # ---------- EVENTS DURING GAME PLAY ----------
        elif GameState == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # ≡ menu toggle
                if menu_button_rect.collidepoint(x, y):
                    ShowMenu = not ShowMenu
                    continue

                # in-game menu panel options
                if ShowMenu:
                    if restart_option_rect.collidepoint(x, y):
                        Restart()
                        if PlayerSymbol == "O":
                            AI()
                        continue
                    if startpage_option_rect.collidepoint(x, y):
                        Restart()
                        GameState = "MENU"
                        continue
                    if switchmode_option_rect.collidepoint(x, y):
                        Difficulty = "Easy" if Difficulty == "Difficult" else "Difficult"
                        ShowMenu = False
                        continue
                    # click outside panel & button closes menu
                    if (not menu_panel_rect.collidepoint(x, y) and
                            not menu_button_rect.collidepoint(x, y)):
                        ShowMenu = False

                # Play Again button after game over
                if GameOver and play_again_rect.collidepoint(x, y):
                    Restart()
                    if PlayerSymbol == "O":
                        AI()
                    continue

                # Handle board clicks only if game is active
                if not GameOver and BOARD_TOP <= y <= BOARD_TOP + 3 * square and 70 <= x <= 430:
                    row = (y - BOARD_TOP) // square
                    col = (x - 70) // square
                    index = row * 3 + col

                    if 0 <= index < 9 and Board[index] == 0:
                        Board[index] = 1  # human move
                        win = CheckWinningLines(Board, 1)
                        if win:
                            WinningLine = win
                            Winner = "YOU WIN!"
                            GameOver = True
                            PlayerWins += 1
                            win_anim_progress = 0.0
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
                                AIWins += 1
                                win_anim_progress = 0.0
                            elif CheckDraw(Board):
                                Winner = "DRAW!"
                                GameOver = True

    # progress winning-line animation
    if GameOver and WinningLine and win_anim_progress < 1.0:
        win_anim_progress += dt * 3  # animation speed

    # ---------- DRAWING ----------
    if GameState == "MENU":
        DrawStartMenu()
    else:
        screen.fill(BoardColor)
        DrawLines()
        XO()
        if WinningLine:
            DrawWinningLine(WinningLine, win_anim_progress)
        Text()
        DrawMenuButton()
        if ShowMenu:
            DrawMenuPanel()
        if GameOver:
            DrawPlayAgainButton()

    pygame.display.update()
