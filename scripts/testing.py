import plc_connection
import time 
import random

BOARD_COORIDNATES = {
    '0': {'x': -100.0, 'y': -15.0},
    '1': {'x': -25.0, 'y': 25.0},
    '2': {'x': 40.0, 'y': 70.0},
    '3': {'x': -140.0, 'y': 50.0},
    '4': {'x': -70.0, 'y': 100.0},
    '5': {'x': -5.0, 'y': 145.0},
    '6': {'x': -175.0, 'y': 120.0},
    '7': {'x': -105.0, 'y': 170.0},
    '8': {'x': -40.0, 'y': 220.0},
}

FREE_TOKEN_COORDINATES = {
    '0': {'x': 75.0, 'y': -10.0},
    '1': {'x': -25.0, 'y': -65.0},
    '2': {'x': -135.0, 'y': -130.0},
    '3': {'x': -185.0, 'y': -35.0},
    '4': {'x': -270.0, 'y': 30.0},
    }

z_high = -400.0
z_low = -522.0
z_1_low = -520.0
z_2_low = -520.0
z_3_low = -505.0
z_4_low = -505.0
z_5_low = -495
x = FREE_TOKEN_COORDINATES['1']['x']  # Initial X position
y = FREE_TOKEN_COORDINATES['1']['y']  # Initial Y position
plc_connection.write_oef__plc(x, y, -522)  # Set initial position to high Z
plc_connection.activate_start_play()  # Activate start play signal
time.sleep(4)


    