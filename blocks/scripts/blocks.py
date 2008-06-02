'''
via: http://www.w3.org/TR/SVG11/shapes.html#RectElement

Mathematically, a 'rect' element can be mapped to an equivalent 'path' element as follows: (Note: all coordinate and length values are first converted into user space coordinates according to Units.)

perform an absolute moveto operation to location (x+rx,y), where x is the value of the 'rect' element's x attribute converted to user space, rx is the effective value of the rx attribute converted to user space and y is the value of the y attribute converted to user space
perform an absolute horizontal lineto operation to location (x+width-rx,y), where width is the 'rect' element's width attribute converted to user space
perform an absolute elliptical arc operation to coordinate (x+width,y+ry), where the effective values for the rx and ry attributes on the 'rect' element converted to user space are used as the rx and ry attributes on the elliptical arc command, respectively, the x-axis-rotation is set to zero, the large-arc-flag is set to zero, and the sweep-flag is set to one
perform a absolute vertical lineto to location (x+width,y+height-ry), where height is the 'rect' element's height attribute converted to user space
perform an absolute elliptical arc operation to coordinate (x+width-rx,y+height)
perform an absolute horizontal lineto to location (x+rx,y+height)
perform an absolute elliptical arc operation to coordinate (x,y+height-ry)
perform an absolute absolute vertical lineto to location (x,y+ry)
perform an absolute elliptical arc operation to coordinate (x+rx,y)
'''

output_template = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%%" height="100%%" version="1.1"
xmlns="http://www.w3.org/2000/svg">
<defs>
  <filter id="MyFilter" filterUnits="userSpaceOnUse" x="0" y="0" width="200" height="120">
    <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
    <!--feOffset in="blur" dx="4" dy="4" result="offsetBlur"/-->
    <feSpecularLighting in="blur" surfaceScale="5" specularConstant=".75" 
                        specularExponent="20" lighting-color="#bbbbbb"  
                        result="specOut">
      <fePointLight x="-5000" y="-10000" z="20000"/>
    </feSpecularLighting>
    <feComposite in="specOut" in2="SourceAlpha" operator="in" result="specOut"/>
    <feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" 
                 k1="0" k2="1" k3="1" k4="0" result="litPaint"/>
    <!--feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="litPaint"/>
    </feMerge-->
  </filter>
