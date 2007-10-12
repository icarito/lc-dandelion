from pygame_events import EventListener, App
from pygame import Rect
import pygame
from pygame_ext import Color, draw_oval, draw_rounded_rect, draw_rect, draw_line
from pygame_ext import pygame_to_pil_img

def open_file():
    return getoutput(['python', 'gtk_dialogs.py', '-open'])

def save_file():
    return getoutput(['python', 'gtk_dialogs.py', '-save'])

def getoutput(cmd_lst):
    ''' How to emulate 'commands.getoutput()' with subprocess '''

    from subprocess import Popen, PIPE
    output = Popen(cmd_lst, stdout=PIPE).communicate()[0]
    return output.strip()

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

    def ondrag(self, pos):
        if self.picker_rect.collidepoint(*pos):
            x,y = pos
            dx,dy = self.picker_rect.topleft
            color = self.surface.get_at((x-dx, y-dy))
            self.update_color(color)
            pygame.display.update(self.swatch_rect)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class Icon(EventListener):

    def __init__(self, name):
        EventListener.__init__(self)
        self.surface = pygame.image.load('icons/%s_32.png' % name)
        self.name = name
	self.rect = Rect(0,0,32,32)

    def get_rect(self):
        return self.rect

    def set_pos(self, pos):
        self.rect.topleft = pos

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def onclick(self, button, pos):
        print '%s clicked' % self.name

REDUCE_ICON = Icon('arrow_in')
EXPAND_ICON = Icon('arrow_out')
ROTATE_CLOCKWISE_ICON = Icon('arrow_rotate_clockwise')
ROTATE_COUNTERCLOCKWISE_ICON = Icon('arrow_rotate_anticlockwise')

COLOR_WHEEL_ICON = Icon('color_wheel')
COLOR_SWATCH_ICON = Icon('color_swatch')
ARROW_CURSOR_ICON = Icon('cursor')
PAINTBRUSH_ICON = Icon('paintbrush')
PAINTCAN_ICON = Icon('paintcan')
PENCIL_ICON = Icon('pencil')
FLIP_VERTICAL_ICON = Icon('shape_flip_vertical')
FLIP_HORIZONTAL_ICON = Icon('shape_flip_horizontal')
ZOOM_ICON = Icon('zoom')
ZOOM_IN_ICON = Icon('zoom_in')
ZOOM_OUT_ICON = Icon('zoom_out')
IMPORT_ICON = Icon('folder')
SAVE_ICON = Icon('picture_save')
PLACEHOLDER_ICON = Icon('plugin')
RECT_TOOL_ICON = Icon('rect')
ROUND_RECT_TOOL_ICON = Icon('rounded_rect')
ELLIPSE_TOOL_ICON = Icon('ellipse')
LINE_TOOL_ICON = Icon('line')
TEXT_TOOL_ICON = Icon('text_allcaps')
UNDO_ICON = Icon('arrow_undo')
REDO_ICON = Icon('arrow_redo')


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

class Tools(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        def choose_pen(self, button, pos):
            canvas.set_handler('onclick', pen_onclick)
            canvas.set_handler('ondrag', pen_ondrag)
        PENCIL_ICON.set_handler('onclick', choose_pen)
        self.add_subview(PENCIL_ICON, (x,y))
        x += 50
        self.add_subview(PLACEHOLDER_ICON, (x,y))
        x -= 50; y += 50
        self.add_subview(PAINTCAN_ICON, (x,y))
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


def pen_ondrag(self, pos):
    print 'pen_drag'
    update_rect = draw_line(app.surface, app.pen_color, app.last_pos, pos, app.pen_width)
    app.last_pos = pos
    self.dirty_rect.union_ip(update_rect)
    pygame.display.update(update_rect)

def pen_onclick(self, button, pos):
    print 'pen_click'
    app.last_pos = pos
     

class Controls(Panel):

    def init_subviews(self):
        x,y = self.get_rect().topleft
        x += 4; y += 4
        self.add_subview(EXPAND_ICON, (x,y))
        x += 50
        self.add_subview(REDUCE_ICON, (x,y))
        x += 50
        self.add_subview(ROTATE_COUNTERCLOCKWISE_ICON, (x,y))
        x += 50
        self.add_subview(ROTATE_CLOCKWISE_ICON, (x,y))
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


class Canvas(Panel):
    
   
    def __init__(self, parent, rect, surface=None):
         Panel.__init__(self, parent, rect, surface)
         self.dirty_rect = Rect(self.get_rect().center,(0,0))
    def import_file(self, filename):
        image = pygame.image.load(filename)
        im_rect = self.center_image(image)
#        self.surface.blit(image, im_rect)
        app.surface.blit(image, im_rect)
        self.dirty_rect.union_ip(im_rect)
        pygame.display.update(im_rect)

    def save_file(self, filename):
        pyimg = app.surface.subsurface(self.dirty_rect)
        pilimg = pygame_to_pil_img(pyimg)
        pilimg.save(filename)

    def center_image(self, image):
        im_rect = image.get_rect()
        ca_rect = self.get_rect()
        im_rect.center = ca_rect.center
        return im_rect
        

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
        # init menu  panel
        menu_rect = Rect(0, 0, 100, 40).inflate(-2,-2)
        self.menu = Menu(self, menu_rect)
        # init tools panel
        tool_rect = Rect(0, 40, 100, bottom_offset).inflate(-2,-2)
        self.tools = Tools(self, tool_rect)
        control_rect = Rect(100, 0, right_width, 40).inflate(-2,-2)
        self.controls = Controls(self, control_rect)
        canvas_rect = Rect(100, 40, right_width, canvas_height).inflate(-2,-2)
        global canvas
        canvas = Canvas(self, canvas_rect)
        canvas.set_handler('onclick', pen_onclick)
        canvas.set_handler('ondrag', pen_ondrag)

    def draw(self):
        self.surface.fill(Color.white)
        for view in self.subviews:
            view.draw()
        pygame.display.update()
       
def main():
  global app
  #app = App(fullscreen=True)
  app = App(fullscreen=False)
  app.pen_width = 1
  app.pen_color = Color.black
  world = DrawWorld(app.new_surface())
  app.add_world(world)
  app.run()

if __name__ == '__main__':
    main()

