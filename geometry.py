'''
Utility functions for drawing
'''
from math import sin, cos, pi, sqrt, atan, radians, degrees

PI_3RD = pi / 3.0
PI_6TH = pi / 6.0

SQRT_3 = sqrt(3)

def round_int(num):
  return int(round(num))


def polarToCart(radius, theta):
  # theta is in radians
  # returns x, y coordinates
  return radius * cos(theta), radius * sin(theta)

# Y is reversed in graphics
def polarToCartR(radius, theta):
  return radius * cos(theta), radius * sin(theta) * -1

def cartToPolar(x,y):
  # returns radius, theta (in radians)
  # special case axes:
  if x == 0 and y == 0: return 0.0, 0.0 # should this be an error
  elif x == 0 and y > 0: return y, pi / 2.0
  elif x == 0 and y < 0: return -y, 3 * pi / 2.0
  elif y == 0 and x > 0: return x, 0.0
  elif y == 0 and x < 0: return -x, pi
  # special case quadrants
  radius = sqrt(x*x + y*y)
  theta = atan(y/x) # this is only valid for first quadrant (x and y positive)
  if x > 0 and y > 0:
    #print 'first quadrant'
    pass
  elif x < 0 and y > 0: 
    #print 'second quadrant'
    theta += pi 
  elif x < 0 and y < 0: 
    #print 'third quadrant'
    theta += pi 
  elif x > 0 and y < 0: 
    #print 'fourth quadrant'
    theta += (2.0 * pi) # fourth quadrant
  return radius, theta

def angle_to_point(origin, pt):
  # translate to origin
  rel_pt = translate_r(pt, origin)
  dist, angle = cartToPolar(*rel_pt)
  return degrees(angle)

def mag(p1, p2):
  # distance from p1 to p2
  x = p2[0] - p1[0]
  y = p2[1] - p1[1]
  return sqrt(x * x + y * y)

def slope(a,b):
  if a[0] == b[0]: return 'VERTICAL'
  return (b[1] - a[1]) / (b[0] - a[0])


def intersection(a,b,c,d):
  Ax,Ay = a; Bx,By = b; Cx,Cy = c; Dx,Dy = d
  u = ((Dx-Cx)*(Ay-Cy)-(Dy-Cy)*(Ax-Cx)) / ((Dy-Cy)*(Bx-Ax)-(Dx-Cx)*(By-Ay))
  x = Ax + u*(Bx-Ax)
  y = Ay + u*(By-Ay)
  return x,y

def perpendicular(a,b):
  m = midpoint(a,b)
  s = slope(a,b)
  if s== 'VERTICAL':
    x = m[0] + 1
    y = m[1] 
  elif s== 0:
    x = m[0]
    y = m[1] + 1
  else:
    # point-slope form y = s(x - m[0]) + m[1], but by choosing 
    # x = m[x] + 1 we collapse it to the version shown here
    # perpendicular slope is -1/slope
    x = m[0] + 1
    y = m[1] + -1/s
  return m,(x,y)
  
def midpoint(p1,p2):
  return (p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5

X = 0
Y = 1

def shift(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]

def shiftAll(l,center):
    return [shift(p,center) for p in l]

# hexpoints should result in the following:
# 
#
#      2  1
#   3        0
#      4  5
#
#

def hexpoints(center, r, horizontal=False):
  offset = 0
  if horizontal: offset = halfTheta
  # trig methods to find the hex corners
  return [translate(polarToCart(r, i*theta + offset), center) for i in hexsides] # basic hex


def _polypoints(center, r, numPoints, degreesRotation=0):
    '''
    center is a point, a tuple of two numbers
    r is a distance
    numPoints is an integer, at least 3
    degreesRotation is a float representing how far to turn before starting
    '''
    if numPoints < 3: raise ValueError, 'Must have at least 3 points in a polygon'
    rotation = radians(degreesRotation)
    theta = (pi * 2) / numPoints
    return [translate(polarToCart(r, i*theta + rotation), center) for i in range(numPoints)]

def poly_point(center, r, degrees):
    x = r * cos(degrees) + center[0]
    y = r * sin(degrees) + center[1]
    return x,y

def polypoints(center, r, numPoints, degreesRotation=0):
    if numPoints < 3: raise ValueError, 'Must have at least 3 points in a polygon'
    rotation = radians(degreesRotation)
    theta = (pi * 2) / numPoints
    return [poly_point(center, r, i*theta+rotation) for i in range(numPoints)]
    

def translate(p1, p2):
  return p1[0] + p2[0], p1[1] + p2[1]

def translate_r(p1, p2):
  # inverse of translate
  return p1[0] - p2[0], p1[1] - p2[1]

def rotate(pt, angle):
  # expect angle in radians
  x,y = pt
  x1 = cos(angle) * x - sin(angle) * y
  y1 = sin(angle) * x + cos(angle) * y
  return x1,y1

def rotate_deg(pt, angle):
  return rotate(pt, radians(angle))

def rotate_on_origin(pt, origin, angle):
  # expects angle in degrees
  #pt1 = translate_r(pt, origin)
  pt2 = rotate_deg(pt, angle)
  pt3 = translate(pt2, origin)
  return pt3

def rotate_on_origin_all(pts, origin, angle):
  return [rotate_on_origin(pt, origin, angle) for pt in pts]

def point_at_distance(origin, angle, distance):
  # expects angle in degrees
  angle = radians(angle)
  x = origin[X] + cos(angle) * distance
  y = origin[Y] + sin(angle) * distance
  return x,y

def translateAll(l,center):
  return [translate(p,center) for p in l]

translate_all = translateAll

hexsides = range(6)
theta = pi / 3.0
halfTheta = theta / 2.0
W = sqrt(3) 

def vector_dot(a,b):
  # dot product, a and b are vectors
  return a[X] * b[X] + a[Y] * b[Y]

def vector_angle(a,b):
  # angle between two vectors
  return arctan(dot(a,b))

def min(x,y):
  if x > y: return y
  return x


def line_range(start, end, steps):
  x,y = start
  xE,yE = end
  dX = (xE-x)/float(steps)
  dY = (yE-y)/float(steps)
  return [(x+dX*i,y+dY*i) for i in range(steps)]

def arc_range(origin, radius, start, end, steps):
  if end < start: end += pi * 2
  dT = (end - start)/float(steps)
  def arc_point(idx):
    return translate(polarToCartR(radius, start + dT * idx), origin)
  return [arc_point(i) for i in range(steps)]

class Vector:

  '''
  Yet another minimalist vector class
  '''

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    if isinstance(other, Vector):
      return Vector(self.x + other.x, self.y + other.y)
    else:
      return Vector(self.x + other, self.y + other)

  def __sub__(self, other):
    if isinstance(other, Vector):
      return Vector(self.x - other.x, self.y - other.y)
    else:
      return Vector(self.x - other, self.y - other)

  def __mul__(self, other):
    return Vector(self.x * other, self.y * other)

  def __div__(self, other):
    return Vector(self.x / other, self.y / other)

  def magnitude(self):
    return sqrt(self.x ** 2, self.y ** 2)

  def dot(self, other):
    return self.x * other.x + self.y + other.y


