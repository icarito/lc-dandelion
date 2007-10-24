'''
Scratch for Python

Will eventually incorporate several "worlds"

1. Drawing world
2. Layout world
3. Coding world
4. Playing world
'''

import pygame
from geometry import *
from pygame_events import App, ForwardingEventListener, EventDispatcher, META
from draw import DrawWorld
from dandelion import ScratchWorld

class DemoDispatcher(EventDispatcher):
  def __init__(self, app):
    EventDispatcher.__init__(self)
    self.app = app

  def _keydown(self, event, time):
    '''
    We want to switch games on Cmd-RightArrow, Cmd-LeftArrow
    '''
    if event.mod & META:
      if event.key == pygame.K_RIGHT:
        self.app.next_world()
      elif event.key == pygame.K_LEFT:
        self.app.prev_world()
    EventDispatcher._keydown(self, event, time)

def main(fullscreen=False):
  app = App(fullscreen=False, screensize=(800,480))
  app.event_dispatcher = DemoDispatcher(app)
  app.add_world(ScratchWorld(app.new_surface()))
  app.add_world(DrawWorld(app.new_surface()))
  app.run()

if __name__ == '__main__':
  import sys
  fullscreen = False
  if 'fullscreen' in sys.argv:  fullscreen = True
  main(fullscreen)

