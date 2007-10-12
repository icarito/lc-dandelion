import sys, os, pygame
from pygame_ext import pygame_to_pil_img

filename = sys.argv[1]
surface = pygame.image.load(filename)
surface = pygame.transform.scale2x(surface)
image = pygame_to_pil_img(surface)
base, ext = os.path.splitext(filename)
filename = base + '_32' + ext
image.save(filename)
