#The scanline floodfill algorithm using our own stack routines, faster
# via http://student.kuleuven.be/~m0216922/CG/floodfill.html

import pygame

def flood_fill(surface, seed_pos, newColor):
    
   screenBuffer = pygame.surfarray.array3d(surface)
   x,y = seed_pos
   oldColor = tuple(screenBuffer[x][y])
   oldColor = [int(val) for val in oldColor]
   oldColor = tuple(oldColor)
   newColor = newColor[0], newColor[1], newColor[2] # drop alpha, if present
      
   print 'comparing oldColor (%s) with newColor (%s) (%s)' % (oldColor, newColor, oldColor == newColor)
   if oldColor == newColor:
       return
   stack = []

   w, h = surface.get_rect().size
   max_x = max_y = 0
   min_x = w
   min_y = h

   stack.append(seed_pos)
   while(stack):
       x,y = stack.pop()
       y1 = y
       while y1 >= 0 and tuple(screenBuffer[x][y1]) == oldColor:
            y1 -= 1
       y1 += 1
       spanLeft = spanRight = False
       while(y1 < h and tuple(screenBuffer[x][y1]) == oldColor ):
           screenBuffer[x][y1] = newColor
           min_x = min(min_x, x)
           max_x = max(max_x, x)
           min_y = min(min_y, y1)
           max_y = max(max_y, y1)
           if not spanLeft and x > 0 and tuple(screenBuffer[x - 1][y1]) == oldColor:
               stack.append((x - 1, y1))
               spanLeft = True
           elif spanLeft and x > 0 and tuple(screenBuffer[x - 1][y1]) != oldColor:
               spanLeft = False
           if not spanRight and x + 1 < w and tuple(screenBuffer[x + 1][y1]) == oldColor:
               stack.append((x + 1, y1))
               spanRight = True
           elif spanRight and x + 1 < w and tuple(screenBuffer[x + 1][y1]) != oldColor:
               spanRight = False
           y1 += 1
   pygame.surfarray.blit_array(surface, screenBuffer)
   return pygame.Rect(min_x, min_y, 1 + max_x - min_x, 1 + max_y - min_y)


