"""
passes tests: 1,2,8

need to move to A*

Passes 1,2,8,9,10
so probably still some mistakes in the heuristics
"""
import copy
# import sys

show_hist = False

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
    low_thresh = 3 ## 4 passes 10th Test

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
        BFS, DFS, A*
        """
        nodes_checked = []
        nodes_to_visit = []
        actions_taken = []
        step = 0
        node_init = FuelInjector.Node(pellets_init, step, actions_taken)
        nodes_to_visit.append(node_init)

        nodes_solution = []

        stop_search = False
        # while nodes_to_visit != []:
        while not stop_search:
            # for i in r_len_nodes_to_visit:
            node_visit = nodes_to_visit[0]

            if node_visit.state == self.STATE_SOLVED:
                nodes_solution.append(node_visit)
                # if len(nodes_solution) > 100000000:
                if len(nodes_solution) > 0:
                    # break
                    stop_search = True
                continue

            children = self.create_children(node_visit)
            children = self.filter_children_doubles(children, nodes_checked)

            # BFS -- shallowest solution (GREAT)
            nodes_to_visit.pop(0)
            nodes_to_visit.extend(children)

            # DFS -- can be fast?
            # nodes_to_visit.pop(0)
            # for child in children:
            #     nodes_to_visit.insert(0, child)


            # sort nodes to visit -- based on pellets
            # nodes_to_visit = self.sort_nodes_to_visit(nodes_to_visit, children)
            # r_len_nodes_to_visit = range(len(nodes_to_visit))

            nodes_checked.append(node_visit)
            if show_hist:
                print 'nodes_to_visit', [str(node) for node in nodes_to_visit], '\nnodes_checked', [str(node) for node in nodes_checked], '\n'


        if show_hist:
            print('nodes_solution', [str(node) for node in nodes_solution])
        # filter the shortest solution
        min_steps = 100000000
        min_id = 100000000
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
                pellets_kid = pellets_now -1
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
        filtered_children2 = []

        for i, n_child in enumerate(children):
            unique = True
            """
            there might be a situation where 2 nodes have the same pellets but not the same steps
            then delete the longer one
            instead delete just dont add this new child (because it's implied that it has more steps)
            """
            for j, n_checked in enumerate(nodes_checked):
                if int(n_child.pellets) == int(n_checked.pellets):
                    # checked one has the same pellets -- compare the steps
                    # if n_child.step < n_checked.step:
                    #     filtered_children2.append(n_child)
                    # else:
                    #     filtered_children2.append(n_checked)

                    unique = False
                    break
            if unique:
                filtered_children.append(n_child)

        return filtered_children

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
                byte_high = pow(2, i+1)
                if byte_low < self.pellets_now < byte_high:
                    dist_low = self.pellets_now - byte_low
                    dist_high = byte_high - self.pellets_now
                    if show_hist:
                        print 'pellets=', self.pellets_now, 'dist_low=', dist_low, byte_low, 'dist_high=', dist_high, byte_high
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

    def sort_nodes_to_visit(self, nodes_to_visit, children):
        """
        put the new kids which had 'divide' action on front

        or just sort by:
        - least steps & least pellets
        """
        sorted_nodes = copy.deepcopy(nodes_to_visit)
        # for i, child in enumerate(children):
        #     # there will be only one kid with divide -- the least pellets_smallest already
        #     if child.taken_actions[-1] == self.ACTION_DIV:
        #         sorted_nodes.insert(0, child)
        #         children.__delitem__(i)

        """
        sort distance wise
        first -- the ones +-1 to byte
        then the lower ones
        """
        sorted_children_byte = []
        for i, child in enumerate(children):
            # then add the SUBTR at the almost last place and ADD as last place(unless close to byte)
            dist_low, dist_high = get_dist_to_bytes(child.pellets)
            if dist_high == 0 or dist_low == 0:
                sorted_nodes.insert(0, children[i])
                children.__delitem__(i)
            elif dist_high == 1 or dist_low == 1:
                sorted_children_byte.insert(0, children[i])
                children.__delitem__(i)

        pellets_children = [child.pellets for child in children]
        pellets_children.sort()
        sorted_children_pellets = []
        for i, pellets_smallest in enumerate(pellets_children):
            for j, child in enumerate(children):
                if pellets_smallest == child.pellets:
                    sorted_children_pellets.insert(i, child)

        nodes_to_visit_sorted = sorted_nodes + sorted_children_byte
        nodes_to_visit_sorted = nodes_to_visit_sorted + sorted_children_pellets
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
        print 'ipt', ipt, 'sol', sol, 'opt', opt
        if sol != opt:
            # raise Warning("Test failed!")
            print 'TEST FAILED'

"""
Test
1 - OK
2 - OK
3
4 - OK
5
6
7
8 - OK
9
10 - OK
"""