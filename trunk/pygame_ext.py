'''
My custom extensions to Pygame
'''

import pygame
from pygame.time import get_ticks
from pygame.sprite import Sprite
from geometry import *
from itertools import cycle
from math import degrees, radians, pi, cos, sin
import Image # from PIL

# Useful Constants

X = 0
Y = 1
LEFT = 0
RIGHT = 1

# Variations of pygame calls

Rect = pygame.Rect

def update(rect=None):
  if rect:
    pygame.display.update(rect)
  else:
    pygame.display.update()

def draw_rect(surface, color, rect, border_color, border_width):
  pygame.draw.rect(surface, color, rect)
  if border_color:
    pygame.draw.rect(surface, border_color, rect, border_width)
    
def draw_rounded_rect(surface, color, rect, border_color, border_width, corner_radius):
  r = corner_radius
  o_l, o_r, o_t, o_b = rect.left, rect.right, rect.top, rect.bottom
  i_l, i_r, i_t, i_b = o_l + r, o_r - r, o_t + r, o_b - r
  top = [(i_l,o_t), (i_r, o_t)]
  top_left = _arc_points((i_l, i_t), r,  pi,  3.0 * pi / 2.0)
  left = [(o_l, i_b), (o_l, i_t)]
  bottom_left = _arc_points((i_l, i_b), r, pi / 2.0, pi)
  bottom = [(i_r, o_b), (i_l, o_b)]
  bottom_right = _arc_points((i_r, i_b), r, 0, pi / 2.0)
  right = [(o_r, i_t), (o_r, i_b)]
  top_right = _arc_points((i_r, i_t), r, 3.0 * pi / 2.0, 2.0 * pi)
  points = top + top_right + right + bottom_right + bottom + bottom_left + left + top_left
  if color:
      pygame.draw.polygon(surface, color, points)
  if border_color:
      pygame.draw.polygon(surface, border_color, points, border_width)
  return rect

def arc_through(surface, color, start_pt, end_pt, through_pt, width):
  a,b = perpendicular(start_pt, through_pt)
  c,d = perpendicular(end_pt, through_pt)
  print 'origin = intersection(%s,%s,%s,%s)' % (a,b,c,d)
  origin = intersection(a,b,c,d)
  r = mag(origin, start_pt)
  # sanity checks
  r2 = mag(origin, end_pt)
  if r != r2: print 'error: r=%f, r2=%f' % (r, r2)
  r3 = mag(origin, through_pt)
  if r != r3: print 'error: r=%f, r3=%f' % (r, r3)
  start_angle = get_angle(origin, start_pt)
  end_angle = get_angle(origin, end_pt)
  draw_arc(surface, color, origin, r, start_angle, end_angle, width)

def _arc_points(origin, radius, start, end):
  start = int(degrees(start))
  end = int(degrees(end))
  theta = radians
  t = translate
  p = polarToCart
  s_to_e = range(start, end)
  return [t(p(radius, theta(i)), origin) for i in s_to_e]
  

def draw_curve(scene, color, origin, radius, start, end, width):
  outer = _arc_points(origin, radius, start, end)
  inner = _arc_points(origin, radius - width, start, end)
  inner.reverse()
  try:
    pygame.draw.polygon(scene, color, outer+inner)
  except Exception, e:
    import sys
    print 'Error in draw_arc:', e
    print 'start: %s, end: %s' % (start, end)
    sys.exit()
    

def draw_arc(surface, color, origin, radius, start_angle, stop_angle,width):
  '''
  Replacement for pygame.draw.arc that allows arcs with the stop_angle less
  than the start_angle.
  '''
  rect = pygame.Rect(origin[0] - radius, origin[1] - radius, radius * 2, radius * 2)
  if start_angle > stop_angle:
    draw_arc(surface, color, origin, radius, start_angle, 2 * pi, width)
    draw_arc(surface, color, origin, radius, 0, stop_angle, width)
  else:
    pygame.draw.arc(surface, color, rect, start_angle, stop_angle, width)
    pygame.draw.arc(surface, color, rect.inflate(-1,-1), start_angle, stop_angle, width)

def draw_text(surface, color, origin, text, size=72):
  font = pygame.font.Font(None, size)
  msg = font.render(text, 1, color)
  rect = msg.get_rect()
  rect.left = origin[0]
  rect.top = origin[1]
  surface.blit(msg, rect)
  return rect

