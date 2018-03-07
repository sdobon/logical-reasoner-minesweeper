"""A command line version of Minesweeper"""
import random
import re
import time
from string import ascii_lowercase

import read, copy
from logical_classes import *
from KB_IE import KnowledgeBase

KB = KnowledgeBase([], [])

non_equivalence = "(not_equal ?a ?b) (not_equal ?a ?c) (not_equal ?a ?d) (not_equal ?a ?e) (not_equal ?a ?f) (not_equal ?a ?g) (not_equal ?a ?h) (not_equal ?a ?i) (not_equal ?b ?a) (not_equal ?b ?c) (not_equal ?b ?d) (not_equal ?b ?e) (not_equal ?b ?f) (not_equal ?b ?g) (not_equal ?b ?h) (not_equal ?b ?i) (not_equal ?c ?a) (not_equal ?c ?b) (not_equal ?c ?d) (not_equal ?c ?e) (not_equal ?c ?f) (not_equal ?c ?g) (not_equal ?c ?h) (not_equal ?c ?i) (not_equal ?d ?a) (not_equal ?d ?b) (not_equal ?d ?c) (not_equal ?d ?e) (not_equal ?d ?f) (not_equal ?d ?g) (not_equal ?d ?h) (not_equal ?d ?i) (not_equal ?e ?a) (not_equal ?e ?b) (not_equal ?e ?c) (not_equal ?e ?d) (not_equal ?e ?f) (not_equal ?e ?g) (not_equal ?e ?h) (not_equal ?e ?i) (not_equal ?f ?a) (not_equal ?f ?b) (not_equal ?f ?c) (not_equal ?f ?d) (not_equal ?f ?e) (not_equal ?f ?g) (not_equal ?f ?h) (not_equal ?f ?i) (not_equal ?g ?a) (not_equal ?g ?b) (not_equal ?g ?c) (not_equal ?g ?d) (not_equal ?g ?e) (not_equal ?g ?f) (not_equa ?g ?h) (not_equal ?g ?i) (not_equal ?h ?a) (not_equal ?h ?b) (not_equal ?h ?c) (not_equal ?h ?d) (not_equal ?h ?e) (not_equal ?h ?f) (not_equal ?h ?g) (not_equal ?h ?i) (not_equal ?i ?a) (not_equal ?i ?b) (not_equal ?i ?c) (not_equal ?i ?d) (not_equal ?i ?e) (not_equal ?i ?f) (not_equal ?i ?g) (not_equal ?i ?h)"


_, rule1 = read.parse_input("rule: ((bomb_count 1 ?a) (adjacent ?b ?a) (bomb ?b)) -> (mark_rest_safe ?a)")
_, rule2 = read.parse_input("rule: ((mark_rest_safe ?a) (adjacent ?b ?a) (unvisited ?b)) -> (safe ?b)")

_, rule3 = read.parse_input("rule: ((bomb_count 1 ?a) (adjacent ?b ?a) (not_safe ?b) (adjacent ?c ?a) (safe ?c) (adjacent ?d ?a) (safe ?d) (adjacent ?e ?a) (safe ?e) (adjacent ?f ?a) (safe ?f) (adjacent ?g ?a) (safe ?g) (adjacent ?h ?a) (safe ?h) (adjacent ?i ?a) (safe ?i) " + non_equivalence + ") -> (mark_rest_bombs ?a)")
_, rule4 = read.parse_input("rule: ((mark_rest_bombs ?a) (adjacent ?b ?a) (unvisited ?b)) -> (bomb ?b)")

# _, rulea = read.parse_input("rule: (    (adjacent ?b ?a)) -> (not_equal ?b ?a)")
# _, ruleb = read.parse_input("rule: ((not_equal ?b ?a) (not_equal ?c ?a)) -> (not_equal ?b ?c)")
# _, rulec = read.parse_input("rule: ((not_equal ?b ?a) (not_equal ?c ?a)) -> (not_equal ?c ?b)")


KB.kb_assert(rule1)
KB.kb_assert(rule2)
KB.kb_assert(rule3)
KB.kb_assert(rule4)

# KB.kb_assert(rulea)
# KB.kb_assert(ruleb)
# KB.kb_assert(rulec)

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


def getneighbors_imaginary(grid, rowno, colno):
    gridsize = len(grid)
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                neighbors.append([(rowno + i, colno + j), False])
            else:
                neighbors.append([(rowno + i, colno + j), "imaginary"])

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

                _, not_safe = read.parse_input("fact: (not_safe " + cell_str + ")")
                KB.kb_retract(not_safe)

            except ValueError:
                pass

    for i in range(gridsize):
        for j in range(gridsize):
            cell_str = str(i) + '_' + str(j)

            try:
                num = int(currgrid[i][j])
                _, count_fact = read.parse_input("fact: (bomb_count " + str(num) + ' ' + cell_str + ")")
                KB.kb_assert(count_fact)

            except ValueError:
                pass


def decide_next_move(gridsize, currgrid):
    for i in range(gridsize):
        for j in range(gridsize):
            if currgrid[i][j] == ' ':
                cell_str = str(i) + '_' + str(j)
                _, ask_safe = read.parse_input("fact: (safe " + cell_str + ")")
                if KB.kb_ask(ask_safe):
                    print("marking safe " + str([i,j]))
                    return {'cell': (i,j), 'flag': False, 'message': ''}

                _, ask_bomb = read.parse_input("fact: (bomb " + cell_str + ")")
                if KB.kb_ask(ask_bomb):
                    print("marking bomb " + str([i,j]))
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

            _, not_safe = read.parse_input("fact: (not_safe " + cell_str + ")")
            KB.kb_assert(not_safe)

            neighbors = getneighbors_imaginary(currgrid, i, j)
            #adjacency
            for n in neighbors:
                cell_str_2 = str(n[0][0]) + '_' + str(n[0][1])
                _, adj = read.parse_input("fact: (adjacent " + cell_str_2 + ' ' + cell_str + ")")
                KB.kb_assert(adj)
                if n[1] == "imaginary":
                    _, safe = read.parse_input("fact: (safe " + cell_str_2 + ")")
                    KB.kb_assert(safe)

            #non equivalence
            for x in range(gridsize):
                for y in range(gridsize):
                    cell_str_3 = str(x) + '_' + str(y)
                    if cell_str != cell_str_3:
                        _, ne = read.parse_input("fact: (not_equal " + cell_str_3 + ' ' + cell_str + ")")
                        KB.kb_assert(ne)

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
        for fact in KB.facts:
            print(fact)
        result = decide_next_move(gridsize, currgrid)

        message = result['message']
        cell = result['cell']
        print(cell)

        if cell:
            print('\n\n')
            rowno, colno = cell
            currcell = currgrid[rowno][colno]
            flag = result['flag']
            print(flag)

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