</defs>
%s
</svg>'''

class Block(object):

    def __init__(self, **kws):
        self.color = 'blue'
        self.width = 1000
        self.height = 25
        self.radius = 3
        self.tabwidth = 11
        self.tabheight = 6
        self.armheight = 20
        self.legwidth = 15
        self.type = 'block'
        self.top = 0
        self.template = template = '<path filter="url(#MyFilter)" id="%(type)s" fill="%(color)s" d="%(path)s" />'
        self.__dict__.update(kws) # allow keyword arguments to over-ride defaults
        self.last_x = 0
        self.last_y = self.radius
        
    def moveto(self, x, y):
        self.last_x = x
        self.last_y = y
        return 'M %d,%d' % (x,y)
        
    def arcto(self, x, y, flag=0):
        self.last_x, self.last_y = x,y
        return 'A %d,%d 0 0,%d %d,%d' % (self.radius, self.radius, flag, x, y)
        
    def lineto(self, x=None, y=None):
        if x is not None:
            self.last_x = x
        if y is not None:
            self.last_y = y
        return 'L %d,%d' % (self.last_x,self.last_y)
        
    def hlineto(self, x):
        return self.lineto(x=x)
        
    def hlineby(self, dx):
        return self.lineto(x = self.last_x + dx)
        
    def vlineto(self, y):
        return self.lineto(y=y)
        
    def vlineby(self, dy):
        return self.lineto(y=self.last_y + dy)
        
    def tl_arc_cw(self):
        '''Top left corner of a rounded rect, clockwise'''
        x = self.last_x + self.radius
        y = self.last_y - self.radius
        return self.arcto(x,y,1)
        
    def tr_arc_cw(self):
        '''Top right corner of a rounded rect, clockwise'''
        x = self.last_x + self.radius
        y = self.last_y + self.radius
        return self.arcto(x,y,1)
        
    def br_arc_cw(self):
        '''Bottom right corner of a rounded rect, clockwise'''
        x = self.last_x - self.radius
        y = self.last_y + self.radius
        return self.arcto(x,y,1)
        
    def bl_arc_cw(self):
        '''Bottom left corner of a rounded rect, clockwise'''
        x = self.last_x - self.radius
        y = self.last_y - self.radius
        return self.arcto(x,y,1)
        
    def bl_arc_acw(self):
        '''Bottom left corner of a rounded rect, anti-clockwise'''
        x = self.last_x + self.radius
        y = self.last_y + self.radius
        return self.arcto(x,y,0)
        
    def br_arc_acw(self):
        '''Bottom right corner of a rounded rect, anti-clockwise'''
        x = self.last_x + self.radius
        y = self.last_y - self.radius
        return self.arcto(x,y,0)
    
    def tr_arc_acw(self):
        '''Top right corner of a rounded rect, anti-clockwise'''
        x = self.last_x - self.radius
        y = self.last_y - self.radius
        return self.arcto(x,y,0)
    
    def tl_arc_acw(self):
        '''Top left corner of a rounded rect, anti-clockwise'''
        x = self.last_x - self.radius
        y = self.last_y + self.radius
        return self.arcto(x,y,0)
        
    def slot(self):
        tabheight, tabwidth = self.tabheight, self.tabwidth
        radius2 = self.radius * 2
        return [
            self.tr_arc_cw(), # top-left arc of slot
            self.vlineby(tabheight - radius2),
            self.bl_arc_acw(), # bottom-left arc of slot
            self.hlineby(tabwidth - radius2),
            self.br_arc_acw(), # bottom-right arc of slot
            self.vlineby(-(tabheight - radius2)),
            self.tl_arc_cw()] # top-right arc of slot
        
    def top_with_slot(self):
        width, legwidth = self.width, self.legwidth
        radius = self.radius
        return [
            self.moveto(0,radius),
            self.tl_arc_cw(),    # top-left corner
            self.hlineto(legwidth - radius)] + self.slot() + [ 
            self.hlineto(width - radius),
            self.tr_arc_cw()] # top-right corner
            
    def hat(self):
        return 'A 60,10 0 0,1 120,10'

    def top_with_hat(self):
        width, legwidth = self.width, self.legwidth
        radius = self.radius
        return [
            self.moveto(0,self.top),
            self.hat(),
            self.hlineto(width - radius),
            self.tr_arc_cw()] # top-right corner
        
            
    def top_flat(self):
        return ['M 0,%s' % self.radius,
            self.tl_arc_cw(), # top-left corner
            self.hlineto(self.width - self.radius),
            self.tr_arc_cw()] # top-right corner
        
    def tab(self):
        radius2 = self.radius * 2
        tabwidth, tabheight = self.tabwidth, self.tabheight
        return [
            self.tl_arc_acw(), # top-right arc of tab
            self.vlineby(tabheight - radius2),
            self.br_arc_cw(), # bottom-right arc of tab
            self.hlineby(-(tabwidth - radius2)),
            self.bl_arc_cw(), # bottom-left arc of tab
            self.vlineby(-(tabheight - radius2)),
            self.tr_arc_acw()] # top-left arc of tab 
    
    def bottom_with_tab(self):
        radius = self.radius
        tabwidth, legwidth = self.tabwidth, self.legwidth
        return [
            self.br_arc_cw(), # bottom-right corner
            self.hlineto(legwidth + tabwidth + radius)] + self.tab() + [
            self.hlineto(radius),
            self.bl_arc_cw()] # bottom-left corner
            
    def inner_bottom_with_tab(self):
        radius = self.radius
        tabwidth, legwidth = self.tabwidth, self.legwidth
        return [
            self.br_arc_cw(), # bottom right corner
            self.hlineto(legwidth * 2 + tabwidth + radius)] + self.tab() + [
            self.hlineto(legwidth + radius),
            self.tl_arc_acw()]
            
    def inner_left_side(self):
        return [self.vlineto(self.height - (self.legwidth + self.radius))]
        
    def inner_bottom_flat(self):
        return [self.bl_arc_acw(),
                self.hlineto(self.width - self.radius),
                self.tr_arc_cw()]
    
    def right_side(self):
        return [self.vlineto(self.height - self.radius)]
        
    def left_side(self):
        return ['z']
        
    def right_arm_side(self):
        return [self.vlineby(self.armheight - self.radius * 2)]
        
    def save(self):
        f = open('images/' + self.type + '_' + self.color +  '.svg', 'w')
        f.write(self.fileout())
        f.close()
        
    def convert(self):
        import os, subprocess
        cwd = os.path.join(os.getcwd(), 'images')
        os.environ['locale'] = 'C'
        bin = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
        svgfile = os.path.join(cwd, self.type + '_' + self.color + '.svg')
        pngfile = os.path.join(cwd, self.type + '_' + self.color + '.png')
        subprocess.check_call([bin, '--without-gui', '--file=%s' % svgfile, '--export-id=%s' % self.type, '--export-id-only',
            '--export-png=%s' % pngfile])
            
    def update(self):
        self.save()
        self.convert()
        
    def fileout(self):
        return output_template % self
        
    def __str__(self):
        path = ' '.join(self.top_with_slot() + self.right_side() + self.bottom_with_tab() + self.left_side())
        color = self.color
        type = self.type
        return self.template % locals()
        
class Container(Block):

    def __init__(self, **kws):
        super(Container, self).__init__(**kws)
        if 'height' not in kws:
            self.height = 1000
        if 'type' not in kws:
            self.type = 'container'
    
    def __str__(self):
        path = ' '.join(self.top_with_slot() + self.right_arm_side() + self.inner_bottom_with_tab() + self.inner_left_side() + self.inner_bottom_flat() + self.right_arm_side() + self.bottom_with_tab() + self.left_side())
        color = self.color
        type = self.type
        return self.template % locals()
        
class Trigger(Block):

    def __init__(self, **kws):
        super(Trigger, self).__init__(**kws)
        if 'top' not in kws:
            self.top = 10
        if 'type' not in kws:
            self.type = 'trigger'

    def __str__(self):
        path = ' '.join(self.top_with_hat() + self.right_side() + self.bottom_with_tab() + self.left_side())
        color = self.color
        type = self.type
        return self.template % locals()
        

def demo():
    return '''<svg x="10" y="20">%s</svg>
    <svg x="10" y="60">%s</svg>
    <svg x="10" y="160">%s</svg>''' % (Block(), Container(), Trigger())


if __name__ == '__main__':
    import sys
    if sys.argv > 1:
        color = sys.argv[1]
    else:
        color = 'blue'
    for C in [Block, Container, Trigger]:
        C(color=color).update()
