'''
Sprites and background tiles from Planet Cute
'''

from pygame.sprite import Sprite
import pygame
from pygame_events import App, EventListener, META
import os


BLOCK_WIDTH = 50
BLOCK_HEIGHT = 60

TRUE_WIDTH = 101
TRUE_HEIGHT = 171

# N800 Screen Size is 800 x 480
# XOXO Screen Size is 1024 x 768 (I think)

SCREENWIDTH = 700
SCREENHEIGHT = 400

SCREENSIZE = SCREENWIDTH, SCREENHEIGHT

CENTRE_X = SCREENWIDTH / 2
CENTRE_Y = SCREENHEIGHT / 2

blocks = dict(blue='Blue Block', brown='Brown Block', dirt='Dirt Block', fire='Fire Block', grass='Grass Block', ice='Ice Block',  plain='Plain Block', sand='Sand Block', stone_tall='Stone Block Tall', stone='Stone Block', wall_tall='Wall Block Tall', wall='Wall Block', water='Water Block', wood='Wood Block')
characters = ['Boy', 'Cat Girl', 'Horn Girl', 'Pink Girl', 'Princess Girl', 'Enemy Bug']
things = ['Chest Closed', 'Chest Lid', 'Chest Open', 'Gem Blue', 'Gem Green', 'Gem Orange', 'Heart', 'Key', 'Rock', 'Selector', 'Speech Bubble', 'Star', 'Tree Short', 'Tree Tall', 'Tree Ugly']
buildings = ['Door Tall Closed', 'Door Tall Open', 'Ramp East', 'Ramp North', 'Ramp South', 'Ramp West', 'Roof East', 'Roof North East', 'Roof North West', 'Roof North', 'Roof South East', 'Roof South West', 'Roof South', 'Roof West', 'Window Tall']
shadows = ['Shadow East', 'Shadow North East', 'Shadow North West', 'Shadow North', 'Shadow South East', 'Shadow South West', 'Shadow South', 'Shadow West', 'Shadow Side West']

class ScratchCostume(object):

    _image_bank = {}
    _nullInstance = None
    
    @classmethod
    def nullCostume(cls):
        if not cls._nullInstance:
            cls.nullInstance = ScratchCostume(None)
        return cls.nullInstance

    def __init__(self, path):
        if path is None:
            self.name = 'Null Costume'
            self.image = pygame.Surface((0,0))
        else:
            self.name, ext = os.path.splitext(os.path.basename(path))
            if self.name not in self._image_bank:
                self._image_bank[self.name] = pygame.image.load(path)
            self.image = self._image_bank[self.name]
        self.rotation_center = self.image.get_rect().center
        
    def get_size(self):
        return self.image.get_size()
        
    def rotated_and_scaled(self, rotation, scaling):
        return pygame.transform.rotozoom(self.image, rotation, scaling)
    

class ScratchSprite(Sprite, EventListener):    
    _count = 0
    
    def __init__(self, *img_names):
        ScratchSprite._count += 1
#        print 'Initializing sprite %d' % ScratchSprite._count
        Sprite.__init__(self)
        self.costumes = []
        self.currentCostume = ScratchCostume.nullCostume()
        self.loadCostumes(*img_names)
        self.x, self.y = BLOCK_WIDTH / 2, BLOCK_HEIGHT / 2
        self.rotation = 0
        self.scaling = 0
        self._updateImage()

    def get_rect(self):
        return self.image.get_rect(center=(self.x, self.y))
        
    def move_to(self, x, y):
        self.x, self.y = x,y
        
    def move_by(self, dx, dy):
        self.x +=  dx
        self.y += dy
        
    def _updateImage(self):
        if self.rotation or self.scaling:
            self.image = self.currentCostume.rotated_and_scaled(self.rotation, self.scaling)
        else:
            self.image = self.currentCostume.image
        
    def scale_by(self, factor):
        self.scaling *= factor
        self._updateImage()
        
    def scale_to(self, factor):
        self.scaling = factor
        self._updateImage()
        
    def rotate_by(self, angle):
        self.rotation += angle
        self._updateImage()
        
    def rotate_to(self, angle):
        self.rotation = angle
        self._updateImage()

    def loadCostumes(self, *img_names):
        import os
        for name in img_names:
            if os.path.exists(name):
                # if name is an image file, create a costume
                if os.path.isfile(name):
                    base, ext = os.path.splitext(name)
                    if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                        self.costumes.append(ScratchCostume(name))
                # if name is a directory, process recursively
                elif os.path.isdir(name):
                    self.loadCostumes(*os.listdir(name))
                # otherwise, skip it
        if self.costumes:
            self.currentCostume = self.costumes[0]

    def draw(self, surface):
        surface.blit(self.image, self.get_rect())
        
        
