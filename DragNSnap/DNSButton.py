from __future__ import with_statement

from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder

from DNSView import PointDiff

ARMWIDTH = 20
TAILWIDTH = 10
LEGWIDTH = 15
TABWIDTH = 10
TABHEIGHT = 5
RADIUS = 6
SMALLRADIUS = RADIUS / 2

def MovePoint(pt, dx, dy):
    return pt[0] + dx, pt[1] + dy

def MoveRect(rect, newLocation):
    origin, size = rect
    return PointDiff(origin, newLocation), size
    
def MidPoint(pt1, pt2):
    return (pt1[0] + pt2[0]) / 2.0, (pt1[1] + pt2[1]) / 2.0
    
def tab(path, left, right):
    insetLeft  = MovePoint(left, RADIUS, 0)
    tabTopLeft = MovePoint(insetLeft, TABWIDTH, 0)
    tabBottomLeft = MovePoint(tabTopLeft, 0, -TABHEIGHT)
    tabBottomRight = MovePoint(tabBottomLeft, TABWIDTH, 0)
    tabTopRight = MovePoint(tabTopLeft, TABWIDTH, 0)
    insetRight = MovePoint(right, -RADIUS, 0) 

    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabTopLeft, tabBottomLeft, SMALLRADIUS)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabBottomLeft, tabBottomRight, SMALLRADIUS)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabBottomRight, tabTopRight, SMALLRADIUS)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabTopRight, insetRight, SMALLRADIUS)
    path.lineToPoint_(insetRight)
    
def tabR(path, right, left):
    insetLeft  = MovePoint(left, RADIUS, 0)
    tabTopLeft = MovePoint(insetLeft, TABWIDTH, 0)
    tabBottomLeft = MovePoint(tabTopLeft, 0, -TABHEIGHT)
    tabBottomRight = MovePoint(tabBottomLeft, TABWIDTH, 0)
    tabTopRight = MovePoint(tabTopLeft, TABWIDTH, 0)
    insetRight = MovePoint(right, -RADIUS, 0) 

    path.appendBezierPathWithArcFromPoint_toPoint_radius_(insetRight, tabTopRight, SMALLRADIUS)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabTopRight, tabBottomRight, SMALLRADIUS)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabBottomRight, tabBottomLeft, SMALLRADIUS)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabBottomLeft, tabTopLeft, SMALLRADIUS)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(tabTopLeft, insetLeft, SMALLRADIUS)
    path.lineToPoint_(insetLeft)
    
def butt(path, bottomLeft, topLeft, radius=RADIUS):
    '''
    Draw a line around the left edge, clockwise from bottom to top, with curved corners top and bottom.  The line should be concave on the right.
    '''
    midLeft = MidPoint(bottomLeft, topLeft)
    insetTopLeft = MovePoint(topLeft, radius, 0)
    insetBottomLeft = MovePoint(bottomLeft, radius, 0)

    path.appendBezierPathWithArcFromPoint_toPoint_radius_(insetBottomLeft, bottomLeft, radius)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(bottomLeft, midLeft, radius)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(midLeft, topLeft, radius)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(topLeft, insetTopLeft, radius)
    
def cap(path, topRight, bottomRight, radius=RADIUS):
    '''
    Draw a line around the right edge, clockwise from top to bottom, with curved corners top and bottom.  The line should be concave on the left.
    '''
    midRight = MidPoint(topRight, bottomRight)
    insetTopRight = MovePoint(topRight, -radius, 0)
    insetBottomRight = MovePoint(bottomRight, -radius, 0)

    path.appendBezierPathWithArcFromPoint_toPoint_radius_(insetTopRight, topRight, radius)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(topRight, midRight, radius)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(midRight, bottomRight, radius)
    path.appendBezierPathWithArcFromPoint_toPoint_radius_(bottomRight, insetBottomRight, radius)
    
def sortSubviews(view1, view2, context):
    if view1 is context:
        return NSOrderedDescending
    if view2 is context:
        return NSOrderedAscending
    return NSOrderedSame
    
