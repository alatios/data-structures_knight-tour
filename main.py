#!/usr/bin/env python3

## To do:
## 1. Implement time counter

import numpy as np
from math import floor

### KNIGHT ALLOWED MOVES (OFFSETS)
allowedOffsetMoves = {(-2,-1),
                      (-1,-2),
                      (+1,-2),
                      (+2,-1),
                      (+2,+1),
                      (+1,+2),
                      (-1,+2),
                      (-2,+1)
}

### SIX BASE STRUCTURED KNIGHT TOURS
## Coords based on chess algebraic notation

####### 6x6 #######
##    # # # # # # 6
##    # # # # # # 5
##    # # # # # # 4
##    + # # # # # 3
##    # # # # # # 2
##    # # # # # # 1
##    1 2 3 4 5 6
##
##    Cell + is (1,3)

path6x6 = {
    (1,1): [(2,3),(3,2)], (2,3): [(3,1),(1,1)],
    (3,1): [(1,2),(2,3)], (1,2): [(3,3),(3,1)],
    (3,3): [(5,2),(1,2)], (5,2): [(6,4),(3,3)],
    (6,4): [(5,6),(5,2)], (5,6): [(3,5),(6,4)],
    (3,5): [(1,6),(5,6)], (1,6): [(2,4),(3,5)],
    (2,4): [(4,3),(1,6)], (4,3): [(5,5),(2,4)],
    (5,5): [(3,6),(4,3)], (3,6): [(1,5),(5,5)],
    (1,5): [(3,4),(3,6)], (3,4): [(2,6),(1,5)],
    (2,6): [(1,4),(3,4)], (1,4): [(2,2),(2,6)],
    (2,2): [(4,1),(1,4)], (4,1): [(6,2),(2,2)],
    (6,2): [(5,4),(4,1)], (5,4): [(6,6),(6,2)],
    (6,6): [(4,5),(5,4)], (4,5): [(5,3),(6,6)],
    (5,3): [(6,1),(4,5)], (6,1): [(4,2),(5,3)],
    (4,2): [(2,1),(6,1)], (2,1): [(1,3),(4,2)],
    (1,3): [(2,5),(2,1)], (2,5): [(4,6),(1,3)],
    (4,6): [(6,5),(2,5)], (6,5): [(4,4),(4,6)],
    (4,4): [(6,3),(6,5)], (6,3): [(5,1),(4,4)],
    (5,1): [(3,2),(6,3)], (3,2): [(1,1),(5,1)]
}

######### 8x8 #########
##    # # # # # # # # 8
##    # # # # # # # # 7
##    # # # # # # # # 6
##    # # # # # # # # 5
##    # # # # # + # # 4
##    # # # # # # # # 3
##    # # # # # # # # 2
##    # # # # # # # # 1
##    1 2 3 4 5 6 7 8
##
##    Cell + is (6,4)

path8x8 = {
    (1,1): [(2,3),(3,2)], (2,3): [(3,1),(1,1)],
    (3,1): [(1,2),(2,3)], (1,2): [(2,4),(3,1)],
    (2,4): [(1,6),(1,2)], (1,6): [(2,8),(2,4)],
    (2,8): [(3,6),(1,6)], (3,6): [(1,5),(2,8)],
    (1,5): [(2,7),(3,6)], (2,7): [(4,8),(1,5)],
    (4,8): [(6,7),(2,7)], (6,7): [(8,8),(4,8)],
    (8,8): [(7,6),(6,7)], (7,6): [(8,4),(8,8)],
    (8,4): [(6,5),(7,6)], (6,5): [(7,7),(8,4)],
    (7,7): [(8,5),(6,5)], (8,5): [(7,3),(7,7)],
    (7,3): [(8,1),(8,5)], (8,1): [(6,2),(7,3)],
    (6,2): [(4,1),(8,1)], (4,1): [(2,2),(6,2)],
    (2,2): [(1,4),(4,1)], (1,4): [(2,6),(2,2)],
    (2,6): [(1,8),(1,4)], (1,8): [(3,7),(2,6)],
    (3,7): [(5,8),(1,8)], (5,8): [(6,6),(3,7)],
    (6,6): [(8,7),(5,8)], (8,7): [(6,8),(6,6)],
    (6,8): [(4,7),(8,7)], (4,7): [(3,5),(6,8)],
    (3,5): [(4,3),(4,7)], (4,3): [(5,5),(3,5)],
    (5,5): [(3,4),(4,3)], (3,4): [(1,3),(5,5)],
    (1,3): [(2,1),(3,4)], (2,1): [(4,2),(1,3)],
    (4,2): [(5,4),(2,1)], (5,4): [(4,6),(4,2)],
    (4,6): [(3,8),(5,4)], (3,8): [(1,7),(4,6)],
    (1,7): [(2,5),(3,8)], (2,5): [(3,3),(1,7)],
    (3,3): [(5,2),(2,5)], (5,2): [(4,4),(3,3)],
    (4,4): [(6,3),(5,2)], (6,3): [(7,1),(4,4)],
    (7,1): [(8,3),(6,3)], (8,3): [(7,5),(7,1)],
    (7,5): [(5,6),(8,3)], (5,6): [(6,4),(7,5)],
    (6,4): [(4,5),(5,6)], (4,5): [(5,7),(6,4)],
    (5,7): [(7,8),(4,5)], (7,8): [(8,6),(5,7)],
    (8,6): [(7,4),(7,8)], (7,4): [(8,2),(8,6)],
    (8,2): [(6,1),(7,4)], (6,1): [(5,3),(8,2)],
    (5,3): [(7,2),(6,1)], (7,2): [(5,1),(5,3)],
    (5,1): [(3,2),(7,2)], (3,2): [(1,1),(5,1)]
}