MOVE_UNIT = 10
ROTATE_UNIT = 10
KEY_MOVES = {pygame.K_UP: (0,-MOVE_UNIT), pygame.K_DOWN:(0,MOVE_UNIT), pygame.K_LEFT:(-MOVE_UNIT, 0), pygame.K_RIGHT:(MOVE_UNIT, 0)}
        
class ScratchListener(EventListener):

    def set_owner(self, world):
        self.world = world
        
    def onkeypress(self, key, mod, ignore):
        if key == pygame.K_u and (mod == pygame.K_RMETA or mod == pygame.K_LMETA):
            sys.exit()
        if mod & META:
            pass
        if mod & pygame.KMOD_ALT:
            if key == pygame.K_LEFT:
                self.world.rotate_by(ROTATE_UNIT)
            if key == pygame.K_RIGHT:
                self.world.rotate_by(-ROTATE_UNIT)
        else:
            if key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.world.move(*KEY_MOVES[key])

    def onpulse(self):
        self.world.tick()

    def onactivate(self, event):
        print 'onactivate:', event

    def ondeactivate(self, event):
        print 'ondeactivate:', event

    def onclick(self, button, pos):
        print 'onclick:', pos

    def ondblclick(self, button, pos):
        print 'ondblclick:', pos

    def ondragbegin(self, pos):
        print 'ondragbegin:', pos

    def ondragend(self, pos):
        print 'ondragend:', pos

    def ondrag(self, pos):
        print 'ondrag:', pos

    def onexit(self):
        print 'onexit'

    def onnewgame(self):
        print 'onnewgame'
                
class ScratchWorld(object):

    def __init__(self, surface):
        global app
        app = App.getApp()
        self.surface = surface
        self.size = self.display_area = self.width, self.height = self.get_rect().size
        self.background = self.getBackground('cute_layout.xml')
        self.listener = ScratchListener()
        self.listener.set_owner(self)
        self.sprite = ScratchSprite('cute/Character Cat Girl.png')
        self.sprite.move_to(BLOCK_WIDTH, BLOCK_HEIGHT)
        self.draw()
        self.dirty_rects = []
        pygame.display.update()

    def tick(self):
        pass
        
    def get_rect(self):
        return self.surface.get_rect()
        
    def _mark_dirty(self):
        rect = self.sprite.get_rect()
        self.surface.blit(self.background, rect, rect)
        self.dirty_rects = [rect]
        
    def move(self, dx, dy):
        self._mark_dirty()
        self.sprite.move_by(dx,dy)
        self.sprite.draw(self.surface)
        self.dirty_rects.append(self.sprite.get_rect())
        pygame.display.update(self.dirty_rects)
        
    def rotate_by(self, angle):
        self._mark_dirty()
        self.sprite.rotate_by(angle)
        self.sprite.draw(self.surface)
        self.dirty_rects.append(self.sprite.get_rect())
        pygame.display.update(self.dirty_rects)

    def draw(self):
        self.surface.blit(self.background, self.get_rect())
        self.sprite.draw(self.surface)

    def getBackground(self, filename):
        from xml.etree import ElementTree as ET
        background = pygame.Surface(SCREENSIZE)
        doc = ET.parse(filename)
        for level in doc.findall('level'):
            level_y = int(level.get('y'))
            for block in level.findall('block'):
                x = int(block.get('x'))
                y = int(block.get('y', level_y))
                type = block.get('type')
                block_sprite = ScratchSprite('cute/%s.png' % blocks[type])
                block_sprite.move_to(x * BLOCK_WIDTH, y * BLOCK_HEIGHT)
                block_sprite.draw(background)
        for building in doc.find('buildings').findall('building'):
            x = int(building.get('x'))
            y = int(building.get('y'))
            type = building.get('type')
            bldg_sprite = ScratchSprite('cute/%s.png' % type)
            bldg_sprite.move_to(x * BLOCK_WIDTH, y * BLOCK_HEIGHT)
            bldg_sprite.draw(background)
        return background

def main():
    global app
    app = App(screensize=SCREENSIZE)
    world = ScratchWorld(app.screen)
    app.add_world(world)
    app.run()

if __name__ == '__main__': main()
