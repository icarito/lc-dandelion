'''
  Event handling

  App: initialize pygame and setup screen, pump events, select world, forward
  events to current world.

  EventDispatcher: synthesize high-level events and distribute them to
  listeners


  EventListener: Interface for registered event handlers
'''

import pygame, sys
from geometry import translate
import new

def get_screen_size():
  size = (800,600)
  if sys.platform == 'win32':
    import win32gui
    size = win32gui.GetWindowRect(win32gui.GetDesktopWindow())[2:]
    del win32gui
  elif sys.platform == 'darwin':
    import objc
    import AppKit
    size = AppKit.NSScreen.mainScreen().visibleFrame()[1]
    #size = int(size.width), int(size.height)
    del AppKit
    del objc
   # how do I calculate size on Linux and elsewhere?
  elif sys.platform == 'linux2':
      # Maemo support only for now
      size = 800,480
  return size


class App:
    
  app = None
    
  @classmethod
  def getApp(cls, *args, **kws):
      if not cls.app:
          cls.app = App(*args, **kws)
      return cls.app

  def __init__(self, fullscreen=False, framerate=15, bitdepth=16,  screensize=(800,480)):
    self.__class__.app = self
    pygame.init()
    self._dirty_rects = []
    self.framerate = framerate
    if fullscreen:
      self.size = self.width, self.height = pygame.display.list_modes(bitdepth, pygame.FULLSCREEN)[0]
      self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
    else:
      self.size = get_screen_size()
      self.screen = pygame.display.set_mode(self.size)
    self.surface = self.screen
    self.rect = self.surface.get_rect()
    self.display_area = self.rect.size
    self.event_dispatcher = EventDispatcher()
    self.worlds = []
    self.current_world = None
    self.current_idx = -1
    self.old_world_surface = None

  def new_surface(self):
    return pygame.Surface(self.size, pygame.SWSURFACE)

  def add_dirty(self, *rects):
      self._dirty_rects += rects
    
  def update(self):
      if self._dirty_rects:
          self._dirty_rects, rects = [], self._dirty_rects
          pygame.display.update(rects)

  def _activate_world(self, world):
    if self.current_world:
      self._deactivate_world(self.current_world)
    self.current_world = world
    self.event_dispatcher.set_owner(world)
    self.event_dispatcher.set_listener(world.listener)
    self.surface.blit(world.surface, (0,0))
    self.old_world_surface = world.surface
    world.surface = self.surface
    pygame.display.update()

  def _deactivate_world(self, world):
    if self.old_world_surface:
      world.surface = self.old_world_surface
      world.surface.blit(self.surface, (0,0))
    
  def add_world(self, world):
    self.worlds.append(world)
    if not self.current_world:
      self._activate_world(world)
      self.current_idx = 0

  def next_world(self):
    if self.current_idx < len(self.worlds) - 1:
      self.current_idx += 1
      world = self.worlds[self.current_idx]
      self._activate_world(world)

  def prev_world(self):
    if self.current_idx > 0:
      self.current_idx -= 1
      world = self.worlds[self.current_idx]
      self._activate_world(world)

  def set_listener(self, listener):
    self.event_dispatcher.set_listener(listener)

  def set_pulse(self, rate):
    pygame.time.set_timer(PULSE_ID, rate)

  def run(self):
    self.event_dispatcher.start(self.framerate)
    while True:
      self.event_dispatcher.pump()

DOUBLE_CLICK_RATE = int((8.0/15.0) * 1000) # 8/15 second
AUTO_KEY_THRESHOLD = int((2.0/5.0) * 1000) # 2/5 second
AUTO_KEY_RATE = int((1.0/10.0) * 1000)     # 1/10 second

META = pygame.KMOD_META
if sys.platform in ('win32', 'linux2'):
  META = pygame.KMOD_CTRL

PULSE_ID = pygame.USEREVENT + 1
#PULSE_RATE = 1000/30                       # 1/30 second
# PULSE_RATE = 1000/15                       # 1/15 second
PULSE_RATE = 1000/20                       # 1/20 second

