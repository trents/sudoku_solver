""" Sudoku solver """

import math
import random
import copy

def find_x_wing_pairs(pair_array):
    pair_array_return = []
    i = 0
    while i < len(pair_array):
        j = i+1
        while j < len(pair_array):
            if pair_array[i][1] == pair_array[j][1] and pair_array[i][2] == pair_array[j][2] and pair_array[i][3] == pair_array[j][3]:
                  pair_array_return.append([pair_array[i][1],pair_array[i][0],pair_array[j][0],pair_array[j][2],pair_array[j][3]])
            j += 1
        i += 1
    return pair_array_return

def find_twice_in_row(row):
    results = []
    for i in range(9):
       temp_string = str(i)
       count = 0
       for item in row:
          if temp_string in item:
              count += 1
       if count == 2:
          results.append(temp_string)
    return results

def find_twice_in_row_cols(row,item):
    results = [item]
    for i in range(9):
       if item in row[i]:
           results.append(i)
    return results

def swordfish(sudoku_grid):
    twice_in_row = []
    for i in range(9):
        twice_in_row.append(find_twice_in_row(sudoku_grid[i]))

# create items of value, row, col, col
    swordfishes = []

    for i in range(9):
        current_row = twice_in_row[i]
        for item in current_row:
            current_sword = [item, i]
            for j in range(9):
                if item in sudoku_grid[i][j]:
                    current_sword.append(j)
            swordfishes.append(current_sword)

# identify swordfish cycles - value, row1, col, col, row2, col, col, row3, col, col
    cycles = []

    for i in range(9):
        current_val = str(i+1)
        temp_array = []
        for item in swordfishes:
            if item[0] == current_val:
                temp_array.append(item)
#        print(temp_array)

    return sudoku_grid

def x_wing(sudoku_grid):
    twice_in_row = []
    for i in range(9):
        twice_in_row.append(find_twice_in_row(sudoku_grid[i])) 
    twice_in_row_cols = []
    for i in range(9):
        temp = []
        for item in twice_in_row[i]:
            temp.append(find_twice_in_row_cols(sudoku_grid[i],item))
        for item in temp:
            twice_in_row_cols.append([i,item[0],item[1],item[2]])
    x_wing_pairs = find_x_wing_pairs(twice_in_row_cols)
    for item in x_wing_pairs:
        for i in range(9):
            if i != item[1] and i != item[2]:
                if item[0] in sudoku_grid[i][item[3]]:
                        chunks = sudoku_grid[i][item[3]].split(item[0])
                        sudoku_grid[i][item[3]] = chunks[0] + chunks[1]
                if item[0] in sudoku_grid[i][item[4]]:
                        chunks = sudoku_grid[i][item[4]].split(item[0])
                        sudoku_grid[i][item[4]] = chunks[0] + chunks[1]
    return sudoku_grid

def reduce_row(row,sudoku_grid):
    for i in range(9):
        if len(sudoku_grid[row][i]) == 1:
            for j in range(9):
                if i != j:
                    if sudoku_grid[row][i] in sudoku_grid[row][j]:
                        chunks = sudoku_grid[row][j].split(sudoku_grid[row][i])
                        sudoku_grid[row][j] = chunks[0] + chunks[1]
    count_dict = {}
    for i in range(9):
        for char in sudoku_grid[row][i]:
            if char in count_dict:
                count_dict[char] = "X"
            else:
                count_dict[char] = i

    for key in count_dict:
        if count_dict[key] != "X":
            sudoku_grid[row][count_dict[key]] = key

    return sudoku_grid

def reduce_col(col,sudoku_grid):
    for i in range(9):
        if len(sudoku_grid[i][col]) == 1:
            for j in range(9):
                if i != j:
                    if sudoku_grid[i][col] in sudoku_grid[j][col]:
                        chunks = sudoku_grid[j][col].split(sudoku_grid[i][col])
                        sudoku_grid[j][col] = chunks[0] + chunks[1]
    count_dict = {}
    for i in range(9):
        for char in sudoku_grid[i][col]:
            if char in count_dict:
                count_dict[char] = "X"
            else:
                count_dict[char] = i

    for key in count_dict:
        if count_dict[key] != "X":
            sudoku_grid[count_dict[key]][col] = key

    return sudoku_grid