def draw_line(surface, color, origin, dest, width):
  # insert polygon-based drawing here
  print 'draw line start: %s' % (origin, )
  print 'drawline end: %s' % (dest, )
  return pygame.draw.line(surface, color, origin, dest, width)

def draw_oval( surf, color, A, B, radius, width=0):
  #'''
  #draw_oval function by John-Paul Gignac, from his Zoepaint applications
  #'''
	granularity = 10
	points = []

	dx = B[0] - A[0]
	dy = B[1] - A[1]
	lenAB = mag(A,B)
	if( lenAB == 0):
		ux = radius
		uy = 0.0
	else:
		ux = (A[1] - B[1]) * radius / lenAB
		uy = (B[0] - A[0]) * radius / lenAB
	vx = -uy
	vy = ux

	for i in range(granularity + 1):
		angle = pi * i / granularity
		c = cos(angle)
		s = sin(angle)
		points.append((A[0]+round(c*ux+s*vx), A[1]+round(c*uy+s*vy)))
	for i in range(granularity + 1):
		angle = pi * i / granularity
		c = cos(angle)
		s = sin(angle)
		points.append((B[0]-round(c*ux+s*vx), B[1]-round(c*uy+s*vy)))

	pygame.draw.polygon( surf, color, points, width)

	return pygame.Rect(min(A[0],B[0])-radius-1,min(A[1],B[1])-radius-1,
		abs(dx)+2*radius+2,abs(dy)+2*radius+2)


def pygame_to_pil_img(pg_img):
  imgstr = pygame.image.tostring(pg_img, 'RGBA')
  return Image.fromstring('RGB', pg_img.get_size(), imgstr)

def pil_to_pygame_img(pil_img):
  imgstr = pil_img.tostring()
  return pygame.image.fromstring(imgstr, pil_img.size, 'RGBA')


class Color:
  def __init__(self):
    self.__dict__ = pygame.colordict.THECOLORS
  def __str__(self):
    keys = self.__dict__.keys()
    keys.sort()
    return "Color: %s" % ', '.join(keys)

Color = Color()

S1 = (60,60)
S2 = (150,300)
S3 = (300,150)
T1 = pi
T2 = pi/2.0
STEPS = 30
ORIGIN = (300,300)
RADIUS = 150
transition_swoop = line_range(S1, S2, STEPS) + \
                   arc_range(ORIGIN, RADIUS, T1, T2, STEPS * 3) + \
                   line_range(S3, S1, STEPS) + \
                   [S1] * 10

swoop = cycle(transition_swoop)

class AnimatedSprite(Sprite):

  def __init__(self, filename, frames, variations, cycle=True):
    Sprite.__init__(self)
    self.surface = pygame.image.load(filename).convert()
    self.rect = pygame.Rect(self.surface.get_rect())
    self.rect.width = self.rect.width / variations
    self.rect.height = self.rect.height / frames
    self.variant = 0 # first variant
    self.surface.set_colorkey(Color.black, pygame.RLEACCEL)
    self.animation_clips = self._get_clips(frames=3,variations=2)
    self._next_clip = self._next_clip(frames, cycle) # turn generator into iterable
    self.next_frame()
    self.speed = [2,2]
    self.animation_delay = 100
    self.last_move = get_ticks()

  def _next_clip(self, frames, cycle):
    # generator for getting the next clipping rectangle for the sprite
    indices = range(frames)
    if not cycle: indices += indices[1::-1]
    while(1):
      for i in indices:
        yield self.animation_clips[i][self.variant]

  def _get_clips(self, frames, variations):
    def r(dx,dy):
      w,h = self.rect.width, self.rect.height
      return pygame.Rect(dx * w, dy * h, w, h)
    return [[r(dx,dy) for dx in range(variations)] for dy in range(frames)]

  def animate(self):
    time = get_ticks()
    if time > self.last_move:
      self.clip = self._next_clip.next()
      self.last_move = time
        
  def next_frame(self):
    # force next frame regardless of animation delay
    self.clip = self._next_clip.next()

  def set_variation(self, variant):
    self.variant = variant

  def move_to(self, pt):
    self.rect.left, self.rect.top = pt

  def move_by(self, vec):
    self.rect.left += vec[0]
    self.rect.top += vec[1]

  def draw(self, scene):
    #self.surface.set_clip(self.clip)
    scene.blit(self.surface, self.rect, self.clip)

