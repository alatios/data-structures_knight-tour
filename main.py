#!/usr/bin/env python3

import chessboard as cb
import time
import sys

## Pass chessboard side as argument
n = int(sys.argv[1])
board = cb.Chessboard(n,n)

print("Rows:", board.GetRows())
print("Columns:", board.GetColumns())

print("Building knight adjacency list...")

## Start the clock
tick = time.perf_counter()

board.FindAdjacencyList()
print("Building knight tour...")
board.FindTour()

## Stop the clock
tock = time.perf_counter()

#print((board.GetTour()))
## This prints the tour. The only time it's useful is to ascertain
## at a glance that the script simply did not work. And we hope to
## have other systems in place to establish that, so it's really
## just for show.
print()
board.PrintTour()
print()

## Just a quick check that we got all squares. The debug feature does
## the same check, but this is more obvious.
print("ADL length:", len(board.GetAdjacencyList()))
print("Tot. squares:", board.GetColumns() * board.GetRows())

## See documentation of Chessboard class.
## In short: tells us if the script has screwed up.
board.DebugTour()

## Print elapsed time (in seconds) to find the tour.
print(f"Path found in {tock - tick:0.4f} seconds.")
