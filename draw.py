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
        
class LineTool(Tool):
    
    cursor = pygame.image.load('icons/pencil.png')
    
    def __init__(self):
        Tool.__init__(self)
        self.start_pos = None
        
    def ondragbegin(self, pos):
        self.start_pos = pos
        
    def ondrag(self, pos, prev):
        prev_rect = points_to_rect(self.start_pos, prev).inflate(canvas.pen_width, canvas.pen_width)
        app.surface.blit(canvas.surface, prev_rect, canvas.local_rect(prev_rect))
        new_rect = pygame.draw.line(app.surface, canvas.pen_color, prev, pos, canvas.pen_width)
        app.add_dirty(prev_rect, new_rect)
        
    def ondragend(self, pos):
        if not self.start_pos:
            return
        canvas.draw_line(self.start_pos, pos)
        self.start_pos = None
        
        

class Panel(EventListener):

    def __init__(self, parent, rect, surface=None):
        EventListener.__init__(self, self)
        self.listener = self
        self.parent = parent
        if parent:
             parent.add_subview(self)
             self.surface = parent.surface
             self.rect = rect
        else:
             self.surface = surface
             if rect:
                 self.rect = rect
             else:
                 self.rect = surface.get_rect()
        self.init_subviews()

    def get_rect(self):
         return self.rect

    def init_subviews(self):
        pass

    def draw(self):
        draw_rounded_rect(self.surface, Color.white, self.get_rect(), Color.black, 1, 5)
        for view in self.subviews:
            view.draw(self.surface)
        app.surface.blit(self.surface, self.rect)
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

class Icon(EventListener):

    def __init__(self, name, tool=None, default=False):
        EventListener.__init__(self)
        self.surface = pygame.image.load('icons/%s_32.png' % name)
        self.name = name
        self.rect = Rect(0,0,32,32)
        self.tool = tool
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

IMPORT_ICON = Icon('folder')
SAVE_ICON = Icon('picture_save')

class Menu(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        def import_image(self, button, pos):
            filename = open_file()
            if filename:
                canvas.import_file(filename) 
        IMPORT_ICON.set_handler('onclick', import_image)
        self.add_subview(IMPORT_ICON, (x,y))
        x += 50
        def save_image(self, button, pos):
            filename = save_file()
            if filename:
                canvas.save_file(filename)
        SAVE_ICON.set_handler('onclick', save_image)
        self.add_subview(SAVE_ICON, (x,y))


class Controls(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        self.add_subview(Icon('arrow_out'), (x,y)) # Expand
        x += 50
        self.add_subview(Icon('arrow_in'), (x,y)) # Reduce
        x += 50
        self.add_subview(Icon('arrow_rotate_clockwise'), (x,y)) # Rotate
        x += 50
        self.add_subview(Icon('arrow_rotate_anticlockwise'), (x,y)) # Rotate d'other way
        x += 50
        self.add_subview(Icon('shape_flip_horizontal'), (x,y))
        x += 50
        self.add_subview(Icon('shape_flip_vertical'), (x,y))
        x += 50
        self.add_subview(Icon('arrow_undo'), (x,y))
        x += 50
        self.add_subview(Icon('arrow_redo'), (x,y))
        x += 50
        self.add_subview(Icon('zoom_in'), (x,y))
        x += 50
        self.add_subview(Icon('zoom_out'), (x,y))


class Tools(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        self.add_subview(Icon('pencil', PenTool(), default=True), (x,y))
        x += 50
        self.add_subview(Icon('plugin'), (x,y))
        x -= 50; y += 50
        self.add_subview(Icon('paintcan', FillTool()), (x,y))
        x += 50
        self.add_subview(Icon('rect', RectTool()), (x,y))
        x -= 50; y += 50
        self.add_subview(Icon('ellipse'), (x,y))
        x += 50
        self.add_subview(Icon('rounded_rect'), (x,y))
        x -= 50; y += 50
        self.add_subview(Icon('line', LineTool()), (x,y))
        x += 50
        self.add_subview(Icon('text_allcaps'), (x,y))
        x = 0; y += 50
        self.add_subview(ColorPicker(), (x,y))
        

class Canvas(Panel):
    
   
    def __init__(self, parent, rect, surface=None):
         global canvas
         canvas = self
         Panel.__init__(self, None, rect, pygame.Surface(rect.size))
         self.surface.fill(Color.white )
         self.pen_color = Color.black
         self.pen_width = 4
         self.dirty_rect = Rect(self.get_rect().center,(0,0))
         self.dirty_cursor = Rect(0,0,0,0)
         
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

    def save_file(self, filename):
        pyimg = app.surface.subsurface(self.dirty_rect)
        pilimg = pygame_to_pil_img(pyimg)
        pilimg.save(filename)
        
    def draw(self):
        pass
        
    # Event handlers

    def ondrag(self, pos, prev):
        app.current_tool.ondrag(pos, prev)
        
    def ondragbegin(self, pos):
        app.current_tool.ondragbegin(pos)
        
    def ondragend(self, pos):
        app.current_tool.ondragend(pos)
        
    def onclick(self, button, pos):
        app.current_tool.onclick(button, pos)
        
    def onmousemove(self, pos, prev):
        app.surface.blit(self.surface, self.dirty_cursor, self.local_rect(self.dirty_cursor))
        app.current_tool.onmousemove(pos, prev)
        self.dirty_cursor = app.current_tool.cursor_rect(pos)
        
    def onmouseout(self, pos):
        print 'onmouseout'
        app.surface.blit(self.surface, self.dirty_cursor, self.local_rect(self.dirty_cursor))
        pygame.mouse.set_visible(True)
        
    def onmouseover(self, pos):
        print 'onmouseover'
        pygame.mouse.set_visible(False)
        app.current_tool.onmousemove(pos, pos)
        self.dirty_cursor = app.current_tool.cursor_rect(pos)
        
    # Drawing Utilities

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
        app.surface.blit(self.surface, rect, local_rect)
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
        self.echo_to_app(self.rect, self.local_rect(self.rect))
        
        

class DrawWorld(Panel):

    def __init__(self, surface):
        global app
        app = App.getApp()
        Panel.__init__(self, None, None, surface)

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
        self.add_subview(Canvas(self, canvas_rect))
        # init menu  panel
        menu_rect = Rect(0, 0, 100, 40).inflate(-2,-2)
        self.add_subview(Menu(self, menu_rect))
        # init tools panel
        tool_rect = Rect(0, 40, 100, bottom_offset).inflate(-2,-2)
        self.add_subview(Tools(self, tool_rect))
        control_rect = Rect(100, 0, right_width, 40).inflate(-2,-2)
        self.add_subview(Controls(self, control_rect))
        self.draw()

    def draw(self):
        self.surface.fill(Color.white)
        for view in self.subviews:
            view.draw()
                   
def main():
  #app = App(fullscreen=True)
  app = App(fullscreen=False, screensize=(800,480))
  world = DrawWorld(app.new_surface())
  app.add_world(world)
  app.run()

if __name__ == '__main__':
    main()