class DNSButton(NSControl):
    # the actual base class is NSControl
    
    def initWithFrame_(self, frameRect):
        super(DNSButton, self).initWithFrame_(frameRect)
        self.colour = NSColor.blueColor()
        self.dragOrigin = (0,0)
        self._initOutline()
        return self
        
    def viewRect(self):
        (x, y), (width, height) = self.bounds()
        return (x+1, y + TABHEIGHT + 1), (width - 2, height - TABHEIGHT - 2)
        
    def _initOutline(self):
        rect = self.viewRect()
        topLeft = NSMinX(rect), NSMaxY(rect)
        insetTopLeft = MovePoint(topLeft, RADIUS, 0)
        topRight = NSMaxX(rect), NSMaxY(rect)
        bottomRight = NSMaxX(rect), NSMinY(rect)
        bottomLeft = NSMinX(rect), NSMinY(rect)
        self.outline = NSBezierPath.bezierPath()
        self.outline.moveToPoint_(insetTopLeft)
        tab(self.outline, topLeft, topRight)
        cap(self.outline, topRight, bottomRight)
        tabR(self.outline, bottomRight, bottomLeft)
        butt(self.outline, bottomLeft, topLeft)
        
    def drawRect_(self, rect):
        self.colour.set()
        self.outline.fill()
        NSColor.blackColor().set()
        self.outline.stroke()
        
    def mouseDown_(self, event):
        self.dragOrigin = event.locationInWindow()
        self.superview().sortSubviewsUsingFunction_context_(sortSubviews, self)
        
    def mouseDragged_(self, event):
        location = event.locationInWindow()
        offset = PointDiff(self.dragOrigin, location)
        print 'DNSButton mouseDragging with offset:', offset
        self.setFrame_(MoveRect(self.frame(), offset))
        self.dragOrigin = location
        self.superview().setNeedsDisplay_(True)
                
class DNSTrigger(DNSButton):
    pass
    
class DNSExpression(DNSButton):

    def initWithFrame_(self, frame):
        (x,y),(w,h) = frame
        adjFrame = (x,y),(w, ARMWIDTH + RADIUS * 2 + 2)
        return super(DNSExpression, self).initWithFrame_(frame)

class DNSVariable_(DNSExpression):

    def initWithFrame_(self, frame):
        self = super(DNSIntVariable, self).initWithFrame_(frame)
        self.color = NSColor.orangeColor()
        return self

    def _initOutline(self):
        rect = self.viewRect() 

class DNSStep(DNSButton):

    def initWithFrame_(self, frame):
        self.frameType = 'variable'
        (x,y),(w,h) = frame
        adjFrame = (x,y),(w, ARMWIDTH + RADIUS * 2 + 2)
        return super(DNSStep, self).initWithFrame_(frame)
    
    def _initOutline(self):
        rect = self.viewRect()
        topLeft = NSMinX(rect), NSMaxY(rect)
        insetTopLeft = MovePoint(topLeft, RADIUS, 0)
        topRight = NSMaxX(rect), NSMaxY(rect)
        bottomRight = NSMaxX(rect), NSMinY(rect)
        bottomLeft = NSMinX(rect), NSMinY(rect)
        
        self.outline = NSBezierPath.bezierPath()
        self.outline.moveToPoint_(insetTopLeft)

        tab(self.outline, topLeft, topRight)
        cap(self.outline, topRight, bottomRight)
        tabR(self.outline, bottomRight, bottomLeft)
        butt(self.outline, bottomLeft, topLeft)
        
class DNSContainer(DNSButton):
    
    def _initOutline(self):
        rect = self.viewRect()
        topLeft = NSMinX(rect), NSMaxY(rect)
        insetTopLeft = MovePoint(topLeft, RADIUS, 0)
        bottomLeftOfTopArm = MovePoint(topLeft, LEGWIDTH, -ARMWIDTH)
        topRight = NSMaxX(rect), NSMaxY(rect)
        bottomRightOfTopArm = MovePoint(topRight, 0, -ARMWIDTH)
        bottomRight = NSMaxX(rect), NSMinY(rect)
        topRightOfBottomArm = MovePoint(bottomRight, 0, ARMWIDTH)
        bottomLeft = NSMinX(rect), NSMinY(rect)
        topLeftOfBottomArm = MovePoint(bottomLeft, LEGWIDTH, ARMWIDTH)

        self.outline = NSBezierPath.bezierPath()
        self.outline.moveToPoint_(insetTopLeft)

        tab(self.outline, topLeft, topRight)
        cap(self.outline, topRight, bottomRightOfTopArm)
        tabR(self.outline, bottomRightOfTopArm, bottomLeftOfTopArm)
        butt(self.outline, bottomLeftOfTopArm, topLeftOfBottomArm)
        cap(self.outline, topRightOfBottomArm, bottomRight)
        tabR(self.outline, bottomRight, bottomLeft)
        butt(self.outline, bottomLeft, topLeft)

