# Tic Tac Toe - MiniMax AI

A beautiful, interactive Tic Tac Toe game built with Python and Pygame, featuring an unbeatable AI opponent powered by the MiniMax algorithm.

## Features

- **Smart AI Opponent**: Uses the MiniMax algorithm for optimal gameplay
- **Two Difficulty Modes**: 
  - **Easy**: Random move selection for casual play
  - **Hard**: Unbeatable AI using MiniMax algorithm
- **Symbol Selection**: Choose to play as X or O
- **Beautiful Pink UI**: Eye-catching gradient pink theme with smooth animations
- **Score Tracking**: Keeps track of wins for both player and AI
- **Interactive Menu**: In-game menu for restarting, changing difficulty, or returning to start screen
- **Winning Animation**: Animated line drawing to highlight the winning combination

## Purpose

This project demonstrates the implementation of the **MiniMax algorithm** in game theory, showcasing how artificial intelligence can make optimal decisions in a zero-sum game. The game provides an educational example of:

- Game tree traversal
- Recursive algorithm implementation
- UI/UX design with Pygame
- State management in game development

## Installation & Setup

### Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Step 1: Install Python (if not already installed)

**Windows:**
```powershell
# Download from https://www.python.org/downloads/
# Or use Windows Store
```

### Step 2: Install Pygame

**Open your terminal (PowerShell on Windows) and run:**
```powershell
pip install pygame
```

### Step 3: Run the game

**go to game directory and run:**
```powershell
python TicTacToe.py
```
or simply
```powershell
py TicTacToe.py
```

## How to Play?

### Start Menu
1. **Select Difficulty**: Choose between Easy or Hard mode
   - Easy: AI makes random moves
   - Hard: AI uses MiniMax algorithm (nearly impossible to beat!)
2. **Choose Your Symbol**: Select whether you want to play as X or O
   - If you choose O, the AI (as X) will make the first move
3. **Click "Start Game"** to begin

### During Gameplay
- **Make Your Move**: Click on any empty cell on the board to place your symbol
- **AI Response**: The AI will automatically make its move after yours
- **Win Condition**: Get three of your symbols in a row (horizontally, vertically, or diagonally)
- **Score Display**: Your wins vs AI wins are shown below the board

### In-Game Menu (≡ button)
Click the menu button in the top-right corner to access:
- **Restart Game**: Start a fresh round with the same settings
- **Go to Start Page**: Return to the main menu to change difficulty or symbol
- **Switch Difficulty**: Toggle between Easy and Hard mode mid-game

### After Game Ends
- A winning line animation will highlight the winning combination
- Your result (YOU WIN! / AI WINS! / DRAW!) will be displayed
- Click the **"Play Again"** button to start another round

## How the AI Works

### MiniMax Algorithm
The AI in Hard mode uses the **MiniMax algorithm**, a recursive decision-making algorithm:

1. **Maximizing Player (AI)**: Tries to maximize its score
2. **Minimizing Player (Human)**: Tries to minimize the AI's score
3. **Game Tree Exploration**: The algorithm explores all possible future game states
4. **Scoring System**:
   - AI wins: +10 points (minus depth for faster wins)
   - Human wins: -10 points (plus depth)
   - Draw: 0 points
5. **Optimal Decision**: The AI selects the move with the highest score

This makes the AI virtually **unbeatable** in Hard mode - the best you can do is draw!
