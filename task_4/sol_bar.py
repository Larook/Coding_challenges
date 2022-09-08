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

    def __init__(self):
        self.N_ID = 0

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
        # def __init__(self, pellets, step, taken_actions):
        # def __init__(self, pellets, step):
        # def __init__(self, n_id, pellets, step, hist_pellets):
        def __init__(self, n_id, pellets, step, hist_pellets, hist_actions):

            self.id = n_id
            self.pellets = pellets
            self.step = step
            self.state = FuelInjector().get_state_pellets(self.pellets)
            self.hist_actions = hist_actions
            self.hist_pellets = hist_pellets


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
        hist_actions = []

        hist_pellets = []
        step = 0
        # node_init = FuelInjector.Node(pellets_init, step, actions_taken)
        # node_init = FuelInjector.Node(self.N_ID, pellets_init, step, hist_pellets)
        node_init = FuelInjector.Node(self.N_ID, pellets_init, step, hist_pellets, hist_actions)
        self.N_ID += 1
        nodes_to_visit.append(node_init)

        # add for DFS
        children = self.create_children(node_init)
        for child in children:
            nodes_to_visit.append(child)

        nodes_solution = []

        stop_search = False
        # while nodes_to_visit != []:
        while not stop_search:
            # for i in r_len_nodes_to_visit:
            node_visit = nodes_to_visit[0]

            if node_visit.state == self.STATE_SOLVED:
                # todo: make sure that the same node.id will not be added to the solutions
                nodes_solution.append(node_visit)
                # if len(nodes_solution) > 100000000:
                nodes_to_visit.pop(0)

                if len(nodes_solution) > 1:
                    stop_search = True
                    # break

                continue


            """
            BFS -- shallowest solution (GREAT), but the performance...
            filter children doubles take too much time, so can improve creating children!!
            """
            children = self.create_children(node_visit)
            children = self.filter_children_doubles(children, nodes_checked)
            nodes_to_visit.pop(0)
            nodes_to_visit.extend(children)

            # DFS -- can be fast? but doesn't give any good solutions
            # can limit the search depth...
            # limit_d = 10
            # nodes_to_visit.pop(0)
            # children = self.create_children(node_visit)
            # for child in children:
            #     if child.step <= limit_d:
            #         nodes_to_visit.insert(0, child)
            #     else:
            #         cnt_exess += 1
            #         print 'stop investigating this node', cnt_exess
            #         pass

            # the answer is MCTS or A* -- both require heuristics

            # sort nodes to visit -- based on pellets
            # nodes_to_visit = self.sort_nodes_to_visit(nodes_to_visit, children)
            # r_len_nodes_to_visit = range(len(nodes_to_visit))

            nodes_checked.append(node_visit)
            if show_hist:
                print 'nodes_to_visit', [str(node) for node in nodes_to_visit], '\nnodes_checked', [str(node) for node in nodes_checked], '\n'


        if show_hist:
            print('nodes_solution', [str(node) for node in nodes_solution])
        # filter the shortest solution
        min_steps = 1000000000000000000000
        min_id = 10000000000000000000
        for i, node in enumerate(nodes_solution):
            if node.step <= min_steps:
                min_steps = node.step
                min_id = i

        best_sol = nodes_solution[min_id]
        return best_sol.step

    def create_children(self, node_parent):
        """
        make only smart children so less time iterating and checking later
        """
        children = []
        pellets_now = node_parent.pellets
        # possible_actions = self.get_possible_actions(node_parent.state)
        # possible_actions = self.get_possible_actions2(node_parent.state, pellets_now)
        possible_actions = self.get_possible_actions3(node_parent.state, pellets_now)
        for i, action in enumerate(possible_actions):
            if action == self.ACTION_ADD:
                pellets_kid = pellets_now + 1
            if action == self.ACTION_SUBTR:
                pellets_kid = pellets_now -1
            if action == self.ACTION_DIV:
                if pellets_now % 2 != 0:
                    raise 'Something wrong with pellets'
                pellets_kid = int(pellets_now / 2)
            # child = self.Node(pellets_kid, node_parent.step + 1, node_parent.taken_actions + [action])
            # child = self.Node(self.N_ID, pellets_kid, node_parent.step + 1, node_parent.hist_pellets + [node_parent.pellets])
            child = self.Node(self.N_ID, pellets_kid, node_parent.step + 1,
                              node_parent.hist_pellets + [node_parent.pellets], node_parent.hist_actions + [action])
            self.N_ID += 1
            children.append(child)
        return children

    def filter_children_doubles(self, children, nodes_checked):
        """
        return only the children that were not already checked
        """
        # pellets_visited = [node.pellets for node in nodes_checked]
        # pellets_children = [node.pellets for node in children]
        filtered_children = []
        # filtered_children2 = []

        for i, n_child in enumerate(children):
            unique = True
            """
            there might be a situation where 2 nodes have the same pellets but not the same steps
            then delete the longer one
            instead delete just dont add this new child (because it's implied that the CHILD has more steps)
            """
            for j, n_checked in enumerate(nodes_checked):
                if int(n_child.pellets) == int(n_checked.pellets):
                    # # checked one has the same pellets -- compare the steps
                    # new_hist = n_child.hist_actions
                    # old_hist = n_checked.hist_actions
                    # if n_child.hist_actions[:-1] == n_checked.hist_actions[:-1]:
                    #     # if n_child.step < n_checked.step:
                    #     #     filtered_children2.append(n_child)
                    #     # else:
                    #     #     filtered_children2.append(n_checked)
                    #     unique = False
                    #     break
                    unique = False
                    break
            if unique:
                filtered_children.append(n_child)

        return filtered_children

    def get_possible_actions(self, state_now,):
        """
        when ODD state -- cannot divide
        """


        if state_now == self.STATE_ODD_LOW or state_now == self.STATE_ODD_HIGH:
            return self.possible_actions[:-1]
        else:
            return self.possible_actions
        pass


    def get_possible_actions2(self, state_now, pellets=None):
        """
        when ODD state -- cannot divide

        what if we enable ADD only when distance to byte is 0 or 1?
        """
        possible_actions = []

        # check if can DIV
        if state_now == self.STATE_EVEN_LOW or state_now == self.STATE_EVEN_HIGH:
            possible_actions.append(self.ACTION_DIV)

        # check if can ADD
        dist_low, dist_high = get_dist_to_bytes(pellets)
        if dist_high == 1:
            possible_actions.append(self.ACTION_ADD)

        # add SUB only when not 2
        if pellets != 2:
            possible_actions.append(self.ACTION_SUBTR)


        # if state_now == self.STATE_ODD_LOW or state_now == self.STATE_ODD_HIGH:
        #     return self.possible_actions[:-1]
        # else:
        #     return self.possible_actions
        # pass
        return possible_actions

    def get_possible_actions3(self, state_now, pellets=None):
        """
        when Even -- just divide (even when 2)
        else: add and sub

        what if we enable ADD only when distance to byte is 0 or 1?
        """
        possible_actions = []

        # check if can DIV
        if pellets % 2 == 0:
            possible_actions.append(self.ACTION_DIV)

        else:
            # ADD when distance to byte?
            # dist_low, dist_high = get_dist_to_bytes(pellets)
            # if dist_high == 1:
            possible_actions.append(self.ACTION_ADD)

            # always SUB
            possible_actions.append(self.ACTION_SUBTR)
        return possible_actions

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
    test_inputs = ['213789']
    test_outputs = [25]
    for ipt, opt in zip(test_inputs, test_outputs):

        import time
        start_graph = time.time()
        sol = solution(ipt)
        time_graph = time.time() - start_graph
        print 'ipt', ipt, 'sol', sol, 'opt', opt
        print('time_graph', time_graph, 'sol', sol)

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