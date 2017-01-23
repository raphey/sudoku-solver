__author__ = 'raphey'


import time


def start_timer():
    """Creates a global timing variable. To be used with stop_timer.
    """
    global time0
    time0 = time.time()


def stop_timer():
    """Prints time elapsed since start_timer function was called.
    """
    print "Time elapsed:", round(time.time() - time0, 3), "seconds"


def memo(f):
    """Decorator that caches the return value for each call to f(args) to speed of repeated calls.

    Taken from Peter Norvig's Design of Computer Programs course.
    """

    cache = {}

    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f


def print_puzzle(puzzle, change_list=None):
    """Prints a sudoku puzzle.

    puzzle is a 9x9 list of lists, the puzzle in current state, with zeros for unknown values.
    change_list is an optional list of tuples, a list of newly changed coordinates to be emphasized in printout
    Currently no part of the algorithm draws conclusions regarding multiple cells, but the idea was that some logic
    could apply to pairs or triples of cells.
    """
    if change_list is None:
        change_list = []
    hr = "-" * 11 + "|" + "-" * 11 + "|" + "-" * 11
    br = " " * 11 + "|" + " " * 11 + "|" + " " * 11
    print
    for i in range(0, 9):
        row_str = ""
        for j in range(0, 9):
            val = puzzle[i][j]
            print_val = "." if val == 0 else str(val)
            if (i, j) in change_list:
                row_str += "_" + print_val + "_"
            else:
                row_str += " " + print_val + " "
            if j == 2 or j == 5:
                row_str += "|"
            else:
                row_str += " "
        print row_str
        if i == 2 or i == 5:
            print hr
        elif i < 8:
            print br
    print


@memo
def row(i):
    """Returns all the cells in row i, as a list of tuples.
    """
    return [(i, x) for x in range(0, 9)]


@memo
def col(j):
    """Returns all the cells in column j, as a list of tuples.
    """
    return [(x, j) for x in range(0, 9)]


@memo
def clust(k):
    """Returns all the cells in cluster k, as a list of tuples. (A cluster is one of nine 3x3 groups.)

    Clusters are numbered like this:
    012
    345
    678
    """
    xd = k // 3
    yd = k % 3
    return [(x + 3 * xd, y + 3 * yd) for x in range(0, 3) for y in range(0, 3)]


def row_mates(i, j):
    """For a given cell i, j in a puzzle, returns the 8 other cells in the same row, as a list of tuples.
    """
    return [cell for cell in row(i) if cell != (i, j)]


def col_mates(i, j):
    """For a given cell i, j in a puzzle, returns the 8 other cells in the same column, as a list of tuples.
    """
    return [cell for cell in col(j) if cell != (i, j)]


def clust_mates(i, j):
    """For a given cell i, j in a puzzle, returns the 8 other cells in the same cluster, as a list of tuples.
    """
    return [cell for cell in clust(clust_index(i, j)) if cell != (i, j)]


