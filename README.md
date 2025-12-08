# Tic Tac Toe with MiniMax

## Features

- **Smart AI Opponent**: Uses the MiniMax algorithm
- **Two Difficulty Modes**: 
  - **Easy**: Random move selection for casual play
  - **Hard**: Unbeatable AI using MiniMax algorithm
- **Choose to play as X or O**
- **Score Tracking**

## Purpose

This project demonstrates the implementation of the **MiniMax algorithm** in game theory, showing how artificial intelligence can make optimal decisions in a zero-sum game. The game provides an example of:

- Game tree traversal
- Recursive algorithm implementation
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
**or simply**
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
- **Win Condition**: Get three of your symbols in a row
- **Score Display**: Your wins vs AI wins are counted below the board

### In-Game Menu
Click the menu button in the top-right corner to access:
- **Restart Game**: Start a new round with the same settings
- **Go to Start Page**
- **Switch Difficulty**: Toggle between Easy and Hard mode mid-game

### After Game Ends
- A winning line animation will highlight the winning combination
- Your result (YOU WIN! / AI WINS! / DRAW!) will be displayed
- Click the **"Play Again"** button to start another round