########### 10x10 ###########
##    # # # # # # # # # # 10
##    # # # # # # # # # # 9
##    # # # # # # # # # # 8
##    # # # # # # # # + # 7
##    # # # # # # # # # # 6
##    # # # # # # # # # # 5
##    # # # # # # # # # # 4
##    # # # # # # # # # # 3
##    # # # # # # # # # # 2
##    # # # # # # # # # # 1
##    1 2 3 4 5 6 7 8 9 10
##
##    Cell + is (9,7)

path10x10 = {
    (1,1): [(2,3),(3,2)],   (2,3): [(4,4),(1,1)],
    (4,4): [(5,6),(2,3)],   (5,6): [(6,8),(4,4)],
    (6,8): [(4,7),(5,6)],   (4,7): [(5,5),(6,8)],
    (5,5): [(3,4),(4,7)],   (3,4): [(2,6),(5,5)],
    (2,6): [(4,5),(3,4)],   (4,5): [(5,3),(2,6)],
    (5,3): [(7,4),(4,5)],   (7,4): [(6,6),(5,3)],
    (6,6): [(7,8),(7,4)],   (7,8): [(8,6),(6,6)],
    (8,6): [(6,7),(7,8)],   (6,7): [(5,9),(8,6)],
    (5,9): [(7,10),(6,7)],  (7,10): [(8,8),(5,9)],
    (8,8): [(7,6),(7,10)],  (7,6): [(5,7),(8,8)],
    (5,7): [(6,5),(7,6)],   (6,5): [(4,6),(5,7)],
    (4,6): [(5,4),(6,5)],   (5,4): [(6,2),(4,6)],
    (6,2): [(4,1),(5,4)],   (4,1): [(3,3),(6,2)],
    (3,3): [(2,1),(4,1)],   (2,1): [(1,3),(3,3)],
    (1,3): [(2,5),(2,1)],   (2,5): [(3,7),(1,3)],
    (3,7): [(1,8),(2,5)],   (1,8): [(2,10),(3,7)],
    (2,10): [(4,9),(1,8)],  (4,9): [(6,10),(2,10)],
    (6,10): [(5,8),(4,9)],  (5,8): [(7,7),(6,10)],
    (7,7): [(9,6),(5,8)],   (9,6): [(8,4),(7,7)],
    (8,4): [(10,5),(9,6)],  (10,5): [(9,7),(8,4)],
    (9,7): [(10,9),(10,5)], (10,9): [(8,10),(9,7)],
    (8,10): [(6,9),(10,9)], (6,9): [(4,10),(8,10)],
    (4,10): [(3,8),(6,9)],  (3,8): [(1,9),(4,10)],
    (1,9): [(3,10),(3,8)],  (3,10): [(4,8),(1,9)],
    (4,8): [(2,9),(3,10)],  (2,9): [(1,7),(4,8)],
    (1,7): [(3,6),(2,9)],   (3,6): [(1,5),(1,7)],
    (1,5): [(2,7),(3,6)],   (2,7): [(3,5),(1,5)],
    (3,5): [(1,4),(2,7)],   (1,4): [(2,2),(3,5)],
    (2,2): [(4,3),(1,4)],   (4,3): [(6,4),(2,2)],
    (6,4): [(8,5),(4,3)],   (8,5): [(7,3),(6,4)],
    (7,3): [(6,1),(8,5)],   (6,1): [(4,2),(7,3)],
    (4,2): [(6,3),(6,1)],   (6,3): [(7,5),(4,2)],
    (7,5): [(8,7),(6,3)],   (8,7): [(9,9),(7,5)],
    (9,9): [(10,7),(8,7)],  (10,7): [(9,5),(9,9)],
    (9,5): [(8,3),(10,7)],  (8,3): [(10,4),(9,5)],
    (10,4): [(9,2),(8,3)],  (9,2): [(7,1),(10,4)],
    (7,1): [(5,2),(9,2)],   (5,2): [(3,1),(7,1)],
    (3,1): [(1,2),(5,2)],   (1,2): [(2,4),(3,1)],
    (2,4): [(1,6),(1,2)],   (1,6): [(2,8),(2,4)],
    (2,8): [(1,10),(1,6)],  (1,10): [(3,9),(2,8)],
    (3,9): [(5,10),(1,10)], (5,10): [(7,9),(3,9)],
    (7,9): [(9,10),(5,10)], (9,10): [(10,8),(7,9)],
    (10,8): [(8,9),(9,10)], (8,9): [(10,10),(10,8)],
    (10,10): [(9,8),(8,9)], (9,8): [(10,6),(10,10)],
    (10,6): [(9,4),(9,8)],  (9,4): [(10,2),(10,6)],
    (10,2): [(8,1),(9,4)],  (8,1): [(9,3),(10,2)],
    (9,3): [(10,1),(8,1)],  (10,1): [(8,2),(9,3)],
    (8,2): [(10,3),(10,1)], (10,3): [(9,1),(8,2)],
    (9,1): [(7,2),(10,3)],  (7,2): [(5,1),(9,1)],
    (5,1): [(3,2),(7,2)],   (3,2): [(1,1),(5,1)]
}

