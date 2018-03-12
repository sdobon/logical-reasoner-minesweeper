"""A command line version of Minesweeper"""
import random
import re
import time
from string import ascii_lowercase

import read, copy
from logical_classes import *
from KB_IE import KnowledgeBase


# KB = KnowledgeBase([], [])

#still mark_rest_bomb bug
#BUT MARKING DOWN FLAG WHERE FLAG SHOULD NOT BE

#if we put a flag down, we need to decrease everybody unknown_cells so we retract and then we also take away from everybody unknown_bomb_count

#things are only ever visited once we look at them in the board

_, found_safe_rule = read.parse_input("rule: ((number ?cell ?x) (known_bomb_count ?cell ?x)) -> (mark_rest_safe ?cell)")
#found_safe_rule if number in cell matches the known bombs then the rest of the cells around it are safe

_, set_bomb_rule = read.parse_input("rule: ((unknown_bomb_count ?cell ?x) (unknown_cells ?cell ?x)) -> (mark_rest_bomb ?cell)")
#set_bomb_rule if the # of unknown cells around the cell matches unknown bomb count, they must all be bombs

_, mark_rest_bomb = read.parse_input("rule: ((mark_rest_bomb ?cell_1) (adjacent ?cell_1 ?cell_2) (unvisited ?cell_2) -> (bomb ?cell_2)")
#if the cell has been mark_rest_bomb and some cell is adjacent to it, and we have not visited, the cell is a bomb
_, mark_rest_safe = read.parse_input("rule: ((mark_rest_safe ?cell_1) (adjacent ?cell_1 ?cell_2) (unvisited ?cell_2)) -> (safe ?cell_2)")
_, adjacent = read.parse_input("rule: ((adjacent ?cell_1 ?cell_2)) -> (adjacent ?cell_2 ?cell_1)")
#
# KB.kb_assert(found_safe_rule)
# KB.kb_assert(set_bomb_rule)
# KB.kb_assert(mark_rest_bomb)
# KB.kb_assert(mark_rest_safe)
# KB.kb_assert(adjacent)


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


def look_at_board(gridsize, currgrid, oldgrid, KB):

    #mark all new additions visited
    for i in range(0, gridsize):
        for j in range(0, gridsize):
            if currgrid[i][j] != oldgrid[i][j]: #we found a new change
                cell_str = str(i) + '_' + str(j) #name of cell changed

                _, unvisited_fact = read.parse_input("fact: (unvisited " + cell_str + ")") #we are now visiting that fact
                KB.kb_retract(unvisited_fact) #retract the visit


    #add new number facts for all numbers added and unknown_bomb_count
    for i in range(0, gridsize):
        for j in range(0, gridsize):
            if currgrid[i][j] != oldgrid[i][j]: #we found a new change
                cell_str = str(i) + '_' + str(j) #name of cell changed

                try:
                    num = int(currgrid[i][j]) #see if a number is there
                    _, count_fact = read.parse_input("fact: (number " + cell_str + ' ' + str(num) + ")")
                    KB.kb_assert(count_fact) #if so add the number and cell as a fact

                    for k in range(0, 9):
                        _, ask_bombs = read.parse_input("fact: (known_bomb_count " + cell_str + ' ' + str(k) + ")")
                        if KB.kb_ask(ask_bombs): #find the known bomb count
                            _, unknown_bombs = read.parse_input("fact: (unknown_bomb_count " + cell_str + ' ' + str(num - k) + ")")
                            KB.kb_assert(unknown_bombs) #assert the unknown bomb count
                            break
                except ValueError:
                    continue

    #update neighbor's unknown cells
    for i in range(0, gridsize):
        for j in range(0, gridsize):
            if currgrid[i][j] != oldgrid[i][j]:
                neighbors = getneighbors(currgrid, i, j)
                for n in neighbors:
                    cell_str_n = str(n[0]) + '_' + str(n[1])  # cell_str of neighbor
                    for l in range(0, 9):
                        _, ask_unknown_cells = read.parse_input("fact: (unknown_cells " + cell_str_n + ' ' + str(l) + ")")
                        if KB.kb_ask(ask_unknown_cells):  # find the unknown_cells
                            KB.kb_retract(ask_unknown_cells)  # take away unknown_cells
                            _, new_unknown_cells = read.parse_input("fact: (unknown_cells " + cell_str_n + ' ' + str(l - 1) + ")")

                            KB.kb_assert(new_unknown_cells)
                            break

    #update bomb_count of neighbor cells
    for i in range(0, gridsize):
        for j in range(0, gridsize):
            if currgrid[i][j] != oldgrid[i][j]:
                if currgrid[i][j] == 'F':
                    neighbors = getneighbors(currgrid, i, j)
                    for n in neighbors:
                        cell_str_n = str(n[0]) + '_' + str(n[1])
                        for m in range (0, 9):

                            _, ask_bomb_num = read.parse_input("fact: (known_bomb_count " + cell_str_n + ' ' + str(m) + ")")
                            if KB.kb_ask(ask_bomb_num):
                                KB.kb_retract(ask_bomb_num)
                                _, new_bomb_num = read.parse_input("fact: (known_bomb_count " + cell_str_n + ' ' + str(m + 1) + ")")
                                KB.kb_assert(new_bomb_num)
                                break

    for i in range(0, gridsize):
        for j in range(0, gridsize):
            if currgrid[i][j] != oldgrid[i][j]:
                if currgrid[i][j] == 'F':
                    neighbors = getneighbors(currgrid, i, j)
                    for n in neighbors:
                        cell_str_n = str(n[0]) + '_' + str(n[1])
                        for p in range (0, 9):
                            _, ask_bomb_num_unknown = read.parse_input("fact: (unknown_bomb_count " + cell_str_n + ' ' + str(p) + ")")
                            if KB.kb_ask(ask_bomb_num_unknown):
                                KB.kb_retract(ask_bomb_num_unknown)
                                _, new_bomb_num_unknown = read.parse_input("fact: (unknown_bomb_count " + cell_str_n + ' ' + str(p - 1) + ")")
                                KB.kb_assert(new_bomb_num_unknown)
                                break




