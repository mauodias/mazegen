#!/usr/bin/env python

import sys
import os

import draw
import maze

def run(rows=40, cols=40, cell_size=10, initial_x=0, initial_y=0, final_x=20, final_y=39):
    drawer = draw.Drawer('temp.svg')
    m = maze.Maze(rows, cols, cell_size, drawer)
    m.generate(initial_x, initial_y, final_x, final_y)
    out = m.draw()
    return out

def entry(request):
    svg = run()
    return svg

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(run())
    elif len(sys.argv) == 9:
        rows = sys.argv[1]
        cols = sys.argv[2]
        cell_size = sys.argv[3]
        initial_x = sys.argv[4]
        initial_y = sys.argv[5]
        final_x = sys.argv[6]
        final_y = sys.argv[7]
        run()
    else:
        print('Incorrect parameters')
