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


def sum_arrays_elementwise(a, b):
    """
    works like np.sum([arr1, arr2], axis=0)
    """
    # assert len(a) == len(b)
    # c = []
    # for i in range(len(a)):
    #     c.append(a[i] + b[i])
    # return c
    return np.sum([a, b], axis=0)


class Chessboard:
    """
    the chessboard knight movements solving
    """

    def __init__(self, grid_dim=8):
        self.grid_dim = grid_dim
        self.board = self.create_chessboard()

    def create_chessboard(self):
        """
        using classical list,
        """
        # chessboard = []
        # field = 0
        # for i in range(self.grid_dim):
        #     row = []
        #     for j in range(self.grid_dim):
        #         row.append(field)
        #         field += 1
        #     chessboard.append(row)
        # return chessboard
        return np.arange(self.grid_dim ** 2).reshape((self.grid_dim, self.grid_dim))

    def get_row_col_field(self, field):
        """ works like np.where(board == field) """
        # for r in range(len(self.board)):
        #     for c in range(len(self.board[r])):
        #         if self.board[r][c] == field:
        #             return r, c
        r, c = np.where(self.board == field)
        return r[0], c[0]

    def is_within(self, pos):
        return 0 <= pos <= self.grid_dim - 1

    def get_nexts(self, src):
        """
        returns the possible fields that the knight can occupy given the current position
        Also checking if can make moves
        Each move --> 2 steps in first direction and 1 in the following (just to unify the notation)
        Can be represented smarter???
        """
        pos_r, pos_c = self.get_row_col_field(src)
        next_moves_legal = []

        # can left-down?
        can_l_d = self.is_within(pos_r + 1) and self.is_within(pos_c - 2)
        if can_l_d:
            next_moves_legal.append(self.board[pos_r + 1][pos_c - 2])
        # can left-up?
        can_l_u = self.is_within(pos_r - 1) and self.is_within(pos_c - 2)
        if can_l_u:
            next_moves_legal.append(self.board[pos_r - 1][pos_c - 2])

        # can up-left?
        can_u_l = self.is_within(pos_r - 2) and self.is_within(pos_c - 1)
        if can_u_l:
            next_moves_legal.append(self.board[pos_r - 2][pos_c - 1])
        # can up-right?
        can_u_r = self.is_within(pos_r - 2) and self.is_within(pos_c + 1)
        if can_u_r:
            next_moves_legal.append(self.board[pos_r - 2][pos_c + 1])

        # can right-up?
        can_r_u = self.is_within(pos_r - 1) and self.is_within(pos_c + 2)
        if can_r_u:
            next_moves_legal.append(self.board[pos_r - 1][pos_c + 2])
        # can right-down?
        can_r_d = self.is_within(pos_r + 1) and self.is_within(pos_c + 2)
        if can_r_d:
            next_moves_legal.append(self.board[pos_r + 1][pos_c + 2])

        # can down-right?
        can_d_r = self.is_within(pos_r + 2) and self.is_within(pos_c + 1)
        if can_d_r:
            next_moves_legal.append(self.board[pos_r + 2][pos_c + 1])
        # can down-left?
        can_d_l = self.is_within(pos_r + 2) and self.is_within(pos_c - 1)
        if can_d_l:
            next_moves_legal.append(self.board[pos_r + 2][pos_c - 1])

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
    states = []  # graph of visited nodes (field of the board) with the number of actions

    i = 0
    nodes = [src]
    actions_taken = [i]

    while i < len(nodes):
        action_no = actions_taken[i]
        current_field = nodes[i]
        states.append({'action_no': action_no, 'current_field': current_field})

        if int(current_field) == int(dest):
            break
        else:
            # if not found solution -- add possible actions (children) to the end of search space
            children = chessboard.get_nexts(current_field)
            """ 
            Adding at the end of the list -> BFS; if added to the beginning of the list -> DFS 
            Is it the smallest number of moves possible? BFS makes sure it is
            """
            nodes.extend(children)

            # additionally we know it will take to +1 action to go to children node, save it
            acts_new = [1 for child in children]
            acts_current = [action_no for child in children]
            actions_taken.extend(sum_arrays_elementwise(acts_new, acts_current))
        i += 1
    return int(states[-1]['action_no'])


if __name__ == "__main__":
    test_1 = solution(0, 1)
    print 'test_1', test_1
    assert test_1 == 3

    test_2 = solution(19, 36)
    print 'test_2', test_2
    assert test_2 == 1
