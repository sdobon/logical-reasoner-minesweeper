"""A command line version of Minesweeper"""
import random
import re
import time
from string import ascii_lowercase

import read, copy
from logical_classes import *
from KB_IE import KnowledgeBase

KB = KnowledgeBase([], [])

_, rule1 = read.parse_input("rule: ((bomb_count 1 ?a) (adjacent ?b ?a) (bomb ?b)) -> (mark_rest_safe ?a)")

_, rule2 = read.parse_input("rule: ((mark_rest_safe ?a) (adjacent ?b ?a) (unvisited ?b)) -> (safe ?b)")

KB.kb_assert(rule1)
KB.kb_assert(rule2)

def setupgrid(gridsize, start, numberofmines):
    emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]

    mines = getmines(emptygrid, start, numberofmines)

    for i, j in mines:
        emptygrid[i][j] = 'X'

    grid = getnumbers(emptygrid)

    return (grid, mines)


def showgrid(grid):
    gridsize = len(grid)

    horizontal = '   ' + (4 * gridsize * '-') + '-'

    # Print top column letters
    toplabel = '     '

    for i in ascii_lowercase[:gridsize]:
        toplabel = toplabel + i + '   '

    print(toplabel + '\n' + horizontal)

    # Print left row numbers
    for idx, i in enumerate(grid):
        row = '{0:2} |'.format(idx + 1)

        for j in i:
            row = row + ' ' + j + ' |'

        print(row + '\n' + horizontal)

    print('')


def getrandomcell(grid):
    gridsize = len(grid)

    a = random.randint(0, gridsize - 1)
    b = random.randint(0, gridsize - 1)

    return (a, b)


def getneighbors(grid, rowno, colno):
    gridsize = len(grid)
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                neighbors.append((rowno + i, colno + j))

    return neighbors


def getmines(grid, start, numberofmines):
    mines = []
    neighbors = getneighbors(grid, *start)

    for i in range(numberofmines):
        cell = getrandomcell(grid)
        while cell == start or cell in mines or cell in neighbors:
            cell = getrandomcell(grid)
        mines.append(cell)

    return mines


def getnumbers(grid):
    for rowno, row in enumerate(grid):
        for colno, cell in enumerate(row):
            if cell != 'X':
                # Gets the values of the neighbors
                values = [grid[r][c] for r, c in getneighbors(grid,
                                                              rowno, colno)]

                # Counts how many are mines
                grid[rowno][colno] = str(values.count('X'))

    return grid


def showcells(grid, currgrid, rowno, colno):
    # Exit function if the cell was already shown
    if currgrid[rowno][colno] != ' ':
        return

    # Show current cell
    currgrid[rowno][colno] = grid[rowno][colno]

    # Get the neighbors if the cell is empty
    if grid[rowno][colno] == '0':
        for r, c in getneighbors(grid, rowno, colno):
            # Repeat function for each neighbor that doesn't have a flag
            if currgrid[r][c] != 'F':
                showcells(grid, currgrid, r, c)


def playagain():
    choice = input('Play again? (y/n): ')

    return choice.lower() == 'y'


def parseinput(inputstring, gridsize, helpmessage):
    cell = ()
    flag = False
    message = "Invalid cell. " + helpmessage

    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridsize - 1])
    validinput = re.match(pattern, inputstring)

    if inputstring == 'help':
        message = helpmessage

    elif validinput:
        rowno = int(validinput.group(2)) - 1
        colno = ascii_lowercase.index(validinput.group(1))
        flag = bool(validinput.group(3))

        if -1 < rowno < gridsize:
            cell = (rowno, colno)
            message = ''

    return {'cell': cell, 'flag': flag, 'message': message}


def look_at_board(gridsize, currgrid):
    for i in range(gridsize):
        for j in range(gridsize):
            cell_str = str(i) + '_' + str(j)

            if currgrid[i][j] != ' ':
                _, unvisited = read.parse_input("fact: (unvisited " + cell_str + ")")
                KB.kb_retract(unvisited)

            try:
                num = int(currgrid[i][j])
                _, count_fact = read.parse_input("fact: (bomb_count " + str(num) + ' ' + cell_str + ")")
                KB.kb_assert(count_fact)
                # print(KB.facts)

            except ValueError:
                pass


def decide_next_move(gridsize, currgrid):
    for i in range(gridsize):
        for j in range(gridsize):
            if currgrid[i][j] == ' ':
                cell_str = str(i) + '_' + str(j)
                _, ask_safe = read.parse_input("fact: (safe " + cell_str + ")")
                if KB.kb_ask(ask_safe):
                    return {'cell': (i,j), 'flag': False, 'message': ''}

                _, ask_bomb = read.parse_input("fact: (bomb " + cell_str + ")")
                if KB.kb_ask(ask_bomb):
                    return {'cell': (i,j), 'flag': True, 'message': ''}
    print("guessing...")
    return {'cell': getrandomcell(currgrid), 'flag': False, 'message': ''}


def setup_facts(currgrid):
    gridsize = len(currgrid)
    for i in range(gridsize):
        for j in range(gridsize):
            cell_str = str(i) + '_' + str(j)
            _, mark_unvisited = read.parse_input("fact: (unvisited " + cell_str + ")")
            KB.kb_assert(mark_unvisited)
            neighbors = getneighbors(currgrid, i, j)
            for n in neighbors:
                cell_str_2 = str(n[0]) + '_' + str(n[1])
                _, adj = read.parse_input("fact: (adjacent " + cell_str_2 + ' ' + cell_str + ")")
                KB.kb_assert(adj)


def playgame():
    gridsize = 9
    numberofmines = 10

    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

    setup_facts(currgrid)

    grid = []
    flags = []
    starttime = 0

    helpmessage = ("Type the column followed by the row (eg. a5). "
                   "To put or remove a flag, add 'f' to the cell (eg. a5f).")

    showgrid(currgrid)
    print(helpmessage + " Type 'help' to show this message again.\n")

    while True:
        minesleft = numberofmines - len(flags)
        # prompt = input('Enter the cell ({} mines left): '.format(minesleft))
        # result = parseinput(prompt, gridsize, helpmessage + '\n')
        _ = input('advance?')
        look_at_board(gridsize, currgrid)
        result = decide_next_move(gridsize, currgrid)


        message = result['message']
        cell = result['cell']

        if cell:
            print('\n\n')
            rowno, colno = cell
            currcell = currgrid[rowno][colno]
            flag = result['flag']

            if not grid:
                grid, mines = setupgrid(gridsize, cell, numberofmines)
            if not starttime:
                starttime = time.time()

            if flag:
                # Add a flag if the cell is empty
                if currcell == ' ':
                    currgrid[rowno][colno] = 'F'
                    flags.append(cell)
                # Remove the flag if there is one
                elif currcell == 'F':
                    currgrid[rowno][colno] = ' '
                    flags.remove(cell)
                else:
                    message = 'Cannot put a flag there'

            # If there is a flag there, show a message
            elif cell in flags:
                message = 'There is a flag there'

            elif grid[rowno][colno] == 'X':
                print('Game Over\n')
                showgrid(grid)
                if playagain():
                    playgame()
                return

            elif currcell == ' ':
                showcells(grid, currgrid, rowno, colno)

            else:
                message = "That cell is already shown"

            if set(flags) == set(mines):
                minutes, seconds = divmod(int(time.time() - starttime), 60)
                print(
                    'You Win. '
                    'It took you {} minutes and {} seconds.\n'.format(minutes,
                                                                      seconds))
                showgrid(grid)
                if playagain():
                    playgame()
                return

        showgrid(currgrid)
        print(message)

playgame()
