##########################################
# Written 02-14-2024 by Spencer Trumbore #
##########################################

import numpy as np
import csv

def InitializeCharmsArray():
    datafile = open('hk_charms.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    data = []
    for row in datareader:
        data.append([int(row[0]), row[1], int(row[2])])
    return data

def WeightSum(_charmArray):
    total = 0
    for charm in _charmArray:
        total += charm[2]
    return total

def GrimmchildOrCarefree(_charm):
    if (_charm[0] == 39 or _charm[0] == 40): return 1
    else: return 0

def KingsoulOrVoidheart(_charm):
    if (_charm[0] == 41 or _charm[0] == 42): return 1
    else: return 0


charmsArray = InitializeCharmsArray()
combinations = [[]]

counter = 0
conflict = False
f = open("combos.txt", "a")
for charm in charmsArray:
    for subset in combinations:
        if (charm not in subset):
            if (charm[0] == 39 or charm[0] == 40):
                if (np.sum(list(map(GrimmchildOrCarefree, subset))) > 0):
                    conflict = True
            elif (charm[0] == 41 or charm[0] == 42):
                if (np.sum(list(map(KingsoulOrVoidheart, subset))) > 0):
                    conflict = True
            if ((conflict == False) and (WeightSum(subset) + charm[2] <= 11)):
                new_subset = subset + [charm]
                combinations.append(new_subset)
                counter+=1
                f.write(str(counter) + '\t' + str(new_subset) + '\n')
            conflict = False

f.close()
print(counter)
print("DONE!")