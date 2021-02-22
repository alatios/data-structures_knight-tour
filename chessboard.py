#!/usr/bin/env python3

import numpy as np
from math import floor
from knowntours import *

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

    ## Bog-standard constructor and get/set methods, nothing to see here.
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

    ## Finds a closed&structured knight tour through the divide-and-conquer
    ## algorith. Tour is stored as an undirected graph using an adjacency
    ## lists data structure (a Python dictionary).
    def FindAdjacencyList(self):
        nRows = self.GetRows()
        nColumns = self.GetColumns()

        ## Base of recursion: the six known tours.
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

        ## Split the chessboard according to the algorithm
        bottomRows, topRows = SplitSide(nRows)
        leftColumns, rightColumns = SplitSide(nColumns)

        topLeftBoard = Chessboard(topRows, leftColumns)
        topRightBoard = Chessboard(topRows, rightColumns)
        bottomLeftBoard = Chessboard(bottomRows, leftColumns)
        bottomRightBoard = Chessboard(bottomRows, rightColumns)

        ## The divide-and-conquer approach does its magic
        topLeftBoard.FindAdjacencyList()
        topRightBoard.FindAdjacencyList()
        bottomLeftBoard.FindAdjacencyList()
        bottomRightBoard.FindAdjacencyList()

        ## Now to build the complete path from these four
        ## First we save the adjacency lists we just found
        bottomLeftADL = bottomLeftBoard.GetAdjacencyList()
        bottomRightADL = bottomRightBoard.GetAdjacencyList()
        topLeftADL = topLeftBoard.GetAdjacencyList()
        topRightADL = topRightBoard.GetAdjacencyList()

        ## Why do we need four new ones? Because we need to change the coordinates
        newBottomLeftADL = {}
        newBottomRightADL = {}
        newTopLeftADL = {}
        newTopRightADL = {}

        ## Since we're using coordinates based on chess algebraic notation,
        ## it only makes sense to start from bottom left (i.e. (1,1))
        for position in bottomLeftADL:
            newBottomLeftADL[position] = []
            for adjacentSquare in bottomLeftADL[position]:
                newBottomLeftADL[position].append(adjacentSquare)

        ## For the other three, just add the appropriate offsets

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

        ### Fix the edges as prescribed by the algorithm
        ## Relevant squares
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

        ## Join the four ADLs and job's done for the day
        newCompleteADL = {**newBottomLeftADL, **newBottomRightADL, **newTopLeftADL, **newTopRightADL}
        self.SetAdjacencyList(newCompleteADL)
        return

    ## Given a path adjacency list, develop (heh) a direct tour of the board
    ## Reminder: paths are undirected, tours are directed
    def FindTour(self):
        ## Start at bottom left. Conventional, any starting point will do
        startingPosition = (1,1)
        currentPosition = startingPosition
        adjacencyList = self.GetAdjacencyList()

        ## Visited squares dictionary
        visitedSquares = {startingPosition: True}
        tour = {}

        while True:
            foundNextStep = False

            ## Each position has two squares it can reach in a path (forward/backward)
            ## Pick the first non-visited one, assuming one exists
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

        ## Just a simple check to warn us if the tour ended too soon.
        ## Either something went wrong when connecting the sub-paths
        ## or the programmer made a major screw-up. What a loser!
        if len(visitedSquares) != (self.GetRows() * self.GetColumns()):
            print("Ah-le-le?! The tour ends after", len(visitedSquares), "steps instead of", self.GetRows() * self.GetColumns() ,".")

        self.SetTour(tour)

    ## Print tour matrix. Number of each square is the step in which the knight visits it
    def PrintTour(self):
        nextStep = self.GetTour()
        ## Starting position is arbitrary
        startingPosition = (1,1)
        currentPosition = nextStep[startingPosition]

        ## Fill a matrix with zeros
        tourMatrix = np.zeros((self.GetRows(),self.GetColumns()),int)

        ## Dictionary of steps
        visitedPositions = {startingPosition: 1}

        ## Fill the first step in the matrix
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

    ## Combine all previous checks for quick reference
    def DebugTour(self):
        print("Complete: \t", self.TourIsComplete())
        print("Closed: \t", self.TourIsClosed())
        print("Structured: \t", self.TourIsStructured())
        print("Non-repeating: \t", self.TourIsNonRepeating())
        print("Legal: \t\t", self.TourIsLegal())