class EventDispatcher:
  '''
    Double-click rate defaults to 8/15 seconds
    Auto-key threshold defaults to 2/5 seconds
    Auto-key rate defaults to 1/10 seconds
  '''

  def __init__(self):
    self.listener = EventListener(None)
    self.owner = None
    self.clock = pygame.time.Clock()
    self._last_pos = (0,0)
    self._last_mouseup = 0
    self._last_mousedown = 0
    self._last_keydown = 0
    self._last_keyup = 0
    self._is_mousedown = False
    self._is_keydown = False
    self._is_mousein = True
    self._is_dragging = False
    self._keysdown = (0,0)
    self._is_keyrepeating = False
    self._last_keyrepeat = 0
    self._last_tick = 0
    self._last_mouse_pos = (0,0)
    self.clock.tick()

  def start(self, framerate):
    pygame.time.set_timer(PULSE_ID, 1000/framerate)
    
  def set_listener(self, listener):
    self.listener = listener

  def set_owner(self, owner):
    self.owner = owner

  def pump(self):
    self._last_tick += self.clock.tick()
    time = self._last_tick
    event_queue = pygame.event.get()
    for event in event_queue:
      if event.type == pygame.QUIT: 
        self._exit()
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_q and event.mod & META:
          self._exit()
        elif event.key == pygame.K_n and event.mod & pygame.KMOD_META:
          self._new_game()
        elif event.key == pygame.K_F6:
          pygame.display.toggle_fullscreen()
        else: 
          self._keyup(event, time)
      elif event.type == pygame.KEYDOWN:
        self._keydown(event, time)
      elif event.type == pygame.ACTIVEEVENT:
        self._active(event, time)
      elif event.type == pygame.MOUSEMOTION:
        self._mousemove(event, time)
      elif event.type == pygame.MOUSEBUTTONDOWN:
        self._mousedown(event, time)
      elif event.type == pygame.MOUSEBUTTONUP:
        self._mouseup(event, time)
      elif event.type == PULSE_ID:
        app.update()
        self.listener.onpulse()
      else:
        pass # not handling joystick, video, or user events
    self._tick(time)

  def _mouseup(self, event, time):
    '''
    Decide if this is a drag-end, click, or double-click
    if pos is not the same as self._last_pos: drag, not click
    '''
    self._lastpos = event.pos
    self._is_mousedown = False
    self._last_mouseup = time
    if self._is_dragging:
      self._is_dragging = False
      self.listener.ondragend(event.pos)

  def _mousedown(self, event, time):
    '''
    Decide if this is a the beginning of a click, double-click, or drag
    '''
    self.listener.onclick(event.button, event.pos)
    if self._last_pos == event.pos:
      if time < self._last_mouseup + DOUBLE_CLICK_RATE:
        self.listener.ondblclick(event.button, event.pos)
    self._lastpos = event.pos
    self._is_mousedown = True
    self._last_mousedown = time

  def _mousemove(self, event, time):
    '''
    Is this part of a drag, or mouse-in/mouse-out/mouse-move
    '''
    pos = event.pos
    prev = translate(pos, (-event.rel[0], -event.rel[1]))
    self.listener.onmousemove(pos, prev)
    if self._is_mousein:
      if not self.owner.get_rect().collidepoint(*pos):
        self._is_mousein = False
        self.listener.onmouseout(pos)
    else:
      if self.owner.rect.collidepoint(*pos):
        self._is_mousein = True
        print 'mouse_in'
        self.listener.onmousein(pos)
      else:
        print 'point %s not in rect %s' % (pos, self.ownwer.rect)
    if self._is_mousedown:
      if not self._is_dragging:
        self._is_dragging = True
        self.listener.ondragbegin(pos)
      self.listener.ondrag(pos)

  def _keydown(self, event, time):
    self.listener.onkeypress(event.key, event.mod, False)
    self._last_keydown = time
    self._last_keysdown = (event.key, event.mod)
    self._is_keydown = True

  def _keyup(self, event, time):
    self._last_keyup = time
    self._is_keydown = False
    self._is_keyrepeating = False

  def _exit(self):
    self.listener.onexit()
    sys.exit()

  def _active(self, event, time):
    #print 'active:', event
    pass

  def _new_game(self):
    self.listener.onnewgame()

  def _tick(self, time):
    if self._is_keydown:
      if not self._is_keyrepeating:
        if time > self._last_keydown + AUTO_KEY_THRESHOLD:
          self._is_keyrepeating = True
      if self._is_keyrepeating:
        if time > self._last_keyrepeat + AUTO_KEY_RATE:
          self._last_keyrepeat = time
          self.listener.onkeypress(self._last_keysdown[0], self._last_keysdown[1], True)