def guess_move(currgrid, KB):


    while True:

        cell = getrandomcell(currgrid)
        cell_string = str(cell[0]) + '_' + str(cell[1])
        _, ask_unvisited = read.parse_input("fact: (unvisited " + cell_string + ")")
        if KB.kb_ask(ask_unvisited):
            print("guessing...")
            return {'cell': getrandomcell(currgrid), 'flag': False, 'message': ''}

def decide_next_move(gridsize, currgrid, KB):
    for i in range(gridsize):
        for j in range(gridsize):
            if currgrid[i][j] == ' ':
                cell_str = str(i) + '_' + str(j)


                _, ask_safe = read.parse_input("fact: (safe " + cell_str + ")")

                if KB.kb_ask(ask_safe):
                    print("Clicking safe square")

                    return {'cell': (i,j), 'flag': False, 'message': ''}

                _, ask_bomb = read.parse_input("fact: (bomb " + cell_str + ")")
                if KB.kb_ask(ask_bomb):
                    print("Flagging bomb")

                    return {'cell': (i,j), 'flag': True, 'message': ''}
    return guess_move(currgrid, KB)




def setup_facts(currgrid, KB):
    gridsize = len(currgrid)
    for i in range(gridsize):
        for j in range(gridsize): #loop through grid
            cell_str = str(i) + '_' + str(j) #cell_str

            _, known_bomb_count = read.parse_input("fact: (known_bomb_count " + cell_str + " 0)")
            KB.kb_assert(known_bomb_count) #assert the known_bomb_count of each cell to be 0

            _, unvisited_fact = read.parse_input("fact: (unvisited " + cell_str + ")")
            KB.kb_assert(unvisited_fact) #assert each cell to be unvisited


            neighbors = getneighbors(currgrid, i, j)

            _, unknown_cells = read.parse_input("fact: (unknown_cells " + cell_str + ' ' + str(len(neighbors)) + " )")
            KB.kb_assert(unknown_cells) #assert unknown_cells of each cell to be exactly the size of neighbor
            #adjacency
            for n in neighbors:

                cell_str_2 = str(n[0]) + '_' + str(n[1])
                _, adj = read.parse_input("fact: (adjacent " + cell_str_2 + ' ' + cell_str + ")")
                KB.kb_assert(adj)


def playgame():

    KB = KnowledgeBase([], [])
    KB.kb_assert(found_safe_rule)
    KB.kb_assert(set_bomb_rule)
    KB.kb_assert(mark_rest_bomb)
    KB.kb_assert(mark_rest_safe)
    KB.kb_assert(adjacent)

    gridsize = 9
    numberofmines = 10

    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

    setup_facts(currgrid, KB)

    grid = []
    flags = []
    starttime = 0

    helpmessage = ("Type the column followed by the row (eg. a5). "
                   "To put or remove a flag, add 'f' to the cell (eg. a5f).")

    # showgrid(currgrid)
    # print(helpmessage + " Type 'help' to show this message again.\n")

    while True:
        oldgrid = copy.deepcopy(currgrid)
        minesleft = numberofmines - len(flags)
        # prompt = input('Enter the cell ({} mines left): '.format(minesleft))
        # result = parseinput(prompt, gridsize, helpmessage + '\n')
        #_ = input('advance?')

        result = decide_next_move(gridsize, currgrid, KB)

        # if result['flag']:
        #     print "WE ARE FLAGGING"

        message = result['message']
        cell = result['cell']
        # print(cell)

        if cell:
            # print('\n\n')
            rowno, colno = cell
            currcell = currgrid[rowno][colno]
            flag = result['flag']
            # print(flag)

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

                return (0, 0)
                # showgrid(grid)
                # if playagain():
                #     playgame()
                # return

            elif currcell == ' ':
                showcells(grid, currgrid, rowno, colno)

            else:
                message = "That cell is already shown"

            if set(flags) == set(mines):
                minutes, seconds = divmod(int(time.time() - starttime), 60)
                print(
                    'You Win. ')
                    # 'It took you {} minutes and {} seconds.\n'.format(minutes,
                    #                                                   seconds))

                return (1, seconds)


                # if playagain():
                #     playgame()
                # return

        showgrid(currgrid)
        look_at_board(gridsize, currgrid, oldgrid, KB)
        # for fact in KB.facts:
        #     if "adjacent" not in str(fact.statement):
        #         print fact

        # showgrid(currgrid)
        # print(message)



def measure1000():
    wins = 0
    total_games = 0
    seconds = 0

    for i in range(0, 5):
        result = playgame()
        total_games = total_games + 1
        if result[0] == 1:
            wins = wins + 1
            seconds = seconds + result[1]

    print("Win Percentage: " + str(float(float(wins)/float(total_games)) * 100) + "% " + " Average game time: " + str(float(seconds/wins)))




# playgame()
measure1000()
