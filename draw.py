from pygame_events import EventListener, App
from pygame import Rect
import pygame
from pygame_ext import Color, draw_oval, draw_rounded_rect, draw_rect, draw_line
from pygame_ext import pygame_to_pil_img
from dandelion import ScratchSprite
from pygame_flood_fill import seed_fillA

def open_file():
    return getoutput(['python', 'gtk_dialogs.py', '-open'])

def save_file():
    return getoutput(['python', 'gtk_dialogs.py', '-save'])

def getoutput(cmd_lst):
    ''' How to emulate 'commands.getoutput()' with subprocess '''

    from subprocess import Popen, PIPE
    output = Popen(cmd_lst, stdout=PIPE).communicate()[0]
    return output.strip()
    
class Tool(EventListener):
    ''' Abstract tool '''

    cursor = None
    cursor_hotspot = 0,0
    
    def __init__(self):
        EventListener.__init__(self)
        # For debugging, put a red dot where the hotspot is
        pygame.draw.line(self.cursor, Color.red, self.cursor_hotspot, self.cursor_hotspot) 

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
        x,y = pos
        pattern = pygame.Surface((1,1))
        pattern.fill(canvas.pen_color)
        update_rect = seed_fillA(app.surface, x, y, pattern)
        app.add_dirty(update_rect)
     

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
             self.rect = surface.get_rect()
        self.init_subviews()
        self.draw()

    def get_rect(self):
         return self.rect

    def init_subviews(self):
        pass

    def draw(self):
        draw_rounded_rect(self.surface, Color.white, self.get_rect(), Color.black, 1, 5)
        for view in self.subviews:
            view.draw(self.surface)

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

FLIP_VERTICAL_ICON = Icon('shape_flip_vertical')
FLIP_HORIZONTAL_ICON = Icon('shape_flip_horizontal')
UNDO_ICON = Icon('arrow_undo')
REDO_ICON = Icon('arrow_redo')
ZOOM_IN_ICON = Icon('zoom_in')
ZOOM_OUT_ICON = Icon('zoom_out')

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
        self.add_subview(FLIP_HORIZONTAL_ICON, (x,y))
        x += 50
        self.add_subview(FLIP_VERTICAL_ICON, (x,y))
        x += 50
        self.add_subview(UNDO_ICON, (x,y))
        x += 50
        self.add_subview(REDO_ICON, (x,y))
        x += 50
        self.add_subview(ZOOM_IN_ICON, (x,y))
        x += 50
        self.add_subview(ZOOM_OUT_ICON, (x,y))

PLACEHOLDER_ICON = Icon('plugin')
RECT_TOOL_ICON = Icon('rect')
ELLIPSE_TOOL_ICON = Icon('ellipse')
ROUND_RECT_TOOL_ICON = Icon('rounded_rect')
LINE_TOOL_ICON = Icon('line')
TEXT_TOOL_ICON = Icon('text_allcaps')

class Tools(Panel):

    pen_tool = PenTool()
    fill_tool = FillTool()


    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        self.add_subview(Icon('pencil', PenTool(), default=True), (x,y))
        x += 50
        self.add_subview(PLACEHOLDER_ICON, (x,y))
        x -= 50; y += 50
        self.add_subview(Icon('paintcan', FillTool()), (x,y))
        x += 50
        self.add_subview(RECT_TOOL_ICON, (x,y))
        x -= 50; y += 50
        self.add_subview(ELLIPSE_TOOL_ICON, (x,y))
        x += 50
        self.add_subview(ROUND_RECT_TOOL_ICON, (x,y))
        x -= 50; y += 50
        self.add_subview(LINE_TOOL_ICON, (x,y))
        x += 50
        self.add_subview(TEXT_TOOL_ICON, (x,y))
        x = 0; y += 50
        self.add_subview(ColorPicker(), (x,y))

# Unused Icons, so sad:

COLOR_WHEEL_ICON = Icon('color_wheel')
COLOR_SWATCH_ICON = Icon('color_swatch')
ARROW_CURSOR_ICON = Icon('cursor')
PAINTBRUSH_ICON = Icon('paintbrush')
ZOOM_ICON = Icon('zoom')



