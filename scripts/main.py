import client_cognex
import plc_connection
from tictactoe import TicTacToe
import time

board = [[" " for _ in range(3)] for _ in range(3)]
list_board = [cell for row in board for cell in row]

BOARD_COORIDNATES = {
    '0': {'x': -90.0, 'y': -30.0},
    '1': {'x': -20.0, 'y': 20.0},
    '2': {'x': 45.0, 'y': 55.0},
    '3': {'x': -130.0, 'y': 40.0},
    '4': {'x': -65.0, 'y': 95.0},
    '5': {'x': 5.0, 'y': 130.0},
    '6': {'x': -170.0, 'y': 110.0},
    '7': {'x': -100.0, 'y': 150.0},
    '8': {'x': -35.0, 'y': 210.0},
}

FREE_TOKEN_COORDINATES = {
    '0': {'x': 80.0, 'y': -15.0},
    '1': {'x': -20.0, 'y': -80.0},
    '2': {'x': -130.0, 'y': -140.0},
    '3': {'x': -190.0, 'y': -50.0},
    '4': {'x': -280.0, 'y': 20.0},
    }

z_high = -400.0
z_low = -530.0
#print("Cognex Data:", data)
print()

token = 0 
game = TicTacToe(my_token='X', opponent_token='O', board=list_board)

previous_turn_state = 0  # Initialize previous state as off
waiting_for_off = False  # Flag to wait for signal to turn off

print("Starting Tic Tac Toe Game")

plc_connection.write_go_out_home_plc()
time.sleep(4)
plc_connection.write_go_home_plc()
time.sleep(4)

if game.game_over():
    print("Game already over, exiting.")
    
while not game.game_over():
    # send plc signal to go home
    #plc_connection.write_go_home_plc()  # Reset coordinates to home position
    #my_turn = plc_connection.read_my_turn()
    my_turn = plc_connection.read_my_turn_memory()  # Read the current turn state from PLC
    #my_turn = 1  # For testing purposes, we assume it's always our turn
    if my_turn == 1 and previous_turn_state == 0 and not waiting_for_off:
        print("It's my turn!")
        done_turn = False
        
        data, unused_token_coordinates = client_cognex.get_cognex_data()

        cell_data_ids = sorted((id_ for id_ in data.keys() if data[id_]['class'] == ' '), key=lambda x: int(x))
        print("Cell Data IDs:", cell_data_ids)
        token_data_ids = sorted({id_ for id_ in data.keys() if data[id_]['class'] == 'X' or data[id_]['class'] == 'O'}, key=lambda x: int(x))
        print("Token Data IDs:", token_data_ids)

        cell_data = {id_: data[id_] for id_ in cell_data_ids}
        token_data = {id_: data[id_] for id_ in token_data_ids}

        #print("Cell Data:", cell_data)
        #print("Token Data:", token_data)

        # Interpret data as a tic tac toe board
        x_values = [data[id_]['x'] for id_ in cell_data_ids if data[id_]['x']!= 0.0]
        y_values = [data[id_]['y'] for id_ in cell_data_ids if data[id_]['y']!= 0.0]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        max_dev = 200

        for id_ in data.keys():
            x = data[id_]['x']
            y = data[id_]['y']
            if y < min_y + max_dev:
                row = 0
            elif y > max_y - max_dev:
                row = 2
            else:
                row = 1

            if x < min_x + max_dev:
                col = 0
            elif x > max_x - max_dev:
                col = 2
            else:
                col = 1
            if board[row][col] == " ":
                board[row][col] = data[id_]['class']

        list_board = [cell for row in board for cell in row]
        print('List Board:', list_board)

        game.board = list_board
        print("Past Board State:")
        game.print_board()
        move = game.get_best_move()
        game.make_move(move, game.my_token)

        # Update PLC with the new board state
        board_x = BOARD_COORIDNATES[str(move)]['x']
        board_y = BOARD_COORIDNATES[str(move)]['y']

        token_x = FREE_TOKEN_COORDINATES[str(token)]['x']
        token_y = FREE_TOKEN_COORDINATES[str(token)]['y']

        token += 1

        print("Current Board State:")
        game.print_board()
        
        print(f"Making move at position {move} with coordinates ({board_x}, {board_y})")

        waiting_for_off = True

        print(f"Moving to token {token} at ({token_x}, {token_y})")
        print(f"Moving to Z high: {z_high}")
        plc_connection.write_oef__plc(token_x, token_y, z_high)
        plc_connection.activate_start_play()
        time.sleep(4)
        # Go down
        print(f"Moving to Z low: {z_low}")
        plc_connection.write_oef__plc(token_x, token_y, z_low)
        plc_connection.activate_start_play()
        time.sleep(4)

        # Close the gripper
        print("Closing gripper")
        plc_connection.close_gripper()
        time.sleep(1)

    ## Go above the token
        print(f"Moving to Z high: {z_high}")
        plc_connection.write_oef__plc(token_x, token_y, z_high)
        plc_connection.activate_start_play()
        time.sleep(4)

        # Go above the board position
        print(f"Moving to board position {move} at ({board_x}, {board_y})")
        print(f"Moving to Z high: {z_high}")
        plc_connection.write_oef__plc(board_x, board_y, z_high)
        plc_connection.activate_start_play()
        time.sleep(4)

        # Go down the board position
        print(f"Moving to Z low: {z_low}")
        plc_connection.write_oef__plc(board_x, board_y, z_low)
        plc_connection.activate_start_play()
        time.sleep(4)

        # Open the gripper
        print("Closing gripper")
        plc_connection.open_gripper()
        time.sleep(1)

        # Go above the board position
        print(f"Moving to board position {move} at ({board_x}, {board_y})")
        print(f"Moving to Z high: {z_high}")
        plc_connection.write_oef__plc(board_x, board_y, z_high)
        plc_connection.activate_start_play()
        time.sleep(4)

        # Go home
        print("Going home")
        plc_connection.activate_conveyor()
        plc_connection.write_go_home_plc()
        time.sleep(4)
        plc_connection.deactivate_conveyor()
    elif my_turn == 0 and waiting_for_off:
        # Signal turned off, we can reset and wait for next rising edge
        waiting_for_off = False
        print("Signal turned off, waiting for next turn")
    
    # Update previous state
    previous_turn_state = my_turn

print("Game Over!")


    


