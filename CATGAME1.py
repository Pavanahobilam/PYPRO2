import random

class Game:
    def __init__(self, size):
        self.size = size
        self.cat_i = size // 2
        self.cat_j = size // 2
        self.tiles = [[0 for _ in range(size)] for _ in range(size)]
        self.tiles[self.cat_i][self.cat_j] = 6  # Cat's starting position
        self.deadline = 0
        self.terminated = False

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

    def play(self):
        self.init_random_blocks()
        while True:
            moves = self.valid_moves()
            if not moves:
                print("Game over! You won!")
                break
            print("Valid moves:", moves)
            move = input("Enter a move (E, W, NE, NW, SE, SW): ").strip().upper()
            if move not in moves:
                print("Invalid move! Try again.")
                continue
            new_i, new_j = self.target(self.cat_i, self.cat_j, move)
            self.tiles[self.cat_i][self.cat_j] = 0  # Reset current position
            self.cat_i, self.cat_j = new_i, new_j  # Move the cat
            self.tiles[self.cat_i][self.cat_j] = 6  # Update the new position

            # Check if the cat has reached the boundary (escaped)
            if self.cat_i == 0 or self.cat_j == 0 or self.cat_i == self.size - 1 or self.cat_j == self.size - 1:
                print("Game over! The cat escaped!")
                break

# Example to run the game
size = int(input("Enter the size of the grid: "))
game = Game(size)
game.play()
