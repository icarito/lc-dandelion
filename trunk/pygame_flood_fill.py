# The following is a rewrite of the seed fill algorithm by Paul Heckbert.
# The original was published in "Graphics Gems", Academic Press, 1990.
#
# I have rewitten it here in python using pygame Douglas E Knapp 2005
# Fill background with patter. If you want a solid color make a 1*1
# surface of your color.
# May not work if patern is bigger that surface but then again it might.
# If you make it better or faster please let me know at
# magick.crow(at)gmail.
# If your better is slower without more function I don't want to hear
# about it.
# Also faster means you can tell without looking at the thousanths hand
# of your watch.
# the sk var was put in because the original had a goto in it.

from pygame import Rect

def seed_fillA(surface, x, y, pattern):# sk is for skip. It was a goto
    def push(rect,stack,(y,x,x2,dy)):# push for seed_fill
        if y+dy>=rect.bottom or y+dy<rect.top : return #don't fall of the bottom or top of the surface.
        else : stack.append((y, x, x2, dy))
    if pattern==None : return
    (minx,miny,maxx,maxy)=(x,y,x,y)
    pat_width=pattern.get_width()
    pat_height=pattern.get_height()
    stack=[]
    rect=Rect((0,0),surface.get_size())
    #print pygame.__dict__
    #if hasattr(pygame,'surfarray'):
    try:
        surfaceA=pygame.surfarray.pixels2d(surface)
        patternA=pygame.surfarray.pixels2d(pattern)
        old_color = surfaceA[x][y]
        new_color = patternA[x%pat_width][y%pat_height]#make sure that surface color is not the same as the pattern color
        usearray=True
    except:
        surface.lock()
        pattern.lock()
        old_color = surface.get_at((x,y))
        new_color = pattern.get_at((x, y))
        usearray=False
    if old_color == new_color : return #can't fill with same color
    if not rect.collidepoint(x, y) : return #can't fill off the surface
    push(rect,stack,(y, x, x, 1)) # needed in some cases
    push(rect,stack,(y+1, x, x, -1)) # seed segment (popped 1st)
    sk=0
    while len(stack)>0 :
        (y,x1,x2,dy)=stack.pop()
        y+=dy
        x=x1
        #bigger than the left edge and point is old color
        if usearray:
            while x >= rect.left and surfaceA[x][y] == old_color:
	            surfaceA[x][y]=patternA[x%pat_width][y%pat_height];x-=1
        else:
            while x >= rect.left and surface.get_at((x,y)) == old_color:
                surface.set_at((x,y),pattern.get_at((x%pat_width,y%pat_height)));x-=1

        if x<x1:#find max and min x and y for Rect
            if minx>x : minx=x
            if miny>y : miny=y
            if maxx<x : maxx=x
            if maxy<y : maxy=y
            left = x+1
            if left < x1 : push(rect,stack,(y, left, x1-1, -dy)) # leak on left?
            x = x1+1
        else:
            sk=1
        while True :
            if sk==0 :
                xstart=x
                #draw dot to right if right needs color
                if usearray:
                    while x<rect.right and surfaceA[x][y] == old_color: 
						surfaceA[x][y]=patternA[x%pat_width][y%pat_height];x+=1
                else:
                    while x<rect.right and surface.get_at((x,y)) == old_color: 
						surface.set_at((x,y),pattern.get_at((x%pat_width,y%pat_height)));x+=1
                if x>xstart:
                    if minx>x : minx=x
                    if miny>y : miny=y
                    if maxx<x : maxx=x
                    if maxy<y : maxy=y
                push(rect,stack,(y, left, x-1,  dy))#look on the other side of point, added to stack
                if x > x2+1 : push(rect,stack,(y,x2+1, x-1, -dy)) # leak on right?
            x+=1; sk=0
            if usearray:
                while  x <= x2 and surfaceA[x][y] != old_color:x+=1 #draw right if ??
            else:
                while  x <= x2 and surface.get_at((x,y)) != old_color:x+=1 #draw right if ??
            left = x
            if x>x2 : break
    if usearray:
        del(surfaceA)
        del(patternA)
    else:
        surface.unlock()
        pattern.unlock()
    return Rect(minx,miny,maxx-minx+1,maxy-miny+1)
