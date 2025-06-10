import pygame
import os

pygame.mixer.init()

pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
pygame.mixer.music.load(os.path.join(os.getcwd(), "sounds", "its_time.mp3"))
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)  # Wait until the music finishes playing