######### 6x8 #########
##    # # # # # # # # 6
##    # # # + # # # # 5
##    # # # # # # # # 4
##    # # # # # # # # 3
##    # # # # # # # # 2
##    # # # # # # # # 1
##    1 2 3 4 5 6 7 8
##
##    Cell + is (4,5)

path6x8 = {
    (1,1): [(2,3),(3,2)], (2,3): [(3,5),(1,1)],
    (3,5): [(1,6),(2,3)], (1,6): [(2,4),(3,5)],
    (2,4): [(4,3),(1,6)], (4,3): [(3,1),(2,4)],
    (3,1): [(1,2),(4,3)], (1,2): [(3,3),(3,1)],
    (3,3): [(2,1),(1,2)], (2,1): [(1,3),(3,3)],
    (1,3): [(2,5),(2,1)], (2,5): [(4,6),(1,3)],
    (4,6): [(6,5),(2,5)], (6,5): [(8,6),(4,6)],
    (8,6): [(7,4),(6,5)], (7,4): [(8,2),(8,6)],
    (8,2): [(6,1),(7,4)], (6,1): [(4,2),(8,2)],
    (4,2): [(3,4),(6,1)], (3,4): [(1,5),(4,2)],
    (1,5): [(3,6),(3,4)], (3,6): [(5,5),(1,5)],
    (5,5): [(7,6),(3,6)], (7,6): [(8,4),(5,5)],
    (8,4): [(7,2),(7,6)], (7,2): [(5,1),(8,4)],
    (5,1): [(6,3),(7,2)], (6,3): [(7,1),(5,1)],
    (7,1): [(8,3),(6,3)], (8,3): [(7,5),(7,1)],
    (7,5): [(5,6),(8,3)], (5,6): [(4,4),(7,5)],
    (4,4): [(5,2),(5,6)], (5,2): [(7,3),(4,4)],
    (7,3): [(8,1),(5,2)], (8,1): [(6,2),(7,3)],
    (6,2): [(5,4),(8,1)], (5,4): [(6,6),(6,2)],
    (6,6): [(8,5),(5,4)], (8,5): [(6,4),(6,6)],
    (6,4): [(4,5),(8,5)], (4,5): [(2,6),(6,4)],
    (2,6): [(1,4),(4,5)], (1,4): [(2,2),(2,6)],
    (2,2): [(4,1),(1,4)], (4,1): [(5,3),(2,2)],
    (5,3): [(3,2),(4,1)], (3,2): [(1,1),(5,3)]
}

########## 8x6 ##########
## Transpose the 6x8 path
path8x6 = {}
for square in path6x8:
    newSquare = square[1], 8 - square[0] + 1
    path8x6[newSquare] = []
    for adjacentSquare in path6x8[square]:
        newAdjacentSquare = adjacentSquare[1], 8 - adjacentSquare[0] + 1
        path8x6[newSquare].append(newAdjacentSquare)

########### 8x10 ##########
##    # # # # # # # # # # 8
##    # # # # # # # # # # 7
##    # # # # + # # # # # 6
##    # # # # # # # # # # 5
##    # # # # # # # # # # 4
##    # # # # # # # # # # 3
##    # # # # # # # # # # 2
##    # # # # # # # # # # 1
##    1 2 3 4 5 6 7 8 9 10
##
##    Cell + is (5,6)

