import Image, ImageDraw
import pygame
from pygame_ext import pygame_to_pil_img
from pygame_ext import Color
from pygame_ext import draw_rounded_rect, draw_line

def hex(size):
  img = Image.new('RGBA', size, (255,255,255,255))
  draw = ImageDraw.Draw(img)
  x,y = size
  points = [(x/2.0,y),(x,y*2.0/3.0),(x,y/3.0),(x/2.0,0),(0,y/3.0),(0,y*2.0/3.0)]
  draw.polygon(points,fill="green", outline="black")
  del draw
  return img

def rect(size):
    surface = pygame.Surface(size)
    surface.fill(Color.white)
    rect = surface.get_rect()
    rect.inflate_ip(-3, -3)
    pygame.draw.rect(surface, Color.black, rect, 2)
    image = pygame_to_pil_img(surface)
    image.save('icons/rect_32.png')

def ellipse(size):
    surface = pygame.Surface(size)
    surface.fill(Color.white)
    rect = surface.get_rect()
    rect.inflate_ip(-3, -3)
    pygame.draw.ellipse(surface, Color.black, rect, 2)
    image = pygame_to_pil_img(surface)
    image.save('icons/ellipse_32.png')

def line(size):
    surface = pygame.Surface(size)
    surface.fill(Color.white)
    rect = surface.get_rect()
    rect.inflate_ip(-3, -3)
    x,y= rect.bottomleft
    p1 = x-1, y-1
    p2 = x+1, y+1
    x,y = rect.topright
    p3= x+1, y+1
    p4 = x-1, y-1
    points = [p1,p2,p3,p4]
    pygame.draw.polygon(surface, Color.black, points)
    image = pygame_to_pil_img(surface)
    image.save('icons/line_32.png')

def rounded_rect(size):
    surface = pygame.Surface(size)
    surface.fill(Color.white)
    rect = surface.get_rect()
    rect.inflate_ip(-3, -3)
    draw_rounded_rect(surface, Color.white, rect, Color.black, 2, 5)
    image = pygame_to_pil_img(surface)
    image.save('icons/rounded_rect_32.png')

def bytes():
    for x in (255, 242, 228, 215, 201, 188, 174, 161, 147, 134, 120, 107, 93, 80, 66, 53, 39, 26, 13, 0):
        yield x

def colors():
    a = 255
    for r in bytes():
        for g in bytes():
            for b in bytes():
                yield r,g,b,a

def offsets():
    for dy in range(4):
        for dx in reversed(range(5)):
            yield dx * 20, dy * 20 
    

def color_icon():
    size = 100, 80
    surface = pygame.Surface(size)
    color = colors()
    for dx, dy in offsets():
        for x in range(20):
            for y in range(20):
                #print 'progress: %d, %d' % (x,y)
                surface.set_at((dx + x,dy + y), color.next())
    image = pygame_to_pil_img(surface)
    image.save('icons/color_chart_100.png')
    
def main():
#  img = hex((32,32))
#  img.save('hex.png')
#   rect((32,32))
#   ellipse((32,32))
#   rounded_rect((32,32))
#   line((32,32))
    color_icon()

if __name__ == '__main__':
  main()

