'''
Simple generators for cellular automata
'''

import random

DEFAULT_WIDTH=200
DEFAULT_HEIGHT=200

BLACK = 0,0,0
WHITE = 255,255,255

def points(matrix):
    for x in glen(matrix):
        for y in glen(matrix[x]):
            yield x,y
            
def values(matrix):
    for column in matrix:
        for cell in column:
            yield cell
            
def glen(list_like):
    '''generator for length'''
    return xrange(len(list_like))
            
def four_neighbors(matrix, x, y):
    width = len(matrix[0])
    height = len(matrix)
    return matrix[x-1][y], matrix[(x+1) % width][y], matrix[x][y-1], matrix[x][(y+1) % height]
    
def eight_neighbors(matrix, x, y):
    width = len(matrix[0])
    height = len(matrix)
    return matrix[x-1][y], matrix[(x+1) % width][y], matrix[x][y-1], matrix[x][(y+1) % height], matrix[x-1][y-1], matrix[x-1][(y+1) % height], matrix[(x+1) % width][y-1], matrix[(x+1) % width][(y+1) % height]
            
def generation_by_value(function, matrix):
    return [[function(matrix[x][y]) for y in glen(matrix[x])] for x in glen(matrix)]
    
def generation_by_point(function, matrix):
    return [[function(matrix,x,y) for y in glen(matrix[x])] for x in glen(matrix)]
    
def initialize(function, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    return [[function(x,y) for y in xrange(height)] for x in xrange(width)]
    
def view(matrix, fmt=str):
    for y in glen(matrix[0]):
        print ''.join([fmt(matrix[x][y]) for x in glen(matrix)])
        
def random_binary_matrix():
    return initialize(lambda x,y: random.randint(0,1))
    
def random_real_matrix():
    return initialize(lambda x,y: random.random())
        
EMPTY_MATRIX = initialize(lambda x,y: 0)
UNIT_MATRIX = initialize(lambda x,y: 1)

def test():
    assert(EMPTY_MATRIX != UNIT_MATRIX)
    assert(EMPTY_MATRIX[0][0] == 0)
    assert(EMPTY_MATRIX[DEFAULT_WIDTH-1][DEFAULT_HEIGHT-1] == 0)
    assert(UNIT_MATRIX[0][DEFAULT_HEIGHT-1] == 1)
    assert(UNIT_MATRIX[DEFAULT_WIDTH-1][0] == 1)
    assert(initialize(lambda x,y: 1) == UNIT_MATRIX)
    assert(generation_by_value(lambda value: value + 1, EMPTY_MATRIX), UNIT_MATRIX)
    print 'OK'
    view(EMPTY_MATRIX)
    
def wave(matrix, x, y):
    return sum(eight_neighbors(matrix, x, y)) / 8.0
    
def wave_adapter(value):
    return 0, 0, int(value * 255)

def life(matrix, x, y):
    count = sum(eight_neighbors(matrix, x, y))
    alive = matrix[x][y]
    if alive:
        return 1 < count < 4
    else:
        return count == 3

def life_adapter(value):
    if value: return WHITE
    return BLACK

def pygame_test(matrix_init, generation_function, view_adapter):
    import pygame
    import time
    pygame.init()
    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
    screen.fill(BLACK)
    sbuffer = pygame.surfarray.array3d(screen)
    matrix = matrix_init()
    #view(matrix)
    def draw(matrix, sbuffer):
        for x,y in points(matrix):
            sbuffer[x][y] = view_adapter(matrix[x][y])
        pygame.surfarray.blit_array(screen, sbuffer)
        pygame.display.update()
        return generation_by_point(generation_function, matrix)
    while(True):
        matrix = draw(matrix, sbuffer)
    
    
if __name__ == '__main__':
    #test()
#    pygame_test(random_real_matrix, wave, wave_adapter)
    pygame_test(random_binary_matrix, life, life_adapter)
    
    