path8x10 = {
    (1,1): [(2,3),(3,2)],   (2,3): [(1,5),(1,1)],
    (1,5): [(2,7),(2,3)],   (2,7): [(4,8),(1,5)],
    (4,8): [(6,7),(2,7)],   (6,7): [(8,8),(4,8)],
    (8,8): [(10,7),(6,7)],  (10,7): [(9,5),(8,8)],
    (9,5): [(10,3),(10,7)], (10,3): [(9,1),(9,5)],
    (9,1): [(8,3),(10,3)],  (8,3): [(10,2),(9,1)],
    (10,2): [(8,1),(8,3)],  (8,1): [(6,2),(10,2)],
    (6,2): [(4,1),(8,1)],   (4,1): [(2,2),(6,2)],
    (2,2): [(1,4),(4,1)],   (1,4): [(2,6),(2,2)],
    (2,6): [(1,8),(1,4)],   (1,8): [(3,7),(2,6)],
    (3,7): [(5,8),(1,8)],   (5,8): [(7,7),(3,7)],
    (7,7): [(9,8),(5,8)],   (9,8): [(10,6),(7,7)],
    (10,6): [(8,7),(9,8)],  (8,7): [(10,8),(10,6)],
    (10,8): [(9,6),(8,7)],  (9,6): [(10,4),(10,8)],
    (10,4): [(9,2),(9,6)],  (9,2): [(7,1),(10,4)],
    (7,1): [(5,2),(9,2)],   (5,2): [(4,4),(7,1)],
    (4,4): [(6,5),(5,2)],   (6,5): [(7,3),(4,4)],
    (7,3): [(5,4),(6,5)],   (5,4): [(6,6),(7,3)],
    (6,6): [(8,5),(5,4)],   (8,5): [(6,4),(6,6)],
    (6,4): [(4,5),(8,5)],   (4,5): [(3,3),(6,4)],
    (3,3): [(2,5),(4,5)],   (2,5): [(4,6),(3,3)],
    (4,6): [(3,4),(2,5)],   (3,4): [(1,3),(4,6)],
    (1,3): [(2,1),(3,4)],   (2,1): [(4,2),(1,3)],
    (4,2): [(6,3),(2,1)],   (6,3): [(5,5),(4,2)],
    (5,5): [(7,6),(6,3)],   (7,6): [(8,4),(5,5)],
    (8,4): [(10,5),(7,6)],  (10,5): [(9,7),(8,4)],
    (9,7): [(7,8),(10,5)],  (7,8): [(5,7),(9,7)],
    (5,7): [(3,8),(7,8)],   (3,8): [(1,7),(5,7)],
    (1,7): [(3,6),(3,8)],   (3,6): [(2,4),(1,7)],
    (2,4): [(1,2),(3,6)],   (1,2): [(3,1),(2,4)],
    (3,1): [(4,3),(1,2)],   (4,3): [(3,5),(3,1)],
    (3,5): [(1,6),(4,3)],   (1,6): [(2,8),(3,5)],
    (2,8): [(4,7),(1,6)],   (4,7): [(6,8),(2,8)],
    (6,8): [(5,6),(4,7)],   (5,6): [(7,5),(6,8)],
    (7,5): [(9,4),(5,6)],   (9,4): [(8,6),(7,5)],
    (8,6): [(7,4),(9,4)],   (7,4): [(5,3),(8,6)],
    (5,3): [(6,1),(7,4)],   (6,1): [(8,2),(5,3)],
    (8,2): [(10,1),(6,1)],  (10,1): [(9,3),(8,2)],
    (9,3): [(7,2),(10,1)],  (7,2): [(5,1),(9,3)],
    (5,1): [(3,2),(7,2)],   (3,2): [(1,1),(5,1)],
}

########## 10x8 ##########
## Transpose the 8x10 path
path10x8 = {}
for square in path8x10:
    newSquare = square[1], 10 - square[0] + 1
    path10x8[newSquare] = []
    for adjacentSquare in path8x10[square]:
        newAdjacentSquare = adjacentSquare[1], 10 - adjacentSquare[0] + 1
        path10x8[newSquare].append(newAdjacentSquare)

################## 8x10 ###################
##    #  #  #  #  #  #  #  #  #  #  #  # 10
##    #  #  #  #  #  #  #  #  #  #  #  # 9
##    #  #  #  #  #  #  #  #  #  #  #  # 8
##    #  #  #  #  #  #  #  #  #  #  #  # 7
##    #  #  #  #  #  #  #  #  #  +  #  # 6
##    #  #  #  #  #  #  #  #  #  #  #  # 5
##    #  #  #  #  #  #  #  #  #  #  #  # 4
##    #  #  #  #  #  #  #  #  #  #  #  # 3
##    #  #  #  #  #  #  #  #  #  #  #  # 2
##    #  #  #  #  #  #  #  #  #  #  #  # 1
##    1  2  3  4  5  6  7  8  9 10 11 12
##
##    Cell + is (10,6)