@memo
def clust_index(i, j):
    """For a given cell i, j, returns the index of the 3x3 cluster for that cell.

    Clustered are numbered:
    0   1   2
    3   4   5
    6   7   8
    """
    return 3 * (i // 3) + j // 3


@memo
def all_mates(i, j):
    """For a given cell i, j in a puzzle, returns the 20 other cells in the same row/col/cluster, as a list of tuples.
    """
    return list(set(row_mates(i, j)) | set(col_mates(i, j)) | set(clust_mates(i, j)))


def test_cell(puzzle, i, j, val):
    """Checks whether puzzle[i][j] can equal val; returns false if this creates a conflict with a row/col/cluster mate.
    """
    for x, y in all_mates(i, j):
        if puzzle[x][y] == val:
            return False
    return True


def init_cell_poss(puzzle):
    """Takes an initial puzzle state and returns a data structure with a list of possible values for each cell.

    Cells that are already filled in will have empty lists.
    """
    cell_poss = []
    for i in range(0, 9):
        cell_poss.append([])
        for j in range(0, 9):
            if puzzle[i][j] == 0:
                cell_poss[i].append([x for x in range(1, 10) if test_cell(puzzle, i, j, x)])
            else:
                cell_poss[i].append([])
    return cell_poss


def init_val_loc(cell_poss):
    """Takes initial puzzle state; returns possible locations for each value within each row/col/clust structure.

    Returns a list val_loc. val_loc[s][i][v] corresponds to a list of possible positions within a structure, for
    structure type s (0, 1, 2 for row/col/clust), the ith occurrence of that structure, and the placement of value v
    (1 through 9, with an empty placeholder for index 0). val_loc[s][i][v] has an empty list if the value has already
    been assigned within the structure.

    Row and column numbering is intuitive, from 0-8. Clusters and positions within clusters are numbered as follows:
    012
    345
    678
    """
    row_loc = []
    for i in range(0, 9):
        row_loc.append([[]])
        for v in range(1, 10):
            v_loc = [x for x in range(9) if v in cell_poss[i][x]]
            row_loc[i].append(v_loc)

    col_loc = []
    for i in range(0, 9):
        col_loc.append([[]])
        for v in range(1, 10):
            v_loc = [x for x in range(9) if v in cell_poss[x][i]]
            col_loc[i].append(v_loc)

    clust_loc = []
    for i in range(0, 9):
        ul_i = 3 * (i // 3)    # row of upper left corner cell
        ul_j = 3 * (i % 3)          # col of upper left corner cell
        clust_loc.append([[]])
        for v in range(1, 10):
            v_loc = [x for x in range(9) if v in cell_poss[ul_i + x // 3][ul_j + x % 3]]
            clust_loc[i].append(v_loc)

    val_loc = [row_loc, col_loc, clust_loc]
    return val_loc


def assignment_update(i, j, v, puzzle, cell_poss, loc_val):
    """Assigns puzzle[i][j] to have value v and updates data structures for cell possibilities and locations of values
    """
    row_loc, col_loc, clust_loc = loc_val[0], loc_val[1], loc_val[2]
    puzzle[i][j] = v
    cell_poss[i][j] = []
    row_loc[i][v] = []
    col_loc[j][v] = []
    k = clust_index(i, j)
    cl = 3 * (i % 3) + j % 3
    clust_loc[k][v] = []
    for x, y in all_mates(i, j):
        if puzzle[x][y] == 0:        # Time saver, since there's nothing to update for a cell that's already assigned
            if v in cell_poss[x][y]:
                cell_poss[x][y].remove(v)

    for v in range(1, 10):
        if j in row_loc[i][v]:
            row_loc[i][v].remove(j)
        if i in col_loc[j][v]:
            col_loc[j][v].remove(i)
        if cl in clust_loc[k][v]:
            clust_loc[k][v].remove(cl)


def check_for_single_poss(puzzle, cell_poss, val_loc, verbose=False):
    """Tries to find an incomplete cell with only one remaining possibility; fills it in and updates data structures.

    As it discovers such a value, modifies data structures, returns True, and prints the puzzle if verbose is True.
    """
    for i in range(9):
        for j in range(9):
            if len(cell_poss[i][j]) != 1:         # (Solved cells will have empty lists)
                continue
            new_val = cell_poss[i][j][0]
            assignment_update(i, j, new_val, puzzle, cell_poss, val_loc)
            if verbose:
                print "-----------------------------------"
                print
                print "%s is the only possible value for cell (%s, %s):" % \
                      (new_val, i + 1, j + 1)
                print_puzzle(puzzle, [(i, j)])
            return True
    return False


def check_for_single_val_loc(puzzle, cell_poss, val_loc, verbose=False):
    """Tries to find a structure with only one possible location for a value; fills it in and updates data structures.

    When it finds such a location/value, modifies data structures, returns True, and prints puzzle if verbose is True.
    """
    row_loc, col_loc, clust_loc = val_loc[0], val_loc[1], val_loc[2]

    for i in range(9):
        for v in range(1, 10):
            if len(row_loc[i][v]) != 1:         # (Solved location/values will have empty lists)
                continue
            new_loc = row_loc[i][v][0]
            assignment_update(i, new_loc, v, puzzle, cell_poss, val_loc)
            if verbose:
                print "-----------------------------------"
                print
                print "%s can only appear in one place in row %s:" % (v, i + 1)
                print_puzzle(puzzle, [(i, new_loc)])
            return True

    for j in range(9):
        for v in range(1, 10):
            if len(col_loc[j][v]) != 1:         # (Solved location/values will have empty lists)
                continue
            new_loc = col_loc[j][v][0]
            assignment_update(new_loc, j, v, puzzle, cell_poss, val_loc)
            if verbose:
                print "-----------------------------------"
                print
                print "%s can only appear in one place in column %s:" % (v, j + 1)
                print_puzzle(puzzle, [(new_loc, j)])
            return True
    for k in range(9):
        for v in range(1, 10):
            if len(clust_loc[k][v]) != 1:         # (Solved location/values will have empty lists)
                continue
            new_loc = clust_loc[k][v][0]

            new_loc_i = 3 * (k // 3) + new_loc // 3
            new_loc_j = 3 * (k % 3) + new_loc % 3

            assignment_update(new_loc_i, new_loc_j, v, puzzle, cell_poss, val_loc)

            if verbose:
                print "-----------------------------------"
                print "%s can only appear in one place in cluster %s:" % (v, k + 1)
                print_puzzle(puzzle, [(new_loc_i, new_loc_j)])
            return True

    return False


def make_guess(puzzle, i, j, v, guess_depth, cell_poss, val_loc, verbose):
    """Tries a single value, v, at location i, j, by solving a copy of the original puzzle with the new value.
    If it reaches a conclusion (valid or invalid), it adjusts the data structures and returns True.
    If it does not reach a conclusion (limited by guess_depth), it returns False.
    """
    if verbose:
        print "Making a guess of %s at (%s, %s), where possibilities are %s." % (v, i + 1, j + 1, cell_poss[i][j])
    puzzle_copy = [x[:] for x in puzzle]
    puzzle_copy[i][j] = v
    complete, valid = solving_algorithm(puzzle_copy, False, guess_depth - 1)
    if not valid:
        if verbose:
            print "Guess resulted in invalid state. %s cannot occur at (%s, %s):" % (v, i + 1, j + 1)
        cell_poss[i][j].remove(v)
        val_loc[0][i][v].remove(j)
        val_loc[1][j][v].remove(i)
        k = clust_index(i, j)
        cl = 3 * (i % 3) + j % 3
        val_loc[2][k][v].remove(cl)
        if verbose:
            print_puzzle(puzzle, [(i, j)])
        return True
    if complete:
        if verbose:
            print "Lucky! Guess led to a completely solved puzzle."
        for i in range(9):
            for j in range(9):
                puzzle[i][j] = puzzle_copy[i][j]
        return True
    if verbose:
        print "Guess didn't terminate--inconclusive."
    return False


def try_all_guesses(puzzle, guess_depth, cell_poss, val_loc, verbose):
    """Tries a series of guesses in cells, starting with cells with only two possibilities, then three, four, etc.

    Returns True if at least one guess results in a True return from the make_guess function, which itself returns True
    if it results in some progress, be that an assignment or an elimination of a possibility.
    """
    if verbose:
        print "-----------------------------------"
        print
        print "Exhausted basic logic, now trying trial and error..."
    for q in range(2, 10):
        if verbose:
            print "Looking for cells with %s possibilities..." % q
        for i in range(9):
            for j in range(9):
                if len(cell_poss[i][j]) == q:
                    for v in cell_poss[i][j]:
                        if make_guess(puzzle, i, j, v, guess_depth, cell_poss, val_loc, verbose):
                            return True
    return False


def is_valid(puzzle, cell_poss, val_loc):
    """Checks whether a puzzle is valid. Returns True or False.

    A puzzle is valid if these three conditions apply:
    1) It contains no instances of > 1 identical value in the same structure.
    2) It has no structures in which an unused number has no possible locations within the structure
    3) It has no incomplete cells with no possible digits that can go there.
    """
    for v in range(1, 10):
        for m in range(9):
            row_cont = [x for x in puzzle[m] if x != 0]
            if len(row_cont) != len(set(row_cont)):
                return False

            col_cont = [puzzle[x][m] for x in range(9) if puzzle[x][m] != 0]
            if len(col_cont) != len(set(col_cont)):
                return False

            clust_cont = [puzzle[i][j] for i, j in clust(m) if puzzle[i][j] != 0]
            if len(clust_cont) != len(set(clust_cont)):
                return False

            if not val_loc[0][m][v] and v not in row_cont:
                return False

            if not val_loc[1][m][v] and v not in col_cont:
                return False

            if not val_loc[2][m][v] and v not in clust_cont:
                return False

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0 and not cell_poss[i][j]:
                return False

    return True


def is_complete(puzzle):
    """Returns True when puzzle is completely filled in, False otherwise. (This could be an invalid solution.)
    """
    return all(0 not in r for r in puzzle)


def solving_algorithm(puzzle, verbose, guess_depth, cell_poss=None, val_loc=None):
    """Cycles through various algorithms until sudoku puzzle is solved, or the solver is stuck. Also returns validity.

    Optional argument verbosity causes the subroutines to print details of solving logic.
    Guess depth determines how many layers down of speculation the program will go, defaulted to 1. If guess depth is
    set to 0 or 1, this provides logic similar to what a person might be able to do. Higher guess depth (81 is equal to
    limitless guess depth) will provide faster solutions for very difficult puzzles, but they won't make human sense.

    The cell_poss and val_loc data structures can be passed in explicitly. This could be a time-saver for recursive
    guessing, but it's not yet implemented.

    Returns tuple of boolean values, where the first is whether the puzzle is completely filled in, second is whether
    the puzzle is valid, meaning it does not have an instance of two of the same digit in the same structure.
    """

    if cell_poss is None:
        cell_poss = init_cell_poss(puzzle)
    if val_loc is None:
        val_loc = init_val_loc(cell_poss)

    while True and not is_complete(puzzle):
        if check_for_single_poss(puzzle, cell_poss, val_loc, verbose):
            continue
        if check_for_single_val_loc(puzzle, cell_poss, val_loc, verbose):
            continue
        if guess_depth > 0 and try_all_guesses(puzzle, guess_depth, cell_poss, val_loc, verbose):
            continue
        break

    completeness = is_complete(puzzle)
    validity = is_valid(puzzle, cell_poss, val_loc)

    return completeness, validity


def solve(puzzle, verbose=False, guess_depth=1):
    """Prints puzzle, tries to solve it, and prints either solution or terminal state if it fails to solve the puzzle.

    If verbose is True, it also prints the step-by-step process.

    guess_depth determines how many successive guesses the algorithm will make before getting something conclusive.
    """
    print "-----------------------------------"
    print "            New puzzle"
    print "-----------------------------------"
    print_puzzle(puzzle)

    complete, valid = solving_algorithm(puzzle, verbose, guess_depth)

    print "-----------------------------------"
    print

    if not valid:
        if not complete:
            print "Impossible puzzle or error in solving logic. Invalid state reached in incomplete solution:"
        else:
            print "Impossible puzzle or error in solving logic. Invalid state in complete solution:"
    else:
        if not complete:
            print "Got stuck. Final state reached:"
        else:
            print "Solution:"

    print_puzzle(puzzle)


# From www.websudoku.com
medium_puzzle = [[2, 8, 7, 5, 1, 3, 0, 0, 0],
                 [0, 5, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 2, 0, 0, 0, 7, 0],
                 [0, 0, 0, 0, 0, 2, 3, 0, 9],
                 [8, 9, 1, 0, 0, 0, 4, 2, 7],
                 [7, 0, 2, 4, 0, 0, 0, 0, 0],
                 [0, 7, 0, 0, 0, 9, 0, 0, 0],
                 [4, 0, 0, 0, 0, 0, 0, 5, 0],
                 [0, 0, 0, 6, 5, 4, 7, 3, 8]]

# From PE, problem ninety-six (obfuscated a bit to make it less likely to come up in a google search)
hard_puzzle = [[0, 0, 1, 0, 0, 7, 0, 9, 0],
               [5, 9, 0, 0, 8, 0, 0, 0, 1],
               [0, 3, 0, 0, 0, 0, 0, 8, 0],
               [0, 0, 0, 0, 0, 5, 8, 0, 0],
               [0, 5, 0, 0, 6, 0, 0, 2, 0],
               [0, 0, 4, 1, 0, 0, 0, 0, 0],
               [0, 8, 0, 0, 0, 0, 0, 3, 0],
               [1, 0, 0, 0, 2, 0, 0, 7, 9],
               [0, 2, 0, 7, 0, 0, 4, 0, 0]]


# From http://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html
very_hard_puzzle = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 3, 6, 0, 0, 0, 0, 0],
                    [0, 7, 0, 0, 9, 0, 2, 0, 0],
                    [0, 5, 0, 0, 0, 7, 0, 0, 0],
                    [0, 0, 0, 0, 4, 5, 7, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 3, 0],
                    [0, 0, 1, 0, 0, 0, 0, 6, 8],
                    [0, 0, 8, 5, 0, 0, 0, 1, 0],
                    [0, 9, 0, 0, 0, 0, 4, 0, 0]]


# solve(medium_puzzle, True)
# solve(hard_puzzle, True)
# solve(very_hard_puzzle)  # This fails to find a solution--can't solve this one with the default guess depth of one!
# solve(very_hard_puzzle, True, 4)  # This works fine, though a depth of 10 makes it four times faster.
