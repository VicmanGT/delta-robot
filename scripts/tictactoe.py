class TicTacToe:
    def __init__(self, my_token, opponent_token, board):
        # Initialize empty board (using ' ' for empty squares)
        self.board = board
        self.opponent_token = opponent_token
        self.my_token = my_token

    def print_board(self):
        """Print the current state of the board"""
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("---------")

    def available_moves(self):
        """Returns list of available moves (indices of empty squares)"""
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def make_move(self, position, player):
        """Make a move on the board"""
        if self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        """Check if there's a winner. Returns winner symbol or None"""
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != " ":
                return self.board[i]

        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != " ":
                return self.board[i]

        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]

        return None

    def is_board_full(self):
        """Check if the board is full"""
        #print(" " not in self.board)
        return " " not in self.board

    def game_over(self):
        """Check if the game is over"""
        return self.check_winner() is not None or self.is_board_full()

    def minimax(self, depth, is_maximizing):
        """
        Minimax algorithm implementation
        Returns the best score possible for the current board state
        """
        # Base cases
        winner = self.check_winner()
        if winner == self.my_token:
            return 1
        if winner == self.opponent_token:
            return -1
        if self.is_board_full():
            return 0

        # if it is the maximizing player's turn (AI), we want to maximize the score
        if is_maximizing:
            best_score = float("-inf")
            for move in self.available_moves():
                # Make a calculating move
                self.board[move] = self.my_token
                # Recursively call minimax with the next depth and the minimizing player
                score = self.minimax(depth + 1, False)
                # Reset the move
                self.board[move] = " "
                # Update the best score
                best_score = max(score, best_score)
            return best_score
        else:
            # if it is the minimizing player's turn (human), we want to minimize the score
            best_score = float("inf")
            for move in self.available_moves():
                # Make a calculating move
                self.board[move] = self.opponent_token
                # Recursively call minimax with the next depth and the maximizing player
                score = self.minimax(depth + 1, True)
                # Reset the move
                self.board[move] = " "
                # Update the best score
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        """Find the best move for AI using minimax"""
        best_score = float("-inf")
        best_move = None

        for move in self.available_moves():
            # Make a calculating move
            self.board[move] = self.my_token
            # Recursively call minimax with the next depth and the minimizing player
            score = self.minimax(0, False)
            # Reset the move
            self.board[move] = " "

            # Update the best score
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def play_game(self):
        """Main game loop"""
        print("Welcome to Tic Tac Toe!")
        print("You are 'O' and the AI is 'X'")
        print("Enter positions (0-8) as shown below:")
        print("0 | 1 | 2")
        print("---------")
        print("3 | 4 | 5")
        print("---------")
        print("6 | 7 | 8")
        print("\n")

        # Randomly decide who goes first
        import random

        ai_turn = random.choice([True, False])

        while not self.game_over():
            self.print_board()

            if ai_turn:
                print("\nAI's turn...")
                move = self.get_best_move()
                self.make_move(move, self.my_token)
            else:
                while True:
                    try:
                        move = int(input("\nYour turn (0-8): "))
                        if 0 <= move <= 8 and self.make_move(move, self.opponent_token):
                            break
                        else:
                            print("Invalid move! Try again.")
                    except ValueError:
                        print("Please enter a number between 0 and 8!")

            ai_turn = not ai_turn

        # Game over
        self.print_board()
        winner = self.check_winner()
        if winner == self.my_token:
            print("\nAI wins!")
        elif winner == self.opponent_token:
            print("\nCongratulations! You win!")
        else:
            print("\nIt's a tie!")


# Start the game
if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
