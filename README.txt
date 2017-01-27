This is a tool to solve sudoku puzzles in a human-like fashion.

Features:
-Guess depth can be set to make this more similar to how a person would solve the puzzle. The default guess depth for the solve function is 1, which seems to be enough to solve all the typically occurring difficulties of puzzles, but not the very hardest ones. 
-An optional verbose parameter prints the step-by-step solution in a way that (I hope!) is easily understandable. See below for an example.

Things I learned while making this:
-I elected to create and update a few data structures to accompany the puzzle: one to keep track of possibilities per cell, and the other to keep track of where each value can appear within a particular row/column/cluster. I’m not sure how this compares speed-wise to keeping the data structure really simple and carrying out the logical deductions from scratch each time. But either way, the updating is difficult, bug-wise. It might have been better to first try the really simple structure, since worst-case, it’s slow, and then it functions as a tool to check the more complex version.
-It would be better/more readable to make a sudoku class, since I was frequently passing to a function three separate data structures describing the same puzzle.
-I made a nice print function before anything else, which was very useful with debugging.
-After finishing the program, I searched the web and found Peter Norvig’s writeup of a far superior solution (http://norvig.com/sudoku.html). There’s a lot to learn from this, but two things that stuck out are the convenience of using strings for possibilities in place of lists (easier copying) and the general structure of constraint propagation vs backtracking.


Example output from sudoku_solver.py:
-----------------------------------
            New puzzle
-----------------------------------

 .   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   .   . | .   .   5 | 8   .   .  
           |           |           
 .   5   . | .   6   . | .   2   .  
           |           |           
 .   .   4 | 1   .   . | .   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

8 can only appear in one place in row 1:

_8_  .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   .   . | .   .   5 | 8   .   .  
           |           |           
 .   5   . | .   6   . | .   2   .  
           |           |           
 .   .   4 | 1   .   . | .   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

1 can only appear in one place in row 5:

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   .   . | .   .   5 | 8   .   .  
           |           |           
 .   5   . | .   6   . |_1_  2   .  
           |           |           
 .   .   4 | 1   .   . | .   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

1 can only appear in one place in column 2:

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .  _1_  . | .   .   5 | 8   .   .  
           |           |           
 .   5   . | .   6   . | 1   2   .  
           |           |           
 .   .   4 | 1   .   . | .   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

7 can only appear in one place in column 2:

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   .   5 | 8   .   .  
           |           |           
 .   5   . | .   6   . | 1   2   .  
           |           |           
 .  _7_  4 | 1   .   . | .   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

8 can only appear in one place in column 3:

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   .   5 | 8   .   .  
           |           |           
 .   5  _8_| .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   .   . | .   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

9 can only appear in one place in column 7:

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   .   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   .   . |_9_  .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

3 is the only possible value for cell (6, 5):

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   .   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1  _3_  . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

7 can only appear in one place in column 5:

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .  _7_  5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   .  

-----------------------------------

8 can only appear in one place in column 9:

 8   .   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   7   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .  _8_ 

-----------------------------------

Exhausted basic logic, now trying trial and error...
Looking for cells with 2 possibilities...
Making a guess of 4 at (1, 2), where possibilities are [4, 6].
Guess resulted in invalid state. 4 cannot occur at (1, 2):

 8  _._  1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   7   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   8  

-----------------------------------

6 is the only possible value for cell (1, 2):

 8  _6_  1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   7   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   .   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   8  

-----------------------------------

4 is the only possible value for cell (8, 2):

 8   6   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 .   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   7   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1  _4_  . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   8  

-----------------------------------
4 can only appear in one place in cluster 1:

 8   6   1 | .   .   7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
_4_  3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   7   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   4   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   8  

-----------------------------------

Exhausted basic logic, now trying trial and error...
Looking for cells with 2 possibilities...
Making a guess of 4 at (1, 5), where possibilities are [4, 5].
Guess resulted in invalid state. 4 cannot occur at (1, 5):

 8   6   1 | .  _._  7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 4   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   7   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   4   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   8  

-----------------------------------

5 is the only possible value for cell (1, 5):

 8   6   1 | .  _5_  7 | .   9   .  
           |           |           
 5   9   . | .   8   . | .   .   1  
           |           |           
 4   3   . | .   .   . | .   8   .  
-----------|-----------|-----------
 .   1   . | .   7   5 | 8   .   .  
           |           |           
 .   5   8 | .   6   . | 1   2   .  
           |           |           
 .   7   4 | 1   3   . | 9   .   .  
-----------|-----------|-----------
 .   8   . | .   .   . | .   3   .  
           |           |           
 1   4   . | .   2   . | .   7   9  
           |           |           
 .   2   . | 7   .   . | 4   .   8  

-----------------------------------

Exhausted basic logic, now trying trial and error...
Looking for cells with 2 possibilities...
Making a guess of 2 at (1, 7), where possibilities are [2, 3].
Lucky! Guess led to a completely solved puzzle.
-----------------------------------

Solution:

 8   6   1 | 3   5   7 | 2   9   4  
           |           |           
 5   9   7 | 4   8   2 | 3   6   1  
           |           |           
 4   3   2 | 6   1   9 | 7   8   5  
-----------|-----------|-----------
 9   1   6 | 2   7   5 | 8   4   3  
           |           |           
 3   5   8 | 9   6   4 | 1   2   7  
           |           |           
 2   7   4 | 1   3   8 | 9   5   6  
-----------|-----------|-----------
 7   8   9 | 5   4   1 | 6   3   2  
           |           |           
 1   4   3 | 8   2   6 | 5   7   9  
           |           |           
 6   2   5 | 7   9   3 | 4   1   8  

