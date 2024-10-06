import tkinter as tk
import random

class GameGUI:
    def __init__(self, master, size):
        self.master = master
        self.size = size
        self.cat_i = size // 2
        self.cat_j = size // 2
        self.tiles = [[0 for _ in range(size)] for _ in range(size)]
        self.tiles[self.cat_i][self.cat_j] = 6  # Cat's starting position
        
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        
        # Create the grid of buttons
        self.create_grid()
        self.init_random_blocks()

    def create_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = tk.Button(self.master, width=4, height=2, 
                                command=lambda i=i, j=j: self.handle_click(i, j))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn
        self.update_grid()

    def init_random_blocks(self):
        # Initialize a random number of blocked tiles
        n = random.randint(round(0.067 * (self.size ** 2)), round(0.13 * (self.size ** 2)))
        count = 0
        while count < n:
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
            if self.tiles[i][j] == 0:  # Ensure it's not already blocked
                self.tiles[i][j] = 1  # Mark as blocked
                count += 1
        self.update_grid()

    def update_grid(self):
        # Update the button grid to reflect the tile states
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j] == 6:  # Cat position
                    self.buttons[i][j].config(text="Cat", bg="orange")
                elif self.tiles[i][j] == 1:  # Blocked tile
                    self.buttons[i][j].config(text="X", bg="gray")
                else:
                    self.buttons[i][j].config(text="", bg="white")

    def valid_moves(self):
        # Determine valid moves for the cat
        moves = []
        if self.cat_j < self.size - 1 and self.tiles[self.cat_i][self.cat_j + 1] == 0:
            moves.append("E")
        if self.cat_j > 0 and self.tiles[self.cat_i][self.cat_j - 1] == 0:
            moves.append("W")
        if self.cat_i % 2 == 0:
            if self.cat_i > 0 and self.cat_j < self.size and self.tiles[self.cat_i - 1][self.cat_j] == 0:
                moves.append("NE")
        else:
            if self.cat_i > 0 and self.cat_j < self.size - 1 and self.tiles[self.cat_i - 1][self.cat_j + 1] == 0:
                moves.append("NE")
        if self.cat_i % 2 == 0:
            if self.cat_i > 0 and self.cat_j > 0 and self.tiles[self.cat_i - 1][self.cat_j - 1] == 0:
                moves.append("NW")
        else:
            if self.cat_i > 0 and self.cat_j >= 0 and self.tiles[self.cat_i - 1][self.cat_j] == 0:
                moves.append("NW")
        if self.cat_i % 2 == 0:
            if self.cat_i < self.size - 1 and self.cat_j < self.size and self.tiles[self.cat_i + 1][self.cat_j] == 0:
                moves.append("SE")
        else:
            if self.cat_i < self.size - 1 and self.cat_j < self.size - 1 and self.tiles[self.cat_i + 1][self.cat_j + 1] == 0:
                moves.append("SE")
        if self.cat_i % 2 == 0:
            if self.cat_i < self.size - 1 and self.cat_j > 0 and self.tiles[self.cat_i + 1][self.cat_j - 1] == 0:
                moves.append("SW")
        else:
            if self.cat_i < self.size - 1 and self.cat_j > 0 and self.tiles[self.cat_i + 1][self.cat_j] == 0:
                moves.append("SW")
        return moves

    def target(self, i, j, dir):
        # Determine the new position based on the direction of the move
        if dir == "E":
            return [i, j + 1]
        elif dir == "W":
            return [i, j - 1]
        elif dir == "NE":
            return [i - 1, j] if (i % 2) == 0 else [i - 1, j + 1]
        elif dir == "NW":
            return [i - 1, j - 1] if (i % 2) == 0 else [i - 1, j]
        elif dir == "SE":
            return [i + 1, j] if (i % 2) == 0 else [i + 1, j + 1]
        elif dir == "SW":
            return [i + 1, j - 1] if (i % 2) == 0 else [i + 1, j]

    def handle_click(self, i, j):
        # Handle clicks on the grid and move the cat
        moves = self.valid_moves()
        move = None
        if j == self.cat_j + 1 and i == self.cat_i:
            move = "E"
        elif j == self.cat_j - 1 and i == self.cat_i:
            move = "W"
        elif i == self.cat_i - 1 and j == (self.cat_j if self.cat_i % 2 == 0 else self.cat_j + 1):
            move = "NE"
        elif i == self.cat_i - 1 and j == (self.cat_j - 1 if self.cat_i % 2 == 0 else self.cat_j):
            move = "NW"
        elif i == self.cat_i + 1 and j == (self.cat_j if self.cat_i % 2 == 0 else self.cat_j + 1):
            move = "SE"
        elif i == self.cat_i + 1 and j == (self.cat_j - 1 if self.cat_i % 2 == 0 else self.cat_j):
            move = "SW"
        
        if move in moves:
            new_i, new_j = self.target(self.cat_i, self.cat_j, move)
            self.tiles[self.cat_i][self.cat_j] = 0  # Reset current position
            self.cat_i, self.cat_j = new_i, new_j  # Move the cat
            self.tiles[self.cat_i][self.cat_j] = 6  # Update the new position
            self.update_grid()

            # Check if the cat has reached the boundary (escaped)
            if self.cat_i == 0 or self.cat_j == 0 or self.cat_i == self.size - 1 or self.cat_j == self.size - 1:
                print("Game over! The cat escaped!")
                self.end_game("Game over! The cat escaped!")
        
        else:
            print("Invalid move!")

    def end_game(self, message):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")
        tk.Label(self.master, text=message, font=('Helvetica', 16)).grid(row=self.size, column=0, columnspan=self.size)

# Create the main window
root = tk.Tk()
root.title("Cat Escape Game")

# Create the game
size = 8  # Define grid size
game = GameGUI(root, size)

# Run the GUI loop
root.mainloop()
