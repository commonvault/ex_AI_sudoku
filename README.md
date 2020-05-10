# Sudoku
This is the 4th assignment of the Artificial Intelligence course at Columbia University. This code solves a constraint satisfaction problem (CSP) using arc-consistency (AC3) and backtracking (BTS) algorithms, completed on April 7, 2020.

**Problem Description:**
Consider the Sudoku puzzle, there are 81 variables in total, i.e. the tiles to be filled with digits. Each variable is named by its row and its column, and must be assigned a value from 1 to 9, subject to the constraint that no two cells in the same row, column, or box may contain the same value.

*Considerations in AC3*

1.) Which are the initial arcs that need to be added to the queue? First look for ALL empty cells on the sudoku board. Then, at each empty cell, create arcs between this cell and its neighbors. The 'neighbor' means the cells in the same row, column, or 3x3 box, regardless whether they are already labeled or not. For example, the neighbor of '11' are '12', '13',... '19', '21', '31',... '91', '22', '23', 32', '33'. This way, you will create arcs ('11', '12'), ('11', '13'), etc. In other words, (empty cell, ALL neighbors)

2.) Which arcs should be added after REDUCING the arc? If checking an arc ('11', '16') leads to revising the cell '11', this also means we may also be able to reduce the domain value of the neighbors of '11'. The arcs to be added would be ('12', '11'), ('13', '11'), ('21', '11'), ('22', '11') etc., EXCEPT ('16', '11') that is (Xk, Xi) where Xk are neighbors of Xi except Xj.

*Considerations in BTS*

1.) Which variable should be assigned next?
    minimum remaining value (var x with fewest legal values in its domain

2.) In what order should the value of x be tried?
    least constraining value (rules out the fewest values in remaining var)
