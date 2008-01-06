from pygame_events import EventListener, App
from pygame import Rect
import pygame
from pygame_ext import Color, draw_oval, draw_rounded_rect, draw_rect, draw_line
from pygame_ext import pygame_to_pil_img
from dandelion import ScratchSprite
from pygame_flood_fill import flood_fill
from math import ceil

def open_file():
    return getoutput(['python', 'gtk_dialogs.py', '-open'])

def save_file():
    return getoutput(['python', 'gtk_dialogs.py', '-save'])

def getoutput(cmd_lst):
    ''' How to emulate 'commands.getoutput()' with subprocess '''

    from subprocess import Popen, PIPE
    output = Popen(cmd_lst, stdout=PIPE).communicate()[0]
    return output.strip()
    
def points_to_rect(p1, p2):
    x1,y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
    x2,y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
    w,h = x2 - x1, y2 - y1
    return Rect((x1,y1),(w+1,h+1))
        
class Tool(EventListener):
    ''' Abstract tool '''

    cursor = None
    cursor_hotspot = 0,0
    
    def __init__(self):
        EventListener.__init__(self)
        # For debugging, put a red dot where the hotspot is
        pygame.draw.line(self.cursor, Color.red, self.cursor_hotspot, self.cursor_hotspot) 

    def ondragbegin(self, pos):
        pass
        
    def ondragend(self, pos):
        pass

    def ondrag(self, pos, prev):
        pass

    def onclick(self, button, pos):
        pass
        
    def cursor_rect(self, pos):
        x,y = pos
        dx, dy = self.cursor_hotspot
        return self.cursor.get_rect(center=(x-dx, y-dy))

    def onmousemove(self, pos, prev):
        rect = app.surface.blit(self.cursor, self.cursor_rect(pos))
        app.add_dirty(rect)
        return rect

class PenTool(Tool):
    
    cursor = pygame.image.load('icons/pencil.png')
    
    def __init__(self):
        Tool.__init__(self)
        self.last_pos = (0,0)

    def ondrag(self, pos, prev):
        canvas.draw_line(prev, pos)

    def onclick(self, button, pos):
        canvas.draw_point(pos)
        
class FillTool(Tool):
    
    cursor = pygame.image.load('icons/paintcan.png')

    def onclick(self, button, pos):
        canvas.draw_fill(pos)
        
class RectTool(Tool):
    
    cursor = pygame.image.load('icons/pencil.png')
    
    def __init__(self):
        Tool.__init__(self)
        self.start_pos = None
    
    def ondragbegin(self, pos):
        self.start_pos = pos
        
    def ondrag(self, pos, prev):
        prev_rect = points_to_rect(self.start_pos, prev).inflate(canvas.pen_width, canvas.pen_width)
        app.surface.blit(canvas.surface, prev_rect, canvas.local_rect(prev_rect))
        new_rect = points_to_rect(self.start_pos, pos)
        pygame.draw.rect(app.surface, canvas.pen_color, new_rect, canvas.pen_width)
        app.add_dirty(prev_rect, new_rect.inflate(canvas.pen_width, canvas.pen_width))
        
    def ondragend(self, pos):
        if not self.start_pos:
            return
        canvas.draw_rect(points_to_rect(self.start_pos, pos))
        self.start_pos = None

class EllipseTool(Tool):

    cursor = pygame.image.load('icons/pencil.png')

    def __init__(self):
        Tool.__init__(self)
        self.start_pos = None

    def ondragbegin(self, pos):
        self.start_pos = pos

    def ondrag(self, pos, prev):
        prev_rect = points_to_rect(self.start_pos, prev).inflate(canvas.pen_width, canvas.pen_width)
        app.surface.blit(canvas.surface, prev_rect, canvas.local_rect(prev_rect))
        new_rect = points_to_rect(self.start_pos, pos)
        try:
            pygame.draw.ellipse(app.surface, canvas.pen_color, new_rect, canvas.pen_width)
            app.add_dirty(prev_rect, new_rect.inflate(canvas.pen_width, canvas.pen_width))
        except ValueError, e:
            # cannot draw ellipse until mouse has moved furher than the radius of the ellipse
            pass

    def ondragend(self, pos):
        if not self.start_pos:
            return
        canvas.draw_ellipse(points_to_rect(self.start_pos, pos))
        self.start_pos = None

