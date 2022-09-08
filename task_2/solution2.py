"""
passes tests: 1,2,8

need to move to A*

Passes 1,2,8,9,10
so probably still some mistakes in the heuristics
"""
import copy
import sys

show_hist = True


def get_dist_to_bytes(pellets_now):
    # find the closest powers of 2
    for i in range(0, 1028):
        byte_low = pow(2, i)
        byte_high = pow(2, i + 1)
        if byte_low <= pellets_now <= byte_high:
            dist_low = pellets_now - byte_low
            dist_high = byte_high - pellets_now
            return dist_low, dist_high
    # print("Couldnt find bytes distance???")
    raise Warning("Couldnt find bytes distance???")


class FuelInjector:
    pellets_init = 0
    history = []
    pellets_now = pellets_init

    ACTION_ADD = 0
    ACTION_SUBTR = 1
    ACTION_DIV = 2
    possible_actions = (ACTION_ADD, ACTION_SUBTR, ACTION_DIV)
    action_reward_raw = {ACTION_ADD: 0, ACTION_SUBTR: 0, ACTION_DIV: 0}

    """
    due to the HUGE state space we need to reduce it
    States:
    0 - solved
    1 - even number and GT 2
    2 - odd number and GT 2
    3 - even number and LE 2
    4 - odd number and LE 2
    """
    STATE_SOLVED = 0
    STATE_EVEN_HIGH = 1
    STATE_ODD_HIGH = 2
    STATE_EVEN_LOW = 3
    STATE_ODD_LOW = 4
    possible_states = (STATE_SOLVED, STATE_EVEN_HIGH, STATE_ODD_HIGH, STATE_EVEN_LOW, STATE_ODD_LOW)
    # low_thresh = 2
    low_thresh = 3  ## 4 passes 10th Test

    Q_table = []

    # def __init__(self, pellets):
    #     self.pellets_init = int(pellets)
    #     self.pellets_now = int(pellets)
    #     self.state_now = self.get_state_pellets(self.pellets_now)
    #     self.history.append({'step': 0, 'pellets': self.pellets_now, 'state': self.state_now, 'taken_actions': []})
    #     # print self.history[-1]
    #
    #     # # init Q table
    #     # for r, state in enumerate(self.possible_states):
    #     #     row = []
    #     #     for c, action in enumerate(self.possible_actions):
    #     #         row.append(action)
    #     #     self.Q_table.append(row)

    def get_state_pellets(self, pellets):
        """
         due to the HUGE state space we need to reduce it
        """
        if pellets == 1:
            return self.STATE_SOLVED

        if pellets >= self.low_thresh:
            if pellets % 2 == 1:
                return self.STATE_ODD_HIGH
            else:
                return self.STATE_EVEN_HIGH
        else:
            if pellets % 2 == 1:
                return self.STATE_ODD_LOW
            else:
                return self.STATE_EVEN_LOW

    def take_action(self, a):
        """
        0 - add one fuel pellet
        1 - subtract one fuel pellet
        2 - divide by 2
        """
        if a == self.ACTION_ADD:
            self.pellets_now += 1
        if a == self.ACTION_SUBTR:
            self.pellets_now -= 1
        if a == self.ACTION_DIV:
            self.pellets_now /= 2

    class Node:
        def __init__(self, pellets, step, taken_actions):
            self.pellets = pellets
            self.step = step
            self.state = FuelInjector().get_state_pellets(self.pellets)
            self.taken_actions = taken_actions

        def get_node(self):
            """ returns a node in form of dictionary """
            return str(self.__dict__)

        def __str__(self):
            return str(self.__dict__)

    def solve_fuel_pellets_graph(self, pellets_init):
        """
        Graph search approach
        """
        nodes_checked = []
        nodes_to_visit = []
        actions_taken = []
        step = 0
        node_init = FuelInjector.Node(pellets_init, step, actions_taken)  # automatically calculates state
        nodes_to_visit.append(node_init)

        nodes_solution = []

        stop_search = False
        while not stop_search:
            node_visit = nodes_to_visit[0]  # take from head (already has state)

            if node_visit.state == self.STATE_SOLVED:
                nodes_solution.append(node_visit)
                if len(nodes_solution) > 3:
                    stop_search = True
                continue

            # if it wasn't a solution --> check children
            nodes_to_visit.pop(0)  # already visited
            children = self.create_children(node_visit)
            children = self.filter_children_doubles(children, nodes_checked)  # remove already visited

            # sort nodes to visit -- based on pellets
            nodes_to_visit = self.sort_nodes_to_visit(nodes_to_visit, children)

            nodes_checked.append(node_visit)
            if show_hist:
                print
                'nodes_to_visit', [str(node) for node in nodes_to_visit], '\nnodes_checked', [str(node) for node in
                                                                                              nodes_checked], '\n'

        if show_hist:
            print('nodes_solution', [str(node) for node in nodes_solution])
        # filter the shortest solution
        min_steps = 99999999999999999999
        min_id = 99999999999999999999
        for i, node in enumerate(nodes_solution):
            if node.step <= min_steps:
                min_steps = node.step
                min_id = i
        return nodes_solution[min_id].step

    def create_children(self, node_parent):
        children = []
        pellets_now = node_parent.pellets
        possible_actions = self.get_possible_actions(node_parent.state)
        for action in possible_actions:
            if action == self.ACTION_ADD:
                pellets_kid = pellets_now + 1
            if action == self.ACTION_SUBTR:
                pellets_kid = pellets_now - 1
            if action == self.ACTION_DIV:
                pellets_kid = pellets_now / 2
            child = self.Node(pellets_kid, node_parent.step + 1, node_parent.taken_actions + [action])
            children.append(child)
        return children

    def filter_children_doubles(self, children, nodes_checked):
        """
        return only the children that were not already checked
        """
        # pellets_visited = [node.pellets for node in nodes_checked]
        # pellets_children = [node.pellets for node in children]
        filtered_children = []

        for n_child in children:
            unique = True
            for n_checked in nodes_checked:
                if n_child.pellets == n_checked.pellets:
                    unique = False
                    break
            if unique:
                filtered_children.append(n_child)

        return filtered_children

    def solve_fuel_pellets_rl(self):
        """
        Reinforcement Learning approach

        State -> Action -> Reward_1 -> State_1 -> Action_1 -> Reward_2 -> ...
        """
        # max_episodes = 100
        max_episodes = 1
        for episode in range(max_episodes):
            is_solved = False
            taken_actions = []
            step = 1
            while not is_solved:
                #
                action_reward = copy.deepcopy(self.action_reward_raw)
                state_now = self.state_now
                is_solved = state_now == self.STATE_SOLVED

                if not is_solved:
                    # check possible rewards for each action

                    # a_best = self.choose_greedy_from_possible(state_now, action_reward)
                    a_best = self.get_action_distance_byte()

                    # execute action
                    self.take_action(a_best)
                    taken_actions.append(a_best)

                self.state_now = self.get_state_pellets(self.pellets_now)
                self.history.append(
                    {'step': step, 'pellets': self.pellets_now, 'state': state_now, 'taken_actions': taken_actions})
                if show_hist:
                    print
                    self.history[-1]
                is_solved = self.state_now == self.STATE_SOLVED
                step += 1

            # having solution just return the least number of taken actions
            steps_taken_solution = self.history[-1]['step']
            return steps_taken_solution

    def choose_greedy(self, act_rew):
        """
        return action giving highest reward
        """
        act = False
        reward = 0
        for k in act_rew:
            if act_rew[k] > reward:
                act = k
                reward = act_rew[k]
        return act

    def get_reward(self, state_now, action):
        """
        possible_states = (STATE_SOLVED, STATE_EVEN_HIGH, STATE_ODD_HIGH, STATE_EVEN_LOW, STATE_ODD_LOW)
        possible_actions = (ACTION_ADD, ACTION_SUBTR, ACTION_DIV)
        """

        if state_now == self.STATE_SOLVED:
            return 1

        if state_now == self.STATE_EVEN_HIGH:
            if action == self.ACTION_ADD:
                return 0.3
            if action == self.ACTION_SUBTR:
                return 0.2
            if action == self.ACTION_DIV:
                return 0.9

        if state_now == self.STATE_ODD_HIGH:
            if action == self.ACTION_ADD:
                return 0.8
            if action == self.ACTION_SUBTR:
                return 0.6
            if action == self.ACTION_DIV:
                return 0.

        if state_now == self.STATE_EVEN_LOW:
            if action == self.ACTION_ADD:
                return 0.2
            if action == self.ACTION_SUBTR:
                return 0.7
            if action == self.ACTION_DIV:
                return 0.9

        if state_now == self.STATE_ODD_LOW:
            if action == self.ACTION_ADD:
                return 0.6
            if action == self.ACTION_SUBTR:
                return 0.8
            if action == self.ACTION_DIV:
                return 0.

        pass

    def get_possible_actions(self, state_now):
        """
        when ODD state -- cannot divide
        """
        if state_now == self.STATE_ODD_LOW or state_now == self.STATE_ODD_HIGH:
            return self.possible_actions[:-1]
        else:
            return self.possible_actions
        pass

    def get_action_distance_byte(self):
        """
        calculates the distance to the closest power of 2 representation
        """
        # if even just divide
        if self.pellets_now % 2 == 0:
            return self.ACTION_DIV

        else:
            # find the closest powers of 2
            for i in range(0, 1028):
                byte_low = pow(2, i)
                byte_high = pow(2, i + 1)
                if byte_low < self.pellets_now < byte_high:
                    dist_low = self.pellets_now - byte_low
                    dist_high = byte_high - self.pellets_now
                    if show_hist:
                        print
                        'pellets=', self.pellets_now, 'dist_low=', dist_low, byte_low, 'dist_high=', dist_high, byte_high
                    if dist_low == 1:
                        return self.ACTION_SUBTR
                    if dist_high == 1:
                        return self.ACTION_ADD
                    return self.ACTION_ADD

                    # # this passes only 1,2,8 tests
                    # if dist_low <= dist_high:
                    #     return self.ACTION_SUBTR
                    # else:
                    #     return self.ACTION_ADD

    def choose_greedy_from_possible(self, state, action_reward):
        for action in self.get_possible_actions(state):
            reward = self.get_reward(state, action)
            action_reward[action] = reward
        # best action
        a_best = self.choose_greedy(action_reward)
        return a_best

    def sort_nodes_to_visit(self, nodes_to_visit, children):
        """
        put the new kids which had 'divide' action on front
        """
        # sorted_nodes = copy.deepcopy(nodes_to_visit)
        # for i, child in enumerate(children):
        #     # there will be only one kid with divide -- the least pellets_smallest already
        #     if child.taken_actions[-1] == self.ACTION_DIV:
        #         sorted_nodes.insert(0, child)
        #         children.__delitem__(i)

        """
        sort distance wise
        first -- the ones +-1 to byte
        then the lower ones

        has to be in increasing order at the end
        """
        children_init = copy.deepcopy(children)
        sorted_children_byte = []
        for i, child in enumerate(children):
            # then add the SUBTR at the almost last place and ADD as last place(unless close to byte)
            dist_low, dist_high = get_dist_to_bytes(child.pellets)
            if dist_high == 0 or dist_low == 0:
                sorted_children_byte.insert(0, children[i])
                children.__delitem__(i)
            elif dist_high == 1 or dist_low == 1:
                sorted_children_byte.insert(0, children[i])
                children.__delitem__(i)
            # else:
            #     sorted_children_byte.append(children[i])

        # nodes_to_visit_sorted = sorted_nodes + sorted_children_byte
        nodes_to_visit_unsorted = nodes_to_visit + children
        pellets_nodes = [child.pellets for child in nodes_to_visit_unsorted]
        pellets_nodes.sort()

        sorted_nodes = []
        for i, pellets_smallest in enumerate(pellets_nodes):
            for j, child in enumerate(nodes_to_visit_unsorted):
                if pellets_smallest == child.pellets:
                    sorted_nodes.insert(i, child)

        nodes_to_visit_sorted = sorted_children_byte + sorted_nodes
        # nodes_to_visit_sorted = nodes_to_visit_sorted + sorted_nodes
        # return nodes_to_visit_sorted
        return nodes_to_visit_sorted


def solution(n):
    # Your code here
    assert len(str(n)) <= 309
    n = int(n)
    # solver = FuelInjector(n)
    # no_actions = solver.solve_fuel_pellets_rl()

    solver = FuelInjector()
    no_actions = solver.solve_fuel_pellets_graph(n)
    return no_actions


if __name__ == "__main__":

    # test_inputs = ['4', '15', '77', '135',]
    # test_outputs = [2, 5, 9, 9]
    test_inputs = ['135']
    test_outputs = [9]
    for ipt, opt in zip(test_inputs, test_outputs):
        sol = solution(ipt)
        print
        'ipt', ipt, 'sol', sol, 'opt', opt
        if sol != opt:
            # raise Warning("Test failed!")
            print
            'TEST FAILED'

"""
Test
1 - OK
2 - OK
3
4 - OK (not now)
5
6
7
8 - OK
9 - OK
10 - OK
"""