def reduce_sub(sub,sudoku_grid):
    minigrid = []
    row = math.floor(sub/3)
    col = sub % 3
    start_row = row * 3
    start_col = col * 3
    for j in range(start_row,start_row+3):
        minirow = []
        for k in range(start_col,start_col+3):
            minirow.append(sudoku_grid[j][k])
        minigrid.append(minirow)
    minigrid = reduce_mini(minigrid)
    for j in range(start_row,start_row+3):
        for k in range(start_col,start_col+3):
            sudoku_grid[j][k] = minigrid[j%3][k%3]
    return sudoku_grid

def reduce_mini(minigrid):
    row = []
    for i in range(3):
        for j in range(3):
            row.append(minigrid[i][j])
    for i in range(9):
        if len(row[i]) == 1:
            for j in range(9):
                if i != j:
                    if row[i] in row[j]:
                        chunks = row[j].split(row[i])
                        row[j] = chunks[0] + chunks[1]

    count_dict = {}
    for i in range(9):
        for char in row[i]:
            if char in count_dict:
                count_dict[char] = "X"
            else:
                count_dict[char] = i

    for key in count_dict:
        if count_dict[key] != "X":
            row[count_dict[key]] = key

    for i in range(3):  
        for j in range(3):
            minigrid[i][j] = row[(i*3)+j]

    return minigrid

def reducer(sudoku_grid):
    for i in range(9):
        sudoku_grid = reduce_row(i,sudoku_grid)
        sudoku_grid = reduce_col(i,sudoku_grid)
        sudoku_grid = reduce_sub(i,sudoku_grid)
    return sudoku_grid

def validator(sudoku_grid):
    for i in range(9):
        checker = []
        for j in range(9):
            if sudoku_grid[i][j] not in checker:
                checker.append(sudoku_grid[i][j])
            else:
                return False

    for i in range(9):
        checker = []
        for j in range(9):
            if sudoku_grid[j][i] not in checker:
                checker.append(sudoku_grid[j][i])
            else:
                return False
    return True

def brute_force(sudoku_grid):
    valid = False
    temp_grid = copy.deepcopy(sudoku_grid)
    for i in range(9):
        for j in range(9):
            if len(temp_grid[i][j]) > 1:
                for item in sudoku_grid[i][j]:
                    temp_grid[i][j] = item
                    temp_grid = brute_force(temp_grid)
                    if validator(temp_grid):
                        return temp_grid
    return sudoku_grid                        

def sudoku_solver(arr):
    sudoku_grid = []
    for line in arr:
        sudoku_line = []
        if line[0] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[0])
        if line[1] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[1])
        if line[2] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[2])
        if line[3]== " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[3])
        if line[4] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[4])
        if line[5] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[5])
        if line[6] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[6])
        if line[7] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[7])
        if line[8] == " ":
            sudoku_line.append("123456789")
        else:
            sudoku_line.append(line[8])
        sudoku_grid.append(sudoku_line)

    for j in range(15):
        sudoku_grid = reducer(sudoku_grid)

# now that it's reduced, the last step is to simply brute force what's left with randomized entries and validate

    sudoku_grid = x_wing(sudoku_grid)
    sudoku_grid = swordfish(sudoku_grid)
    print(sudoku_grid)
    sudoku_grid = brute_force(sudoku_grid)

    print(sudoku_grid)

    return 0

with open("sudoku-puzzle.txt") as file:
    d = file.readlines()
new_arr = []
for line in d:
    if len(line) == 9:
        new_arr.append(line)
    else:
       j = 9 - len(line)
       for i in range(j):
           line = line + " "
       new_arr.append(line)
print(sudoku_solver(new_arr))