class VectorSprite(Sprite):

  '''
  Behaves as a sprite, contains both a surface and a rect.
  '''

  def __init__(self, size=(16,16)):
      Sprite.__init__(self)
      self.surface  = pygame.Surface(size)
      self.rect = self.surface.get_rect()
      self.clear = (255, 1, 2)
      self.surface.set_colorkey(self.clear)

  def draw(self, scene):
      scene.blit(self.surface, self.rect)

  def erase(self, scene, color=None):
      if color == None: color = self.clear
      scene.fill(color, self.rect)

  def fromstring(self, data):
      '''
      Initialize surface from vector mini-language
      '''

  def tostring(self):
      '''
      Convert surface to vector mini-language
      '''

  def polygon(self, pointslist, stroke_color=None, fill_color=None, width=1):
    if fill_color:
      pygame.draw.polygon(self.surface, fill_color, pointslist, 0)
    if stroke_color:
      pygame.draw.polygon(self.surface, stroke_color, pointslist, width)

  def arc(self, rect, angle_start, angle_stop, fill_color=None, stroke_color=None, width=1):
    if fill_color:
      pygame.draw.arc(self.surface, fill_color, rect, angle_start, angle_stop, width)
    if stroke_color:
      pygame.draw.arc(self.surface, fill_color, rect, angle_start, angle_stop, 0)

  def render(self):
    self.surface.fill(self.clear)
    #self.surface.set_colorkey(clear, pygame.RLEACCEL)

  def move(self, dx, dy):
    self.rect.left += dx
    self.rect.top += dy

class SimpleWorld:

  def __init__(self, surface, background, scale, listener):
    self.surface = surface
    self.rect = surface.get_rect()
    self.size = self.display_area = self.width, self.height = self.rect.size
    self.size2 = self.width * scale[0], self.height * scale[1]
    surface.fill(Color.white)
    if background:
      self.background = pygame.image.load(background).convert()
      self.background = pygame.transform.scale(self.background, self.size2)
      self.surface.blit(self.background, self.rect)
    listener.set_owner(self)
    self.listener = listener
    pygame.display.update()

  def draw(self, sprite):
    self.surface.blit(self.background, self.rect)
    dirty = [sprite.rect]
    self.move_loop(sprite)
    self.scroll(sprite)
    dirty.append(pygame.Rect(sprite.rect))
    sprite.draw(self.surface)
    pygame.display.update()

  def scroll(self, sprite):
    safe_area = self.rect.inflate((0.8, 0.8))
    width, height = self.size2
    if self.rect.left > 0 and  sprite.rect.left < safe_area.left:
      diff = safe_area.left - sprite.rect.left
      safe_area.left -= diff
      self.rect.left -= diff
    elif self.rect.right < width and sprite.rect.right > safe_area.right:
      diff = sprite.rect.right - safe_area.right
      safe_area.right += diff
      self.rect.right += diff
    if self.rect.top > 0 and sprite.rect.top < safe_area.top:
      diff = safe_area.top - sprite.rect.top
      safe_area.top -= diff
      self.rect.top -= diff
    elif self.rect.bottom < height and sprite.rect.bottom < safe_area.bottom:
      diff = sprite.rect.bottom - safe_area.bottom
      safe_area.bottom += diff
      self.rect.bottom += diff

  def move_loop(self, sprite):
    pos = swoop.next()
    if pos == S1:
      sprite.set_variation(RIGHT)
    elif pos[0] > 300 and pos[1] < 300:
      sprite.set_variation(LEFT)
    sprite.move_to(pos)
    sprite.animate()
    
  def move_around(self, sprite):
    width, height = self.size2
    sprite.rect.move_ip(sprite.speed)
    if sprite.rect.left < 0:
      sprite.set_variation(RIGHT)
      sprite.rect.left = 0
      sprite.speed[X] *= -1
    elif sprite.rect.right > width:
      sprite.set_variation(LEFT)
      sprite.rect.right = width
      sprite.speed[X] *= -1
    if sprite.rect.top < 0:
      sprite.rect.top = 0
      sprite.speed[Y] *= -1
    if sprite.rect.bottom > height:
      sprite.rect.bottom = height
      sprite.speed[Y] *= -1
    sprite.animate()

