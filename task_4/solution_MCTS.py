"""
passes tests: 1,2,8

need to move to A*

Passes 1,2,8,9,10
so probably still some mistakes in the heuristics
"""
import copy

import numpy as np
from collections import defaultdict
show_hist = False


class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]


    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    def get_legal_actions(self):
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''

    def is_game_over(self):
        '''
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''

    def game_result(self):
        '''
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''

    def move(self, action):
        '''
        Modify according to your game or
        needs. Changes the state of your
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board
        position is empty. If you place x in
        row 2 column 3, then it would be some
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns
        the new state after making a move.
        '''

if __name__ == "__main__":
        initial_state = '213789'

        root = MonteCarloTreeSearchNode(state=initial_state)
        selected_node = root.best_action()
        print 'selected_node', selected_node

#
# def solution(n):
#     # Your code here
#     assert len(str(n)) <= 309
#     n = int(n)
#     # solver = FuelInjector(n)
#     # no_actions = solver.solve_fuel_pellets_rl()
#
#     solver = FuelInjector()
#
#     # nodes_solution = solver.solve_fuel_pellets_graph_BFS(n, no_solutions=1)
#     nodes_solution = solver.solve_fuel_pellets_graph(n, no_solutions=1)
#
#     best_solution = solver.get_best_solution(nodes_solution)
#     no_actions = best_solution.step
#     return no_actions
#
# def solution_shallowest(n):
#     n = int(n)
#     solver = FuelInjector()
#     best_solutions = solver.solve_fuel_pellets_graph_BFS(n)[0].step
#     return best_solutions
#
#
#
# if __name__ == "__main__":
#     import time
#
#     # test_inputs = ['4', '15', '77', '135', '217', '314', '2137', '213789']
#     # test_outputs = [2, 5, 9, 9, 11, 11, 15, 25]
#     test_inputs = ['213789']
#     test_outputs = [24]
#     for ipt, opt in zip(test_inputs, test_outputs):
#         # print 'ipt', ipt, 'sol', sol, 'opt', opt
#         print 'ipt', ipt
#
#         start_graph = time.time()
#         sol = solution(ipt)
#         # sol = None
#         time_graph = time.time() - start_graph
#         print('time_graph', time_graph, 'sol', sol)
#
#         start_bfs = time.time()
#         sol_bfs = solution_shallowest(ipt)
#         time_bfs = time.time() - start_bfs
#         print('time_bfs', time_bfs, 'sol', sol_bfs)
#         if sol != opt:
#             # raise Warning("Test failed!")
#             print 'TEST FAILED'
#
# """
# Test
# 1 - OK
# 2 - OK
# 3
# 4 - OK
# 5
# 6
# 7
# 8 - OK
# 9
# 10 - OK
# """