class RoundedRectTool(Tool):

    cursor = pygame.image.load('icons/pencil.png')

    def __init__(self):
        Tool.__init__(self)
        self.start_pos = None

    def ondragbegin(self, pos):
        self.start_pos = pos

    def ondrag(self, pos, prev):
        prev_rect = points_to_rect(self.start_pos, prev).inflate(canvas.pen_width, canvas.pen_width)
        app.surface.blit(canvas.surface, prev_rect, canvas.local_rect(prev_rect))
        new_rect = points_to_rect(self.start_pos, pos)
        draw_rounded_rect(app.surface, None, new_rect, canvas.pen_color, canvas.pen_width, canvas.corner_radius)
        app.add_dirty(prev_rect, new_rect.inflate(canvas.pen_width, canvas.pen_width))

    def ondragend(self, pos):
        if not self.start_pos:
            return
        canvas.draw_rounded_rect(points_to_rect(self.start_pos, pos))
        self.start_pos = None

        
class LineTool(Tool):
    
    cursor = pygame.image.load('icons/pencil.png')
    
    def __init__(self):
        Tool.__init__(self)
        self.start_pos = None
        self.prev_rect = None
        
    def ondragbegin(self, pos):
        self.start_pos = pos
        
    def ondrag(self, pos, prev):
        if self.prev_rect:
            app.surface.blit(canvas.surface, self.prev_rect, canvas.local_rect(self.prev_rect))
            app.add_dirty(self.prev_rect)
        self.prev_rect = pygame.draw.line(app.surface, canvas.pen_color, self.start_pos, pos, canvas.pen_width).inflate(canvas.pen_width,
             canvas.pen_width)
        app.add_dirty(self.prev_rect)
        
    def ondragend(self, pos):
        if not self.start_pos:
            return
        canvas.draw_line(self.start_pos, pos)
        self.start_pos = None
        self.prev_rect = None
        
class TestTool(Tool):
    
    cursor = pygame.image.load('icons/pencil.png')
    
    def __init__(self):
        Tool.__init__(self)
        self.start_pos = None
        
    def ondragbegin(self, pos):
        rect = pygame.draw.line(app.surface, Color.red, pos, pos)
        app.add_dirty(rect)
        self.start_pos = pos
        
    def ondrag(self, pos, prev):
        r1 = pygame.draw.line(app.surface, Color.white, prev, prev)
        r2 = pygame.draw.line(app.surface, Color.red, pos, pos)
        app.add_dirty(r1, r2)
        
    def ondragend(self, pos):
        if not self.start_pos:
            return
        canvas.pen_color = Color.green
        canvas.pen_width = 1
        canvas.draw_line(self.start_pos, self.start_pos)
        canvas.draw_line(pos, pos)
        self.start_pos = None
        

class Panel(EventListener):

    def __init__(self, parent, rect):
        EventListener.__init__(self, self)
        self.listener = self
        self.parent = parent
        if parent:
             parent.add_subview(self)
        self.rect = rect
        print 'Initializing', self.__class__.__name__, rect
        self.init_subviews()

    def get_rect(self):
         return self.rect
         
    def activate(self):
        pass
        
    def deactivate(self):
        pass

    def init_subviews(self):
        pass

    def draw(self, surface):
        print 'Drawing', self.__class__.__name__, self.rect
        draw_rounded_rect(surface, Color.white, self.get_rect(), Color.black, 1, 5)
        for view in self.subviews:
            view.draw(surface)
        app.add_dirty(self.rect)