class Canvas(Panel):
    
   
    def __init__(self, parent, rect, surface=None):
         global canvas
         canvas = self
         Panel.__init__(self, None, None, pygame.Surface(rect.size))
         self.pen_color = Color.black
         self.pen_width = 1.0
         self.dirty_rect = Rect(self.get_rect().center,(0,0))
         self.dirty_cursor = Rect(0,0,0,0)
         
    def import_file(self, filename):
        image = pygame.image.load(filename)
        im_rect = self.center_image(image)
        app.surface.blit(image, im_rect)
        app.add_dirty(im_rect)
        self.dirty_rect.union_ip(im_rect)

    def save_file(self, filename):
        pyimg = app.surface.subsurface(self.dirty_rect)
        pilimg = pygame_to_pil_img(pyimg)
        pilimg.save(filename)

    def center_image(self, image):
        im_rect = image.get_rect()
        ca_rect = self.get_rect()
        im_rect.center = ca_rect.center
        return im_rect
        
    def ondrag(self, pos, prev):
        app.current_tool.ondrag(pos, prev)
        
    def onclick(self, button, pos):
        app.current_tool.onclick(button, pos)
        
    def onmousemoved(self, pos, prev):
        app.surface.blit(self.surface, self.dirty_cursor, self.local_rect(self.dirty_cursor))
        app.current_tool.onmousemoved(pos, prev)
        self.dirty_cursor = app.current_tool.cursor_rect(pos)
        
    def onmouseout(self, pos):
        app.surface.blit(self.surface, self.dirty_cursor, self.local_rect(self.dirty_cursor))
        
    def onmouseover(self, pos):
        app.current_tool.onmousemoved(pos, pos)
        self.dirty_cursor = app.current_tool.cursor_rect(pos)
        
    # Drawing Utilities

    def points_to_local_rect(self, p1, p2):
        x1,y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
        x2,y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
        w,h = x2 - x1, y2 - y1
        dx, dy = self.rect.topleft
        return Rect((x1-dx,y1-dy),(w,h))
        
    def local_rect(self, rect):
        return rect.move(-self.rect.left, -self.rect.top)
        
    def app_rect(self, local):
        return local.move(self.rect.left, self.rect.top)
        
    def local_point(self, point):
        return point[0] - self.rect.left, point[1] - self.rect.top
        
    def echo_to_app(self, rect, local_rect):
        app.surface.blit(self.surface, rect, local_rect)
        app.add_dirty(rect)


    # Drawing routines to draw in both canvas and app surface

    def draw_image(self, source, dest, area=None):
        self.surface.blit(source, self.local_rect(dest), area)
        app.surface.blit(source, dest, area)
        app.add_dirty(dest)
            
    def draw_rect(self, rect):
        local = self.local_rect(rect)
        pygame.draw.rect(self.surface, self.pen_color, local, self.pen_width)
        self.echo_to_app(rect, local)
        
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
        local = self.points_to_local_rect(start_pos, end_pos)
        # draw line
        pygame.draw.line(self.surface, self.pen_color, local.topleft, local.bottomright, self.pen_width)
        # draw end caps
        r1 = pygame.draw.circle(self.surface, self.pen_color, local.topleft, self.pen_width / 2.0)
        r2 = pygame.draw.circle(self.surface, self.pen_color, local.topleft, self.pen_width / 2.0)
        # put the rects from each of these together for echo_to_app
        local = r1.union(r2)
        self.echo_to_app(self.app_rect(local), local)
        
    def draw_point(self, pos):
        local = self.local_point(pos)
        dirty = pygame.draw.circle(self.surface, self.pen_color, local, self.pen_width / 2.0)
        self.echo_to_app(self.app_rect(local), local)
        
        

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
        canvas = Canvas(self, canvas_rect)
        # init menu  panel
        menu_rect = Rect(0, 0, 100, 40).inflate(-2,-2)
        self.menu = Menu(self, menu_rect)
        # init tools panel
        tool_rect = Rect(0, 40, 100, bottom_offset).inflate(-2,-2)
        self.tools = Tools(self, tool_rect)
        control_rect = Rect(100, 0, right_width, 40).inflate(-2,-2)
        self.controls = Controls(self, control_rect)

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

