from __future__ import with_statement

from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder

def PointDiff(pt1, pt2):
    return pt1[0] - pt2[0], pt1[1] - pt2[1]
    
def PointMin(pt1, pt2):
    return min(pt1[0], pt2[0]), min(pt1[1], pt2[1])
    
def PointMax(pt1, pt2):
    return max(pt1[0], pt2[0]), max(pt1[1], pt2[1])
    
def RectFromPoints(pt1, pt2):
    origin = PointMin(pt1, pt2)
    dest = PointMax(pt1, pt2)
    size = PointDiff(dest, origin)
    return origin, size

class DNSCanvasView(NibClassBuilder.AutoBaseClass):
    # the actual base class is NSView
    
    def awakeFromNib(self):
        self.dragging = False
        self.selectionOrigin = (0,0)
        self.selectionRect = (0,0),(0,0)
    
    def drawRect_(self, rect):
        NSColor.whiteColor().set()
        NSRectFill(rect)
        if self.dragging:
            NSColor.gridColor().set()
            print 'selection rect:', (self.selectionRect,)
            path = NSBezierPath.bezierPathWithRect_(self.selectionRect)
            path.setLineWidth_(1.0)
            path.stroke()
        
        
    def mouseDown_(self, event):
        #location = event.locationInWindow()
        #child = self.hitTest_(location)
        #if child is not self:
            
        #else:
        self.selectionOrigin = event.locationInWindow()
        
    def mouseUp_(self, event):
        self.dragging = False
        self.setNeedsDisplay_(True)
        
    def mouseDragged_(self, event): 
        self.dragging = True
        self.selectionRect = RectFromPoints(self.selectionOrigin, event.locationInWindow())
        self.setNeedsDisplay_(True)
        