class ColorPicker(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.surface = pygame.Surface((100,100))
        image = pygame.image.load('icons/color_chart_100.png')
        self.surface.blit(image, (0,0))
        self.rect = Rect(0,0,100,100)
        self.picker_rect = Rect(0,0,100,80)
        self.swatch_rect = Rect(0,80,100,20)
        self.update_color(Color.black)
        
    def get_rect(self):
        return self.rect

    def set_pos(self, pos):
        self.rect.topleft = pos
        self.picker_rect.topleft = pos
        self.swatch_rect.left = self.picker_rect.left
        self.swatch_rect.top = self.picker_rect.top + 80

    def update_color(self, color):
        pygame.draw.rect(self.surface, color, self.swatch_rect)
        pygame.draw.rect(app.surface, color, self.swatch_rect)
        canvas.pen_color = color

    def ondrag(self, pos, prev):
        if self.picker_rect.collidepoint(*pos):
            x,y = pos
            dx,dy = self.picker_rect.topleft
            color = self.surface.get_at((x-dx, y-dy))
            self.update_color(color)
            pygame.display.update(self.swatch_rect)
            
    def onclick(self, button, pos):
        self.ondrag(pos, pos)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class IconButton(EventListener):

    def __init__(self, name, tool=None, control=None, default=False):
        EventListener.__init__(self)
        self.surface = pygame.image.load('icons/%s_32.png' % name)
        self.name = name
        self.rect = Rect(0,0,32,32)
        self.tool = tool
        self.control = control
        if default:
            app.current_tool = tool

    def get_rect(self):
        return self.rect

    def set_pos(self, pos):
        self.rect.topleft = pos

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def onclick(self, button, pos):
        if self.tool:
            app.current_tool = self.tool
        elif self.control:
            self.control()

class Menu(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        def import_image(self, button, pos):
            filename = open_file()
            if filename:
                canvas.import_file(filename) 
        self.add_subview(IconButton('folder', control=import_image), (x,y))
        x += 50
        def save_image(self, button, pos):
            filename = save_file()
            if filename:
                canvas.save_file(filename)
        self.add_subview(IconButton('picture_save', control=save_image), (x,y))


class Controls(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        self.add_subview(IconButton('arrow_out', control=canvas.expand), (x,y)) # Expand
        x += 50
        self.add_subview(IconButton('arrow_in', control=canvas.contract), (x,y)) # Reduce
        x += 50
        self.add_subview(IconButton('arrow_rotate_clockwise', control=canvas.rotate_clockwise), (x,y)) # Rotate
        x += 50
        self.add_subview(IconButton('arrow_rotate_anticlockwise', control=canvas.rotate_anticlockwise), (x,y)) # Rotate d'other way
        x += 50
        self.add_subview(IconButton('shape_flip_horizontal', control=canvas.flip_horizontal), (x,y))
        x += 50
        self.add_subview(IconButton('shape_flip_vertical', control=canvas.flip_vertical), (x,y))
        x += 50
        self.add_subview(IconButton('arrow_undo'), (x,y))
        x += 50
        self.add_subview(IconButton('arrow_redo'), (x,y))
        x += 50
        self.add_subview(IconButton('zoom_in'), (x,y))
        x += 50
        self.add_subview(IconButton('zoom_out'), (x,y))


class Tools(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        self.add_subview(IconButton('pencil', tool=PenTool(), default=True), (x,y))
        x += 50
        self.add_subview(IconButton('plugin', tool=TestTool()), (x,y))
        x -= 50; y += 50
        self.add_subview(IconButton('paintcan', tool=FillTool()), (x,y))
        x += 50
        self.add_subview(IconButton('rect', tool=RectTool()), (x,y))
        x -= 50; y += 50
        self.add_subview(IconButton('ellipse', tool=EllipseTool()), (x,y))
        x += 50
        self.add_subview(IconButton('rounded_rect', tool=RoundedRectTool()), (x,y))
        x -= 50; y += 50
        self.add_subview(IconButton('line', tool=LineTool()), (x,y))
        x += 50
        self.add_subview(IconButton('text_allcaps'), (x,y))
        x = 0; y += 50
        self.add_subview(ColorPicker(), (x,y))
        

class Canvas(Panel):
    
   
    def __init__(self, parent, rect):
         global canvas
         canvas = self
         Panel.__init__(self, parent, rect)
         self.surface = pygame.Surface(rect.size)
         self.surface.fill(Color.white ) # paint the canvas off-screen view white
         self.pen_color = Color.black
         self.pen_width = 4
         self.corner_radius = 10
         self.dirty_rect = Rect(self.get_rect().center,(0,0))
         self.dirty_cursor = Rect(0,0,0,0)
         app.add_dirty(rect)
         
    def border(self):
        print 'drawing border:', self.rect
        old_color = self.pen_color
        old_width = self.pen_width
        self.pen_color = Color.red
        self.pen_width = 4
        self.draw_rect(self.rect)
        self.pen_color = old_color
        self.pen_width = old_width
         
    def import_file(self, filename):
        image = pygame.image.load(filename)
        im_rect = self.center_image(image)
        self.draw_image(image, im_rect)
        self.dirty_rect = im_rect

    def save_file(self, filename):
        pyimg = self.current_image()
        pilimg = pygame_to_pil_img(pyimg)
        pilimg.save(filename)
    
    def activate(self):
        print 'activating canvas:', self.rect, self.surface.get_rect()
        self.parent.surface.blit(self.surface, self.rect, self.surface.get_rect())
        app.add_dirty(self.rect)
        
    def draw(self, surface):
        if self.dirty_cursor.width or self.dirty_cursor.height:
            self.echo_to_app(self.app_rect(self.dirty_rect), self.dirty_rect)
        print 'Drawing Canvas', self.rect
        
    # Event handlers

    def ondrag(self, pos, prev):
        app.current_tool.ondrag(pos, prev)
        
    def ondragbegin(self, pos):
        app.current_tool.ondragbegin(pos)
        
    def ondragend(self, pos):
        app.current_tool.ondragend(pos)
        
    def onclick(self, button, pos):
        app.current_tool.onclick(button, pos)
        
    # Event handling for cursors
        
#    def onmousemove(self, pos, prev):
#        app.surface.blit(self.surface, self.dirty_cursor, self.local_rect(self.dirty_cursor))
#        app.current_tool.onmousemove(pos, prev)
#        self.dirty_cursor = app.current_tool.cursor_rect(pos)
        
#    def onmouseout(self, pos):
#        print 'onmouseout'
#        app.surface.blit(self.surface, self.dirty_cursor, self.local_rect(self.dirty_cursor))
#        pygame.mouse.set_visible(True)
        
#    def onmouseover(self, pos):
#        print 'onmouseover'
#        pygame.mouse.set_visible(False)
#        app.current_tool.onmousemove(pos, pos)
#        self.dirty_cursor = app.current_tool.cursor_rect(pos)

    # Controls
    EXPAND_RATIO = 1.1
    CONTRACT_RATIO = 1.0 / EXPAND_RATIO
    ROTATION_UNIT = 15.0
    
    def transform(self, ratio=None, rotation=None, flip_h=False, flip_v=False):
        # extract a surface based on dirty_rect
        old_center = self.dirty_rect.center
        image = self.current_image()
        if ratio:
            # scale it
            result = pygame.transform.scale(image, (ratio, ratio))
        elif rotation:
            result = pygame.transform.rotate(image, rotation)
        elif flip_h:
            result = pygame.transform.flip(image, True, False)
        elif flip_v:
            result = pygame.transform.flip(image, False, True)
        else:
            return
        rect = result.get_rect(center=old_center)
        if self.rect.contains(rect):
            self.dirty_rect = rect
        else:
            self.dirty_rect = self.rect
        self.surface.blit(result, self.dirty_rect, result.get_rect(size = self.dirty_rect.size))
        self.echo_to_app(rect, self.local_rect(rect))
        return rect
        
    def expand(self):
        return self.transform(ratio=EXPAND_RATIO)
        
    def contract(self):
        return self.transform(ratio=CONTRACT_RATIO)
        
    def rotate_clockwise(self):
        return self.transform(rotation= -ROTATION_UNIT)
        
    def rotate_anticlockwise(self):
        return self.transform(rotation=ROTATION_UNIT)
        
    def flip_horizontal(self):
        return self.transform(flip_h=True)
        
    def flip_vertical(self):
        return self.transform(flip_v=True)
        
        
    # Drawing Utilities
    
    def current_image(self):
        return pygame.transform.chop(self.surface, self.dirty_rect)

    def center_image(self, image):
        im_rect = image.get_rect()
        ca_rect = self.get_rect()
        im_rect.center = ca_rect.center
        return im_rect
    
        
    def local_rect(self, rect):
        return rect.move(-self.rect.left, -self.rect.top)
        
    def app_rect(self, local):
        return local.move(self.rect.left, self.rect.top)
        
    def local_point(self, point):
        return point[0] - self.rect.left, point[1] - self.rect.top
        
    def echo_to_app(self, rect, local_rect):
        # print 'echo_to_app(%s, %s)' % (rect, local_rect)
        rect.inflate_ip(self.pen_width, self.pen_width)
        local_rect.inflate_ip(self.pen_width, self.pen_width)
        self.dirty_rect.union_ip(local_rect)
        self.parent.surface.blit(self.surface, rect, local_rect)
        app.add_dirty(rect)


    # Drawing routines to draw in both canvas and app surface

    def draw_image(self, dest, area=None):
        self.surface.blit(source, dest, area)
        self.echo_to_app(self.app_rect(dest), dest)
            
    def draw_rect(self, rect):
        local = self.local_rect(rect)
        pygame.draw.rect(self.surface, self.pen_color, local, self.pen_width)
        self.echo_to_app(rect, local)
        
    def draw_rect_pts(self, start, end):
        rect = points_to_rect(start, end)
        self.draw_rect(rect)
        
    def draw_filled_rect(self, rect):
        local = self.local_rect(rect)
        pygame.draw.rect(self.surface, self.pen_color, local, 0)
        self.echo_to_app(rect, local)
        
    def draw_rounded_rect(self, rect):
        local = self.local_rect(rect)
        draw_rounded_rect(self.surface, None, local, self.pen_color, self.pen_width, self.corner_radius)
        self.echo_to_app(rect, local)
        
    def draw_filled_rounded_rect(self, rect):
        local = self.local_rect(rect)
        draw_rounded_rect(self.surface, self.pen_color, local, None, self.pen_width, self.corner_radius)
        self.echo_to_app(rect, local)
        
    def draw_ellipse(self, rect):
        local = self.local_rect(rect)
        pygame.draw.ellipse(self.surface, self.pen_color, local, self.pen_width)
        self.echo_to_app(rect, local)
        
    def draw_filled_ellipse(self, rect):
        local = self.local_rect(rect)
        pygame.draw.ellipse(self.surface, self.pen_color, local, 0)
        self.echo_to_app(rect, local)
        
    def draw_line(self, start_pos, end_pos):
        # print 'draw_line(%s, %s)' % (start_pos, end_pos)
        start = self.local_point(start_pos)
        end = self.local_point(end_pos)
        # draw line
        r1 = pygame.draw.line(self.surface, self.pen_color, start, end, self.pen_width)
        # draw end caps
        #r2 = pygame.draw.circle(self.surface, self.pen_color, end, int(ceil(self.pen_width / 2.0)))
        # put the rects from each of these together for echo_to_app
        #local = r1.union(r2)
        self.echo_to_app(self.app_rect(r1), r1)
        
    def draw_point(self, pos):
        local = self.local_point(pos)
        dirty = pygame.draw.circle(self.surface, self.pen_color, local, int(ceil(self.pen_width / 2.0)))
        self.echo_to_app(self.app_rect(dirty), dirty)
        
    def draw_fill(self, pos):
        dirty = flood_fill(self.surface, self.local_point(pos), self.pen_color)
    #    self.echo_to_app(self.app_rect(dirty), dirty)
        self.parent.surface.blit(self.surface, self.rect, self.surface.get_rect())
        app.add_dirty(self.rect)
        
        

class DrawWorld(Panel):

    def __init__(self, surface):
        global app
        app = App.getApp()
        self.surface = surface
        Panel.__init__(self, None, surface.get_rect())
        
    def activate(self):
        for view in self.subviews:
            view.activate()

    def init_subviews(self):
        # get some values for rectangles
        rect = self.get_rect()
        top_offset = 40
        bottom_offset = rect.height - 40
        left_offset = 100
        right_width = rect.width - left_offset
        canvas_height = rect.height - 40
        # init canvas panel
        canvas_rect = Rect(100, 40, right_width, canvas_height).inflate(-2,-2)
        self.canvas = Canvas(self, canvas_rect)
        # init menu  panel
        menu_rect = Rect(0, 0, 100, 40).inflate(-2,-2)
        self.menu = Menu(self, menu_rect)
        # init tools panel
        tool_rect = Rect(0, 40, 100, bottom_offset).inflate(-2,-2)
        self.tools = Tools(self, tool_rect)
        # init controls panel
        control_rect = Rect(100, 0, right_width, 40).inflate(-2,-2)
        self.controls = Controls(self, control_rect)

    def draw(self):
        print 'Draw DrawWorld', self.rect
        self.surface.fill(Color.white)
        for view in self.subviews:
            view.draw(self.surface)
                   
def main():
  #app = App(fullscreen=True)
  app = App(fullscreen=False, screensize=(800,480))
  world = DrawWorld(app.surface)
  app.add_world(world)
  app.run()

if __name__ == '__main__':
    main()

