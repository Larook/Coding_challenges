"""

Table:
-------------------------
| 0| 1| 2| 3| 4| 5| 6| 7|
-------------------------
| 8| 9|10|11|12|13|14|15|
-------------------------
|16|17|18|19|20|21|22|23|
-------------------------
|24|25|26|27|28|29|30|31|
-------------------------
|32|33|34|35|36|37|38|39|
-------------------------
|40|41|42|43|44|45|46|47|
-------------------------
|48|49|50|51|52|53|54|55|
-------------------------
|56|57|58|59|60|61|62|63|
-------------------------


Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(0, 1)
Output:
    3

Input:
solution.solution(19, 36)
Output:
    1
"""

import numpy as np
from array import *
from copy import deepcopy


def sum_arrays_elementwise(a, b):
    """ works like np.sum(arr1, arr2) """
    assert len(a) == len(b)
    c = deepcopy(a)
    for i in range(len(a)):
        c[i] = a[i] + b[i]
    return c


class Chessboard():
    """
    the chessboard knight movements solving
    """

    def __init__(self, grid_dim=8):
        self.grid_dim = grid_dim
        self.board = np.arange(self.grid_dim**2).reshape((self.grid_dim, self.grid_dim))
        self.history = []

    def is_within(self, pos):
        return 0 <= pos <= self.grid_dim - 1

    def get_nexts(self, src):
        """
        returns the possible fields that the knight can occupy given the current position
        """

        # translate current field of the chessboard to position in rows and columns
        pos_r, pos_c = np.where(self.board == src)
        pos_r, pos_c = pos_r[0], pos_c[0]

        """
        checking if can make moves
        Each move --> 2 steps in first direction and 1 in the following (just to unify the notation)
        Can be represented smarter???
        """
        next_moves_legal = []

        # can left-down?
        can_l_d = self.is_within(pos_r+1) and self.is_within(pos_c-2)
        if can_l_d:
            next_moves_legal.append(self.board[pos_r+1][pos_c-2])
        # can left-up?
        can_l_u = self.is_within(pos_r-1) and self.is_within(pos_c-2)
        if can_l_u:
            next_moves_legal.append(self.board[pos_r-1][pos_c-2])

        # can up-left?
        can_u_l = self.is_within(pos_r-2) and self.is_within(pos_c-1)
        if can_u_l:
            next_moves_legal.append(self.board[pos_r-2][pos_c-1])
        # can up-right?
        can_u_r = self.is_within(pos_r-2) and self.is_within(pos_c+1)
        if can_u_r:
            next_moves_legal.append(self.board[pos_r-2][pos_c+1])

        # can right-up?
        can_r_u = self.is_within(pos_r-1) and self.is_within(pos_c+2)
        if can_r_u:
            next_moves_legal.append(self.board[pos_r-1][pos_c+2])
        # can right-down?
        can_r_d = self.is_within(pos_r+1) and self.is_within(pos_c+2)
        if can_r_d:
            next_moves_legal.append(self.board[pos_r+1][pos_c+2])

        # can down-right?
        can_d_r = self.is_within(pos_r+2) and self.is_within(pos_c+1)
        if can_d_r:
            next_moves_legal.append(self.board[pos_r+2][pos_c+1])
        # can down-left?
        can_d_l = self.is_within(pos_r+2) and self.is_within(pos_c-1)
        if can_d_l:
            next_moves_legal.append(self.board[pos_r+2][pos_c-1])

        return next_moves_legal


def solution(src, dest):
    """
    param:
    src - index of starting position in the table
    dest - index of destination position

    returns:
    turns - the least amount of turns in the knight-L shape
    """
    chessboard = Chessboard()
    solutions = []

    to_visit = [src]
    actions_taken = [0]

    i = 0
    while i < len(to_visit):
        current_actions = actions_taken[i]
        current_tile = to_visit[i]

        # for current_actions, current_tile in zip(actions_taken, to_visit):
        chessboard.history.append({'current_actions': current_actions, 'current_tile': current_tile})
        # print('self.history', self.history)

        if current_tile == dest:
            print('found solution', chessboard.history[-1])
            solutions.append(chessboard.history[-1])
            break
        else:
            # if not found solution -- add possible actions (children) to the end of search space
            children = chessboard.get_nexts(current_tile)
            """ 
            adding at the end of the list -> BFS, if added to the beginning of the list -> DFS 
            """
            to_visit.extend(children)

            # additionally we know it will take to +1 action to go to children node
            acts_new = np.ones(len(children))
            acts_current = np.full(acts_new.shape, current_actions)
            actions_taken.extend(np.add(acts_new, acts_current))  # this line causes problems!!!
        i += 1

    print('Finished')
    # is it the smallest number of moves possible? For now just any moves giving task completion
    no_actions = int(chessboard.history[-1]['current_actions'])
    return no_actions


if __name__ == "__main__":
    test_1 = solution(0, 1)
    print 'test_1', test_1
    assert test_1 == 3

    test_2 = solution(19, 36)
    print 'test_2', test_2
    assert test_2 == 1

    print('passed!')