path10x12 = {
    (1,1): [(2,3),(3,2)],     (2,3): [(3,1),(1,1)],
    (3,1): [(1,2),(2,3)],     (1,2): [(2,4),(3,1)],
    (2,4): [(1,6),(1,2)],     (1,6): [(3,5),(2,4)],
    (3,5): [(1,4),(1,6)],     (1,4): [(2,6),(3,5)],
    (2,6): [(3,8),(1,4)],     (3,8): [(1,7),(2,6)],
    (1,7): [(2,9),(3,8)],     (2,9): [(4,10),(1,7)],
    (4,10): [(6,9),(2,9)],    (6,9): [(8,10),(4,10)],
    (8,10): [(10,9),(6,9)],   (10,9): [(12,10),(8,10)],
    (12,10): [(11,8),(10,9)], (11,8): [(12,6),(12,10)],
    (12,6): [(11,4),(11,8)],  (11,4): [(12,2),(12,6)],
    (12,2): [(10,1),(11,4)],  (10,1): [(8,2),(12,2)],
    (8,2): [(6,1),(10,1)],    (6,1): [(4,2),(8,2)],
    (4,2): [(2,1),(6,1)],     (2,1): [(1,3),(4,2)],
    (1,3): [(3,4),(2,1)],     (3,4): [(1,5),(1,3)],
    (1,5): [(2,7),(3,4)],     (2,7): [(1,9),(1,5)],
    (1,9): [(3,10),(2,7)],    (3,10): [(2,8),(1,9)],
    (2,8): [(1,10),(3,10)],   (1,10): [(3,9),(2,8)],
    (3,9): [(1,8),(1,10)],    (1,8): [(2,10),(3,9)],
    (2,10): [(4,9),(1,8)],    (4,9): [(6,10),(2,10)],
    (6,10): [(8,9),(4,9)],    (8,9): [(10,10),(6,10)],
    (10,10): [(12,9),(8,9)],  (12,9): [(11,7),(10,10)],
    (11,7): [(12,5),(12,9)],  (12,5): [(11,3),(11,7)],
    (11,3): [(12,1),(12,5)],  (12,1): [(10,2),(11,3)],
    (10,2): [(8,1),(12,1)],   (8,1): [(6,2),(10,2)],
    (6,2): [(4,1),(8,1)],     (4,1): [(2,2),(6,2)],
    (2,2): [(4,3),(4,1)],     (4,3): [(5,5),(2,2)],
    (5,5): [(7,4),(4,3)],     (7,4): [(5,3),(5,5)],
    (5,3): [(6,5),(7,4)],     (6,5): [(8,6),(5,3)],
    (8,6): [(7,8),(6,5)],     (7,8): [(6,6),(8,6)],
    (6,6): [(8,7),(7,8)],     (8,7): [(9,9),(6,6)],
    (9,9): [(10,7),(8,7)],    (10,7): [(9,5),(9,9)],
    (9,5): [(10,3),(10,7)],   (10,3): [(8,4),(9,5)],
    (8,4): [(9,6),(10,3)],    (9,6): [(11,5),(8,4)],
    (11,5): [(9,4),(9,6)],    (9,4): [(7,3),(11,5)],
    (7,3): [(8,5),(9,4)],     (8,5): [(10,6),(7,3)],
    (10,6): [(9,8),(8,5)],    (9,8): [(7,7),(10,6)],
    (7,7): [(5,8),(9,8)],     (5,8): [(7,9),(7,7)],
    (7,9): [(6,7),(5,8)],     (6,7): [(4,6),(7,9)],
    (4,6): [(5,4),(6,7)],     (5,4): [(7,5),(4,6)],
    (7,5): [(5,6),(5,4)],     (5,6): [(3,7),(7,5)],
    (3,7): [(4,5),(5,6)],     (4,5): [(3,3),(3,7)],
    (3,3): [(2,5),(4,5)],     (2,5): [(4,4),(3,3)],
    (4,4): [(5,2),(2,5)],     (5,2): [(6,4),(4,4)],
    (6,4): [(8,3),(5,2)],     (8,3): [(9,1),(6,4)],
    (9,1): [(7,2),(8,3)],     (7,2): [(9,3),(9,1)],
    (9,3): [(10,5),(7,2)],    (10,5): [(9,7),(9,3)],
    (9,7): [(7,6),(10,5)],    (7,6): [(5,7),(9,7)],
    (5,7): [(3,6),(7,6)],     (3,6): [(4,8),(5,7)],
    (4,8): [(5,10),(3,6)],    (5,10): [(6,8),(4,8)],
    (6,8): [(4,7),(5,10)],    (4,7): [(5,9),(6,8)],
    (5,9): [(7,10),(4,7)],    (7,10): [(8,8),(5,9)],
    (8,8): [(9,10),(7,10)],   (9,10): [(11,9),(8,8)],
    (11,9): [(12,7),(9,10)],  (12,7): [(10,8),(11,9)],
    (10,8): [(11,10),(12,7)], (11,10): [(12,8),(10,8)],
    (12,8): [(11,6),(11,10)], (11,6): [(12,4),(12,8)],
    (12,4): [(11,2),(11,6)],  (11,2): [(10,4),(12,4)],
    (10,4): [(12,3),(11,2)],  (12,3): [(11,1),(10,4)],
    (11,1): [(9,2),(12,3)],   (9,2): [(7,1),(11,1)],
    (7,1): [(6,3),(9,2)],     (6,3): [(5,1),(7,1)],
    (5,1): [(3,2),(6,3)],     (3,2): [(1,1),(5,1)]
}