class EventListener(object):

  def __init__(self, owner=None):
    self.owner = owner
    self.subviews = []

  def set_owner(self, owner):
    self.owner = owner

  def set_handler(self, eventname, fn):
      setattr(self, eventname, new.instancemethod(fn, self, self.__class__))

  def add_subview(self, view, pos=None):
    if pos:
        view.set_pos(pos)
    self.subviews.append(view)

  def onactivate(self, event):
    for view in self.subviews:
        view.onactivate(event)

  def ondeactivate(self, event):
    for view in self.subviews:
        view.ondeactivate(event)

  def onclick(self, button, pos):
    #print self.__class__,'onclick'
    for view in self.subviews:
        #from draw import Icon
        if view.get_rect().collidepoint(*pos):
            view.onclick(button, pos)
        #elif isinstance(view, Icon):
        #    print '%s not in %s' % (pos, view.get_rect())

  def ondblclick(self, button, pos):
    for view in self.subviews:
        if view.get_rect().collidepoint(*pos):
            view.ondblclick(button, pos)

  def ondragbegin(self, pos):
    for view in self.subviews:
        if view.get_rect().collidepoint(*pos):
            view.ondragbegin(pos)

  def ondragend(self, pos):
    for view in self.subviews:
        if view.get_rect().collidepoint(*pos):
            view.ondragend(pos)

  def ondrag(self, pos):
    for view in self.subviews:
        if view.get_rect().collidepoint(*pos):
            view.ondrag(pos)

  def onkeypress(self, key, mod, isrepeat):
    for view in self.subviews:
        view.onkeypress(key, mod, isrepeat)

  def onmouseover(self, pos):
    for view in self.subviews:
        if view.get_rect().collidepoint(*pos):
            view.onmouseover(pos)

  def onmouseout(self, pos):
    # mouseout for subviews handled in onmousemove
    pass

  def onmousemove(self, pos, prev):
    for view in self.subviews:
        if view.get_rect().collidepoint(*pos):
            view.onmousemove(pos, prev)
        elif view.get_rect().collidepoint(*prev):
            view.onmouseout(pos)

  def onpulse(self):
    for view in self.subviews:
        view.onpulse()

  def onexit(self):
    for view in self.subviews:
        view.onexit()

  def onnewgame(self):
    for view in self.subviews:
        view.onnewgame()

class ForwardingEventListener(EventListener):

  def __init__(self, owner):
    EventListener.__init__(self, owner)
    self.sub_listener = None

  def setSubListener(self, listener):
    self.sub_listener = listener

  def onactivate(self, event):
    if self.sub_listener: self.sub_listener.onactivate(event)

  def ondeactivate(self, event):
    if self.sub_listener: self.sub_listener.ondeactivate(event)

  def onclick(self, button, pos):
    if self.sub_listener: self.sub_listener.onclick(button, pos)

  def ondblclick(self, button, pos):
    if self.sub_listener: self.sub_listener.ondblclcik(button, pos)

  def ondragbegin(self, pos):
    if self.sub_listener: self.sub_listener.ondragbegin(pos)

  def ondrag(self, pos):
    if self.sub_listener: self.sub_listener.ondrag(pos)

  def ondragend(self, pos):
    if self.sub_listener: self.sub_listener.ondragend(pos)

  def onkeypress(self, key, mod, isrepeat):
    if self.sub_listener: self.sub_listener.onkeypress(key, mod, isrepeat)

  def onmouseover(self, pos):
    if self.sub_listener: self.sub_listener.onmouseover(pos)

  def onmouseout(self, pos):
    if self.sub_listener: self.sub_listener.onmouseout(pos)

  def onpulse(self):
    if self.sub_listener: self.sub_listener.onpulse()
  
  def onexit(self):
    if self.sub_listener: self.sub_listener.onexit()
