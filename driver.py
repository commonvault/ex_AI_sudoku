#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 21:34:11 2020

@author: ornwipa
"""

import sys
from copy import deepcopy

class sudoku(object):
    def __init__(self, str_rep):
        self.str_rep = str_rep # simply take string representation of 81 digits
        """ create a dictionary with key 11...19, 91...99 """
        self.map = dict()
        for i in range(81):
            rowid = i // 9 + 1
            colid = i % 9 + 1
            key = str(rowid) + str(colid)
            self.map[key] = int(self.str_rep[i])

    def check_map(self):
        print(self.map) # check the correct mapping values to dict in __init__
        
    def get_cell_value(self, row, col):
        """ row, col take int 1...9, use string as key in the dictionary"""
        return int(self.map[str(row) + str(col)]) # ensure to get int, not str
    
    def set_cell_value(self, key, value):
        """ key is a string e.g. '11' """
        if type(value) != int:
            raise TypeError('Value must be integer.')
        if value < 0 or value > 9:
            raise ValueError('Value must be in {0,1,2,3,4,5,6,7,8,9}.')
        self.map[key] = value
    
    def map_to_str(self):
        out = ''
        for i in range(1,10):
            for j in range(1,10):
                out += str(self.map[str(i) + str(j)])
        return out
    
    def clone(self):
        Xcopy = sudoku(self.str_rep)
        Xcopy.map = deepcopy(self.map)
        return Xcopy
    
    def alldiff(self, dictkeys):
        """ dictkeys is a set of only 9 dictionary keys in row, col, box """
        for i in dictkeys:
            if self.map[i] != 0:
                for j in dictkeys:
                    if j != i and self.map[i] == self.map[j]:
                        return False
        return True
    
    def alldiff_row(self, row):
        dictkeys = set()
        for i in range(1,10):
            dictkeys.add(str(row) + str(i))
        return self.alldiff(dictkeys)
    
    def alldiff_col(self, col):
        dictkeys = set()
        for i in range(1,10):
            dictkeys.add(str(i) + str(col))
        return self.alldiff(dictkeys)
    
    def keys_in_box(self, h, v):
        """ h, v are integers 1, 2, 3 : represent horizontal, vertical position 
        of a 3x3 box on the board ; return dictionary keys in the same box """
        dictkeys = set()
        for i in range((h-1)*3+1, h*3+1):
            for j in range((v-1)*3+1, v*3+1):
                dictkeys.add(str(i) + str(j))
        return dictkeys
    
    def alldiff_box(self, h, v):
        dictkeys = self.keys_in_box(h, v)
        return self.alldiff(dictkeys)
    
    def allfill(self, dictkeys):
        """ check if all cells are filled with 1,2,3,4,5,6,7,8,9, none is 0 """
        for i in dictkeys:
            if self.map[i] == 0:
                return False
        return True
    
    def domain(self, key):
        """ key is a single key in dictionary, return domain of cell values """
        if self.map[key] != 0:
            return {self.map[key]} # in case of non-empty cell, domain is fixed
        domain = {1,2,3,4,5,6,7,8,9}
        row, col = int(key)//10, int(key)%10
        for i in range(1,10):
            if i != col:
                try:
                    domain.remove(self.map[str(row) + str(i)])
                except KeyError:
                    pass
        for i in range(1,10):
            if i != row:
                try:
                    domain.remove(self.map[str(i) + str(col)])
                except KeyError:
                    pass
        h, v = (row-1)//3+1, (col-1)//3+1
        for k in self.keys_in_box(h, v):
            if k != key:
                try:
                    domain.remove(self.map[k])
                except KeyError:
                    pass
        return domain
    
    def neighbor(self, key):
        """ return neighboring nodes, same row, col, box """
        neighbors = set()
        row, col = int(key)//10, int(key)%10
        for i in range(1,10):
            if i != col:
                neighbors.add(str(row) + str(i))
        for i in range(1,10):
            if i != row:
                neighbors.add(str(i) + str(row))
        h, v = (row-1)//3+1, (col-1)//3+1
        for k in self.keys_in_box(h, v):
            if k != key:
                neighbors.add(k)        
        return neighbors
    
    def arcs(self):
        """ create all arcs (Xi, Xj) where Xi is an empty cell, Xj is in 
        the same row, col, box as Xi; arcs are key mapping e.g. ('11','32') """
        arcs = set()
        for i in range(1,10):
            for j in range(1,10):
                key = str(i) + str(j)
                if self.map[key] == 0:# and key not in emptycells:
                    
                    for k in range(1,10): # check cells in same row
                        if k != j:# and self.map[str(i) + str(k)] == 0:
                            arcs.add( (key, str(i) + str(k)) )
                            
                    for k in range(1,10): # check cells in same col
                        if k != i:# and self.map[str(k) + str(j)] == 0:
                            arcs.add( (key, str(k) + str(j)) )
                            
                    h, v = (i-1)//3+1, (j-1)//3+1
                    keys_in_box = self.keys_in_box(h, v)
                    for other_key in keys_in_box:
                        if key != other_key:# and self.map[other_key] == 0:
                            arcs.add( (key, other_key) )
        return arcs 

def REVISE(X, xi, xj, Di):
    """ xi, xj are dictionary keys of two cells in arcs; Di is a pre-extracted
    domain of xi and will be returned if it is revised inside the function """
    revised = False
    for d in Di:
        """ if no y in Dj allows (d,y) to satisfy constraint between xi, xj """
        if X.domain(xj) == {d}: # there is only d in Dj, so d cannot be in Di 
            #to_remove.add(d)
            Di.remove(d)
            break
    return (revised, Di)

def AC3(X):
    """ take sudoku class object as input variable X, each has domain D = {1...9} 
    and check arc consistency: for all xi, there are some xj differing from xi """
    for n in range(2): # run 3 times (once or twice didn't work, some left 0)
        queue = list(X.arcs()) # a queue of all arcs in CSP         
        D = dict() # keep track of domain values as reduced
        while queue != []:
            (xi, xj) = queue.pop() # LIFO stack for DFS
            if xi not in D:
                Di = X.domain(xi) # extract domain values for the first time
            else:
                Di = D[xi] # use the domain values stored in dict
        
            (revised, Di) = REVISE(X, xi, xj, Di)
            D[xi] = Di # re-assign the domain values once check to revise
            if len(Di) == 1:
                X.set_cell_value(xi, next(iter(Di))) # set value once only one left
            
            if revised:            
                if len(Di) == 0:
                    return False # inconsistent      
                for xk in X.neighbor(xi): # neighbors of xi
                    if xk != xj:# and X.map[xk] == 0:
                        queue.append((xk, xi))
    return X.map_to_str()

def BACKTRACK(assignment, X):
    """ if assignment is complete then return assignment """
    if assignment.allfill(assignment.map.keys()): # base case (to end recursion)
        return assignment

    """ which variable should be assigned next?
    minimum remaining value (var x with fewest legal values in its domain) """
    least_legal_val = 9
    for key in assignment.map:
        domain_size = len(assignment.domain(key))
        if domain_size < least_legal_val and assignment.map[key] == 0:
            least_legal_val = domain_size
            var = key # this is the heuristic: SELECT_UNASSIGNED_VARIABLES(csp)
    
    row, col = int(var)//10, int(var)%10
    h, v = (row-1)//3+1, (col-1)//3+1                           
    """ in what order should the value of x be tried?
    least constraining value (rules out the fewest values in remaining var) """
    for value in assignment.domain(var): # ORDER_DOMAIN_VALUES(var, assignment, csp)
        tmp = assignment.clone()
        tmp.set_cell_value(var, value)
        """ if value is consistent with assignment """
        if tmp.alldiff_row(row) and tmp.alldiff_col(col) and tmp.alldiff_box(h, v):
            assignment.set_cell_value(var, value) # then assign value to variable
            result = BACKTRACK(assignment, X)
            if result != 'failure':
                return result
            assignment.set_cell_value(var, 0) # remove value from variable
    return 'failure'

def BTS(X):
    """ take sudoku class object as input variable X, each has domain D = {1...9} 
    and have to satisfy constraint C = alldiff_row, alldiff_col, alldiff_box """
    soln = BACKTRACK(X.clone(), X) # first assignment is deepcopy of X    
    try:
        ans = soln.map_to_str()
    except AttributeError: # in case failure, return string
        ans = soln
    return ans
    
def main():
    input_string = str(sys.argv[1])
#     input_file = open("sudokus_start.txt", "r")
# #    line_count = 0
#     while True:
#         input_string = str(input_file.readline())        
# #        line_count += 1
#         if input_string == '\n':
#             break
# #        print(input_string, line_count)
    """ start code to solve sudokus here """
    X = sudoku(input_string)
    out_string = AC3(X)
    if X.allfill(X.map.keys()):
        output_file = open("output.txt", "w")
        output_file.write(out_string + ' AC3\n')
        output_file.close
    else:
        out_string = BTS(X)
        output_file = open("output.txt", "w")
        output_file.write(out_string + ' BTS\n')
        output_file.close        
    
#if __name__ == '__main__':
#    main()

# test = sudoku('000260701680070090190004500820100040004602900050003028009300074040050036703018000')
# print(AC3(test))
# print(BTS(test))
# test = sudoku('003000000008007100560090002005304600000070000320600570030002007002000000670813050')
# print(AC3(test))
# print(BTS(test))
# test = sudoku('000008006050300010007106002000000904913000020065030007030080000001500800500000043')
# print(AC3(test))
# print(BTS(test))
test = sudoku('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
print(AC3(test))
print(BTS(test))
test = sudoku('800000090075209080040500100003080600000300070280005000000004000010027030060900020')
print(AC3(test))
print(BTS(test))