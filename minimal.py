'''
Minimal Pygame Startup

Useful for testing things like getting sprites to rotate without jumping
around.

run with "python -i minimal.py" to play with it at the interactive prompt
'''

import pygame
pygame.init()
screen = pygame.display.set_mode((200,200))
sprite_image = pygame.image.load('icons/pencil_32.png')
original_image = sprite_image
black = (0, 0, 0, 255)

def draw():
   screen.fill(black)
   screen.blit(sprite_image, sprite_image.get_rect(center=(100,100)))
   pygame.display.update()

def rotate1(angle):
   global sprite_image
   sprite_image = pygame.transform.rotate(original_image, angle)
   draw()

def rotate2(angle):
   # Note: rotozoom had jaggies around the box of the image
   global sprite_image
   sprite_image = pygame.transform.rotozoom(original_image, angle, 1.0)
   draw()

draw()
