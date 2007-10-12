import Image # from PIL
import pygame

def pygame_to_pil_img(pg_img):
  imgstr = pygame.image.tostring(pg_img, 'RGB')
  return Image.fromstring('RGB', pg_img.get_size(), imgstr)

def pil_to_pygame_img(pil_img):
  imgstr = pil_img.tostring()
  return pygame.image.fromstring(imgstr, pil_img.size, 'RGB')

