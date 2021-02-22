#!/usr/bin/env python3

import chessboard as cb
import time
import sys

n = int(sys.argv[1])
board = cb.Chessboard(n,n)

print("Rows:", board.GetRows())
print("Columns:", board.GetColumns())

print("Building knight adjacency list...")

tick = time.perf_counter()
board.FindAdjacencyList()
print("Building knight tour...")
board.FindTour()
tock = time.perf_counter()

#print((board.GetTour()))
print()
board.PrintTour()
print()

print("ADL length:", len(board.GetAdjacencyList()))
print("Tot. squares:", board.GetColumns() * board.GetRows())

board.DebugTour()

print(f"Path found in {tock - tick:0.4f} seconds.")
