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

def block(width=200, height=45, radius=5, tabwidth=20, tabheight=15, armwidth=20):
    '''
    A basic, single-step block with upper slot, lower tab and no contents
    '''
    def L(x,y):
        # Lx y
        return 'L %d,%d' % (x,y)
    def A(x,y,flag=0):
        # Arx ry x-axis-rotation large-arc-flag sweep-flag x y
        return 'A %d,%d 0 0,%d %d,%d' % (radius, radius, flag, x, y)
    path = ['M %d,0' % radius,
        L(armwidth - radius, 0),
        A(armwidth, radius, 1),
        L(armwidth, tabheight - radius),
        A(armwidth + radius, tabheight),
        L(armwidth + tabwidth - radius, tabheight),
        A(armwidth + tabwidth, tabheight - radius),
        L(armwidth + tabwidth, radius),
        A(armwidth + tabwidth + radius, 0, 1),
        L(width - radius, 0),
        A(width, radius, 1),
        L(width, height - radius),
        A(width - radius, height, 1),
        L(armwidth + tabwidth + radius, height),
        A(armwidth + tabwidth, height + radius),
        L(armwidth + tabwidth, height + tabheight - radius),
        A(armwidth + tabwidth - radius, height + tabheight, 1),
        L(armwidth + radius, height + tabheight),
        A(armwidth, height + tabheight - radius, 1),
        L(armwidth, height + radius),
        A(armwidth - radius, height),
        L(radius, height),
        A(0, height - radius, 1),
        L(0, radius),
        A(radius, 0, 1),
        'z']
    return ' '.join(path)
    
if __name__ == '__main__':
    print block(),