########## 12x10 ##########
## Transpose the 10x12 path
path12x10 = {}
for square in path10x12:
    newSquare = square[1], 12 - square[0] + 1
    path12x10[newSquare] = []
    for adjacentSquare in path10x12[square]:
        newAdjacentSquare = adjacentSquare[1], 12 - adjacentSquare[0] + 1
        path12x10[newSquare].append(newAdjacentSquare)

## Splits a chessboard side according to the algorithm
def SplitSide(side):
    if side / 4 == floor(side / 4):
        k = side / 4
        lowerSide = 2*k
        upperSide = 2*k
    elif (side - 2) / 4 == floor((side - 2) / 4):
        k = (side - 2) / 4
        lowerSide = 2*k
        upperSide = 2*(k+1)
    else:
        print("ERROR: Failed to split", side, "in two parts.")
        return -1, -1

    if lowerSide + upperSide != side:
        print("ERROR: split sides", lowerSide, "and", upperSide, "fail to sum to", side, ".")
        return -2, -2

    return int(lowerSide), int(upperSide)

class Chessboard:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.knightAdjacencyList = {}
        self.knightTour = {}

    def SetAdjacencyList(self, knightAdjacencyList):
        self.knightAdjacencyList = knightAdjacencyList.copy()

    def GetAdjacencyList(self):
        return self.knightAdjacencyList.copy()

    def SetTour(self, tour):
        self.knightTour = tour.copy()

    def GetTour(self):
        return self.knightTour.copy()

    def GetRows(self):
        return self.rows

    def GetColumns(self):
        return self.columns

    def FindAdjacencyList(self):
        nRows = self.GetRows()
        nColumns = self.GetColumns()

        if (nRows == 6) and (nColumns == 6):
            self.SetAdjacencyList(path6x6)
            return

        if (nRows == 8) and (nColumns == 8):
            self.SetAdjacencyList(path8x8)
            return

        if (nRows == 10) and (nColumns == 10):
            self.SetAdjacencyList(path10x10)
            return

        if (nRows == 6) and (nColumns == 8):
            self.SetAdjacencyList(path6x8)
            return

        if (nRows == 8) and (nColumns == 6):
            self.SetAdjacencyList(path8x6)
            return

        if (nRows == 8) and (nColumns == 10):
            self.SetAdjacencyList(path8x10)
            return

        if (nRows == 10) and (nColumns == 8):
            self.SetAdjacencyList(path10x8)
            return

        if (nRows == 10) and (nColumns == 12):
            self.SetAdjacencyList(path10x12)
            return

        if (nRows == 12) and (nColumns == 10):
            self.SetAdjacencyList(path12x10)
            return

        bottomRows, topRows = SplitSide(nRows)
        leftColumns, rightColumns = SplitSide(nColumns)

        topLeftBoard = Chessboard(topRows, leftColumns)
        topRightBoard = Chessboard(topRows, rightColumns)
        bottomLeftBoard = Chessboard(bottomRows, leftColumns)
        bottomRightBoard = Chessboard(bottomRows, rightColumns)

        topLeftBoard.FindAdjacencyList()
        topRightBoard.FindAdjacencyList()
        bottomLeftBoard.FindAdjacencyList()
        bottomRightBoard.FindAdjacencyList()

        ## Build new adjacency list from bottom left, makes sense for coordinates
        bottomLeftADL = bottomLeftBoard.GetAdjacencyList()
        bottomRightADL = bottomRightBoard.GetAdjacencyList()
        topLeftADL = topLeftBoard.GetAdjacencyList()
        topRightADL = topRightBoard.GetAdjacencyList()

        newBottomLeftADL = {}
        newBottomRightADL = {}
        newTopLeftADL = {}
        newTopRightADL = {}

        for position in bottomLeftADL:
            newBottomLeftADL[position] = []
            for adjacentSquare in bottomLeftADL[position]:
                newBottomLeftADL[position].append(adjacentSquare)

        for position in bottomRightADL:
            ## Add columns of bottom-left to column indexes of bottom-right
            newPosition = tuple(map(lambda i, j: int(i + j), position, (bottomLeftBoard.GetColumns(), 0)))
            newBottomRightADL[newPosition] = []
            for adjacentSquare in bottomRightADL[position]:
                ## Add columns of bottom-left to column indexes of bottom-right
                newAdjacentSquare = tuple(map(lambda i, j: int(i + j), adjacentSquare, (bottomLeftBoard.GetColumns(), 0)))
                newBottomRightADL[newPosition].append(newAdjacentSquare)

        for position in topLeftADL:
            ## Add rows of bottom-left to row indexes of top-left
            newPosition = tuple(map(lambda i, j: int(i + j), position, (0, bottomLeftBoard.GetRows())))
            newTopLeftADL[newPosition] = []
            for adjacentSquare in topLeftADL[position]:
                ## Add rows of bottom-left to row indexes of top-left
                newAdjacentSquare = tuple(map(lambda i, j: int(i + j), adjacentSquare, (0, bottomLeftBoard.GetRows())))
                newTopLeftADL[newPosition].append(newAdjacentSquare)

        for position in topRightADL:
            ## Add rows & columns to top-right
            newPosition = tuple(map(lambda i, j: int(i + j), position, (bottomLeftBoard.GetColumns(), bottomLeftBoard.GetRows())))
            newTopRightADL[newPosition] = []
            for adjacentSquare in topRightADL[position]:
                ## Add rows & columns to top-right
                newAdjacentSquare = tuple(map(lambda i, j: int(i + j), adjacentSquare, (bottomLeftBoard.GetColumns(), bottomLeftBoard.GetRows())))
                newTopRightADL[newPosition].append(newAdjacentSquare)

        ### Fix the edges
        ## Relevant squares
        #A1 = (4,7)
        #A2 = (6,8)
        #B1 = (7,7)
        #B2 = (8,9)
        #C1 = (7,5)
        #C2 = (9,6)
        #D1 = (5,4)
        #D2 = (6,6)
        A1 = (bottomLeftBoard.GetColumns()-2, bottomLeftBoard.GetRows()+1)
        A2 = (bottomLeftBoard.GetColumns(),   bottomLeftBoard.GetRows()+2)
        B1 = (bottomLeftBoard.GetColumns()+1, bottomLeftBoard.GetRows()+1)
        B2 = (bottomLeftBoard.GetColumns()+2, bottomLeftBoard.GetRows()+3)
        C1 = (bottomLeftBoard.GetColumns()+1, bottomLeftBoard.GetRows()-1)
        C2 = (bottomLeftBoard.GetColumns()+3, bottomLeftBoard.GetRows()  )
        D1 = (bottomLeftBoard.GetColumns()-1, bottomLeftBoard.GetRows()-2)
        D2 = (bottomLeftBoard.GetColumns(),   bottomLeftBoard.GetRows()  )
        ## Pop edge A
        newTopLeftADL[A1].remove(A2)
        newTopLeftADL[A2].remove(A1)
        ## Pop edge B
        newTopRightADL[B1].remove(B2)
        newTopRightADL[B2].remove(B1)
        ## Pop edge C
        newBottomRightADL[C1].remove(C2)
        newBottomRightADL[C2].remove(C1)
        ## Pop edge D
        newBottomLeftADL[D1].remove(D2)
        newBottomLeftADL[D2].remove(D1)
        ## Add edge E
        newBottomLeftADL[D2].append(A1)
        newTopLeftADL[A1].append(D2)
        ## Add edge F
        newTopLeftADL[A2].append(B2)
        newTopRightADL[B2].append(A2)
        ## Add edge G
        newTopRightADL[B1].append(C2)
        newBottomRightADL[C2].append(B1)
        ## Add edge H
        newBottomRightADL[C1].append(D1)
        newBottomLeftADL[D1].append(C1)

        newCompleteADL = {**newBottomLeftADL, **newBottomRightADL, **newTopLeftADL, **newTopRightADL}
        self.SetAdjacencyList(newCompleteADL)
        return

    ## Given a path adjacency list, develop (heh) a direct tour of the board
    def FindTour(self):
        startingPosition = (1,1)
        currentPosition = startingPosition
        adjacencyList = self.GetAdjacencyList()
        visitedSquares = {startingPosition: True}
        tour = {}

        while True:
            foundNextStep = False

            for square in adjacencyList[currentPosition]:
                if square not in visitedSquares:
                    visitedSquares[square] = True
                    tour[currentPosition] = square
                    currentPosition = square
                    foundNextStep = True
                    break

            ## If all adjacent squares have already been visited...
            if not foundNextStep:
                ## ... either we're at the last step...
                if tuple(map(lambda i,j: i - j, currentPosition, startingPosition)) in allowedOffsetMoves:
                    tour[currentPosition] = startingPosition
                    break
                ## ... or the tour is broken.
                else:
                    print("ERROR: position", currentPosition, "can't go anywhere.")
                    break

        if len(visitedSquares) != (self.GetRows() * self.GetColumns()):
            print("Ah-le-le?! The tour ends after", len(visitedSquares), "steps instead of", self.GetRows() * self.GetColumns() ,".")

        self.SetTour(tour)

    ## Print tour matrix. Number of each square is the step when the knight visits it
    def PrintTour(self):
        nextStep = self.GetTour()
        startingPosition = (1,1)
        currentPosition = nextStep[startingPosition]

        tourMatrix = np.zeros((self.GetRows(),self.GetColumns()),int)

        visitedPositions = {startingPosition: 1}
        tourMatrix[self.GetRows()-startingPosition[1],startingPosition[0]-1] = 1
        positionCounter = 1

        while currentPosition !=  startingPosition:
            if currentPosition in visitedPositions:
                print("ERROR: square", currentPosition, "is repeating.")
                print("Visited at steps", visitedPositions[currentPosition], "and", positionCounter,".")
                break

            positionCounter += 1
            visitedPositions[currentPosition] = positionCounter
            tourMatrix[int(self.GetRows()-currentPosition[1]),int(currentPosition[0]-1)] = positionCounter
            currentPosition = nextStep[currentPosition]

        if len(visitedPositions) != self.GetRows() * self.GetColumns():
            print("ERROR: ", len(visitedPositions), "visited squares, but", self.GetRows()*self.GetColumns(), "squares on the board.")

        print(tourMatrix)

    ## Is the tour structured (look it up)?
    def TourIsStructured(self):
        adjacencyList = self.GetAdjacencyList()
        columns = self.GetColumns()
        rows = self.GetRows()

        condBL1 = ((1,3) in adjacencyList[(2,1)])
        condBL2 = ((1,2) in adjacencyList[(3,1)])
        condTL1 = ((1,rows-1) in adjacencyList[(3,rows)])
        condTL2 = ((1,rows-2) in adjacencyList[(2,rows)])
        condTR1 = ((columns-2,rows) in adjacencyList[(columns,rows-1)])
        condTR2 = ((columns-1,rows) in adjacencyList[(columns,rows-2)])
        condBR1 = ((columns-2,1) in adjacencyList[(columns,2)])
        condBR2 = ((columns-1,1) in adjacencyList[(columns,3)])

        return (condBL1 and condBL2 and condTL1 and condTL2 and condTR1 and condTR2 and condBR1 and condBR2)

    ## Is the tour the right length?
    def TourIsComplete(self):
        return len(self.GetTour()) == self.GetColumns() * self.GetRows()

    ## Does the tour end where it started?
    def TourIsClosed(self):
        startingPosition = (1,1)
        currentPosition = startingPosition
        tourNextStep = self.GetTour()

        for i in range(self.GetColumns() * self.GetRows()):
            currentPosition = tourNextStep[currentPosition]

        return currentPosition == startingPosition

    ## Is every square in the tour unique?
    def TourIsNonRepeating(self):
        startingPosition = (1,1)
        currentPosition = startingPosition
        tourNextStep = self.GetTour()

        ## Skip first position because it's also the last
        visitedPositions = {}
        isNonRepeating = True

        for i in range(self.GetColumns() * self.GetRows()):
            currentPosition = tourNextStep[currentPosition]
            if currentPosition in visitedPositions:
                isNonRepeating = False
                break

        return isNonRepeating

    ## Can each move in the tour be performed by a knight?
    def TourIsLegal(self):
        tourNextStep = self.GetTour()
        previousPosition = (1,1)
        currentPosition = tourNextStep[previousPosition]


        ## Skip first position because it's also the last
        isLegal = True

        for i in range(self.GetColumns() * self.GetRows()):
            if tuple(map(lambda i,j: i - j, currentPosition, previousPosition)) not in allowedOffsetMoves:
                isLegal = False
                break

            previousPosition = currentPosition
            currentPosition = tourNextStep[currentPosition]

        return isLegal

    def DebugTour(self):
        print("Complete: \t", self.TourIsComplete())
        print("Closed: \t", self.TourIsClosed())
        print("Structured: \t", self.TourIsStructured())
        print("Non-repeating: \t", self.TourIsNonRepeating())
        print("Legal: \t\t", self.TourIsLegal())

n = 200
board = Chessboard(n,n)

print(board.GetRows())
print(board.GetColumns())

print("Building knight adjacency list...")
board.FindAdjacencyList()
print("Building knight tour...")
board.FindTour()
#print((board.GetTour()))
print()
board.PrintTour()

print("ADL length:", len(board.GetAdjacencyList()))
print("Tot. squares:", board.GetColumns() * board.GetRows())

board.DebugTour()
