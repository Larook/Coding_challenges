"""
passes tests: 1,2,8

need to move to A*

Passes 1,2,8,9,10
so probably still some mistakes in the heuristics
"""
import copy

show_hist = False
# todo: Make sure that doubled nodes are filtered out properly


def get_dist_to_bytes(pellets_now):
    """ find the closest powers of 2"""
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
    parent_last_act = None

    ACTION_ADD = 0
    ACTION_SUBTR = 1
    ACTION_DIV = 2
    possible_actions = (ACTION_ADD, ACTION_SUBTR, ACTION_DIV)

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
    low_thresh = 3  ## 4 passes 10th Test

    def __init__(self, is_bfs):
        self.N_ID = 0
        self.is_bfs = is_bfs


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


    class Node:
        def __init__(self, n_id, pellets, step, hist_pellets, hist_actions):

            self.id = n_id
            self.pellets = pellets
            self.step = step
            self.state = FuelInjector(is_bfs=False).get_state_pellets(self.pellets)
            self.hist_actions = hist_actions
            self.hist_pellets = hist_pellets

            self.h_cost_now = self.get_node_cost_now()
            self.g_cost_hist = 0

        def get_node_cost_now(self):
            dist = min(get_dist_to_bytes(self.pellets))
            if dist == 0:
                return 0
            else:
                h = 0.8 * self.pellets + 10 * self.step + 1 * dist
            return h

        def __str__(self):
            return str(self.__dict__)

    def solve_fuel_pellets_graph(self, pellets_init, no_solutions):
        """
        Graph search approach
        BFS, DFS, A*
        """
        nodes_solution = []

        nodes_checked = []
        nodes_to_visit = []
        hist_actions = []

        hist_pellets = []
        step = 0
        node_init = FuelInjector.Node(self.N_ID, pellets_init, step, hist_pellets, hist_actions)
        self.N_ID += 1
        # nodes_to_visit.append(node_init)

        # add for start
        if not self.is_bfs:
            children = self.create_children(node_init, act_fun=self.get_possible_actions_no_redo)
            # children = self.create_children(node_init, act_fun=self.get_possible_actions3)
        else:
            children = self.create_children(node_init, act_fun=self.get_possible_actions_no_redo)
        for child in children:
            nodes_to_visit.append(child)

        stop_search = False
        while not stop_search:
            if len(nodes_to_visit) == 0:
                stop_search = True
                break

            node_visit = nodes_to_visit[0]
            self.parent_last_act = node_visit.hist_actions[-1]
            nodes_to_visit.pop(0)
            if node_visit.state == self.STATE_SOLVED:
                # todo: make sure that the same node.id will not be added to the solutions
                nodes_solution.append(node_visit)
                if len(nodes_solution) >= no_solutions:
                    stop_search = True
                    # break
                continue

            """
            BFS -- shallowest solution (GREAT), but the performance...
            filter children doubles take too much time, so can improve creating children! ~ done

            solution is heuristics!
            the answer is MCTS or A* -- both require heuristics
            nodes_to_visit = self.sort_nodes_to_visit(nodes_to_visit, children)
            """
            if self.is_bfs:
                children = self.create_children(node_visit, act_fun=self.get_possible_actions_bfs)
                # children = self.filter_children_doubles(children, nodes_checked)
                nodes_to_visit.extend(children)
            else:
                # children = self.create_children(node_visit, act_fun=self.get_possible_actions3)
                # children = self.create_children(node_visit, act_fun=self.get_possible_actions_bfs)
                # children = self.create_children(node_visit, act_fun=self.get_possible_actions_legal)
                children = self.create_children(node_visit, act_fun=self.get_possible_actions_no_redo)
                # children = self.create_children(node_visit, act_fun=self.get_possible_actions_pref_sub)
                # children = self.create_children(node_visit, act_fun=self.get_possible_actions_bfs)

                children = self.filter_children_doubles(children, nodes_checked)
                # todo: proper heuristics
                # nodes_to_visit = self.sort_nodes_to_visit(nodes_to_visit, children)
                # nodes_to_visit = self.sort_nodes_to_visit2(nodes_to_visit)
                # nodes_to_visit = self.sort_nodes_to_visit3(nodes_to_visit, children)
                nodes_to_visit = self.sort_nodes_to_visit4(nodes_to_visit, children)
                # nodes_to_visit.extend(children)


            nodes_checked.append(node_visit)
            if show_hist:
                print
                'nodes_to_visit', [str(node) for node in nodes_to_visit], '\nnodes_checked', [str(node) for node in
                                                                                              nodes_checked], '\n'
        return nodes_solution


    def create_children(self, node_parent, act_fun):
        """
        make only smart children so less time iterating and checking later
        """
        children = []
        pellets_now = node_parent.pellets
        # possible_actions = self.get_possible_actions(node_parent.state)
        # possible_actions = self.get_possible_actions2(node_parent.state, pellets_now)
        # possible_actions = self.get_possible_actions3(pellets_now)
        parents_hist = node_parent.hist_actions
        # if len(node_parent.hist_actions) > 0 and not self.is_bfs:
        #     possible_actions = act_fun(pellets_now)
            # possible_actions = self.get_possible_actions_bfs(pellets_now)
        # else:
        #     possible_actions = self.get_possible_actions_bfs(pellets_now)
        # possible_actions = self.get_possible_actions_bar(pellets_now)
        possible_actions = act_fun(pellets_now)

        # possible_actions = self.get_possible_actions_bar(pellets_now)
        for i, action in enumerate(possible_actions):
            if action == self.ACTION_ADD:
                pellets_kid = pellets_now + 1
            if action == self.ACTION_SUBTR:
                pellets_kid = pellets_now - 1
            if action == self.ACTION_DIV:
                if pellets_now % 2 != 0:
                    raise 'Something wrong with pellets'
                pellets_kid = int(pellets_now / 2)
            # child = self.Node(pellets_kid, node_parent.step + 1, node_parent.taken_actions + [action])
            # child = self.Node(self.N_ID, pellets_kid, node_parent.step + 1, node_parent.hist_pellets + [node_parent.pellets])
            child = self.Node(self.N_ID, pellets_kid, node_parent.step + 1,
                              node_parent.hist_pellets + [node_parent.pellets], node_parent.hist_actions + [action])
            # add historical cost from all the
            child.g_cost_hist = node_parent.h_cost_now + child.h_cost_now
            self.N_ID += 1
            children.append(child)
        return children

    def filter_children_doubles(self, children, nodes_checked):
        """
        return only the children that were not already checked
        """

        # filter out doubles inside children
        children = self.get_children_unique_itself(children)

        # filter out doubles inside nodes_checked
        children = self.get_children_not_in_visited(children, nodes_checked)

        return children

    def get_possible_actions_legal(self, pellets):
        """
        when ODD state -- cannot divide
        everything else goes
        """

        possible_actions = []
        # check if can DIV
        if pellets % 2 == 0:
            possible_actions.append(self.ACTION_DIV)

        # always ADD
        possible_actions.append(self.ACTION_ADD)
        # always SUB
        possible_actions.append(self.ACTION_SUBTR)
        return possible_actions

    def get_possible_actions2(self, pellets):
        """
        when ODD state -- cannot divide

        what if we enable ADD only when distance to byte is 0 or 1?
        """
        possible_actions = []

        # check if can DIV
        if pellets % 2 == 0:
            possible_actions.append(self.ACTION_DIV)
        else:
            # add SUB only when not 2
            # if pellets != 2:
            possible_actions.append(self.ACTION_SUBTR)

        # check if can ADD
        dist_low, dist_high = get_dist_to_bytes(pellets)
        if dist_high == 1:
            possible_actions.append(self.ACTION_ADD)

        # if state_now == self.STATE_ODD_LOW or state_now == self.STATE_ODD_HIGH:
        #     return self.possible_actions[:-1]
        # else:
        #     return self.possible_actions
        # pass
        return possible_actions

    def get_possible_actions3(self, pellets):
        """
        when Even -- just divide (even when 2)
        else:
            sub - always
            add - only when dist_byte

        what if we enable ADD only when distance to byte is 0 or 1?
        """
        possible_actions = []

        # check if can DIV
        if pellets % 2 == 0:
            possible_actions.append(self.ACTION_DIV)
            # if this is already a byte dont bother with other actions!
            return possible_actions

        else:
            # ADD when distance to byte?
            dist_low, dist_high = get_dist_to_bytes(pellets)

            if dist_high == 1:
                # if can go up to the byte, then go
                possible_actions.append(self.ACTION_ADD)
            else:
                # always SUB
                possible_actions.append(self.ACTION_SUBTR)

        # else:
        #     # ADD when distance to byte?
        #     dist_low, dist_high = get_dist_to_bytes(pellets)
        #     if dist_high == 1 or dist_low == 1:
        #         if dist_high == 1:
        #             possible_actions.append(self.ACTION_ADD)
        #             return possible_actions
        #         else:
        #             possible_actions.append(self.ACTION_SUBTR)
        #             return possible_actions
        #     else:
        #         # if (pellets+1)%2 == 0:
        #         possible_actions.append(self.ACTION_ADD)
        #
        #         # always SUB
        #         possible_actions.append(self.ACTION_SUBTR)


        return possible_actions

    def get_possible_actions_pref_sub(self, pellets):
        """
        no_redo but prefer subtract
        """
        possible_actions = []
        # check if can DIV
        if pellets % 2 == 0:
            possible_actions.append(self.ACTION_DIV)
            # if this is already a byte dont bother with other actions!
            # return possible_actions
        else:
            # ADD when distance to byte?
            dist_low, dist_high = get_dist_to_bytes(pellets)
            # ADD
            if dist_high == 1:
            # if can go up to the byte, then go
                possible_actions.append(self.ACTION_ADD)
            # else:
            # SUB
            if self.parent_last_act != self.ACTION_ADD:
                possible_actions.append(self.ACTION_SUBTR)

        return possible_actions

    def get_possible_actions_no_redo(self, pellets):
        """
        when Even -- just divide (even when 2)
        else:
            do not go back to the previous state!!!
                if prev_action was ADD -> do not allow for SUBSTR
                if prev_action was SUBSTR -> do not allow for ADD
        """
        possible_actions = []

        # check if can DIV
        if pellets % 2 == 0:
            possible_actions.append(self.ACTION_DIV)
            # if this is already a byte dont bother with other actions!
            # return possible_actions

        else:
            # ADD when distance to byte?
            # dist_low, dist_high = get_dist_to_bytes(pellets)

            # ADD
            # if dist_high == 1:
                # if can go up to the byte, then go
            if self.parent_last_act != self.ACTION_SUBTR:
                possible_actions.append(self.ACTION_ADD)
            # else:
            # SUB
            if self.parent_last_act != self.ACTION_ADD:
                possible_actions.append(self.ACTION_SUBTR)

        return possible_actions


    def get_possible_actions_bfs(self, pellets):
        """
        when Even -- just divide (even when 2)
        always: add and sub
        """
        possible_actions = []
        # check if can DIV
        if pellets % 2 == 0:
            possible_actions.append(self.ACTION_DIV)

        else:
            # always ADD
            possible_actions.append(self.ACTION_ADD)

            # always SUB
            possible_actions.append(self.ACTION_SUBTR)
        return possible_actions

    def sort_nodes_to_visit2(self, nodes_to_visit):
        """
        put the new kids which had 'divide' action on front

        or just sort by:
        - least steps & least pellets
        """

        if len(nodes_to_visit) <= 1:
            return nodes_to_visit
        else:
            # just code for other way of distance calculation
            # distances = []
            # for node_ in nodes_to_visit:
            #     dist = 10
            #     for i in range(3):
            #         if node_.pellets + i % 2 == 0:
            #             dist = i
            #         elif node_.pellets - i % 2 == 0:
            #             dist = -i
            #     distances.append(dist)

            # calculate h
            nodes_to_sort = nodes_to_visit
            nodes_to_sort_init = copy.deepcopy(nodes_to_visit)
            costs_to_sort = []
            for i, node_ in enumerate(nodes_to_sort):
                # there will be only one kid with divide -- the least pellets_smallest already
                # costs_to_sort.append(node_.h_cost_now)
                costs_to_sort.append(node_.g_cost_hist)

            new_order = []
            start_len = len(nodes_to_sort)
            sort_fin = False

            while not sort_fin:
                min_cost = 100000000000000000000000000000
                min_id = 0
                node_ = None
                for i in range(len(nodes_to_sort)):
                    node_ = nodes_to_sort[i]
                    cost_ = costs_to_sort[i]
                    if cost_ < min_cost:
                        min_cost = cost_
                        min_id = i
                if node_ == None:
                    print
                    'yo'
                new_order.append(node_)
                nodes_to_sort.__delitem__(min_id)
                costs_to_sort.__delitem__(min_id)
                if len(new_order) == start_len:
                    sort_fin = True

            return new_order
            # """
            # sort distance wise
            # first -- the ones +-1 to byte
            # then the lower ones
            # """
            # sorted_children_byte = []
            # for i, child in enumerate(children):
            #     # then add the SUBTR at the almost last place and ADD as last place(unless close to byte)
            #     dist_low, dist_high = get_dist_to_bytes(child.pellets)
            #     if dist_high == 0 or dist_low == 0:
            #         sorted_nodes.insert(0, children[i])
            #         children.__delitem__(i)
            #     elif dist_high == 1 or dist_low == 1:
            #         sorted_children_byte.insert(0, children[i])
            #         children.__delitem__(i)
            #
            # pellets_children = [child.pellets for child in children]
            # pellets_children.sort()
            # sorted_children_pellets = []
            # for i, pellets_smallest in enumerate(pellets_children):
            #     for j, child in enumerate(children):
            #         if pellets_smallest == child.pellets:
            #             sorted_children_pellets.insert(i, child)
            #
            # nodes_to_visit_sorted = sorted_nodes + sorted_children_byte
            # nodes_to_visit_sorted = nodes_to_visit_sorted + sorted_children_pellets
            # return nodes_to_visit_sorted

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

    def sort_nodes_to_visit3(self, nodes_to_visit, children):
        """
        put the new kids which had 'divide' action on front

        or just sort by:
        - least steps & least pellets

        sort distance wise
        first -- the ones 0, +-1 to byte, rest of nodes
        then the lower ones
        """
        sorted_c_byte, sorted_c_byte_next, unsorted_c = self.sort_bytewise(children)
        sorted_children_pelletwise = self.sort_pelletwise(unsorted_c)

        nodes_to_visit_sorted = sorted_c_byte + sorted_c_byte_next + nodes_to_visit + sorted_children_pelletwise
        # nodes_to_visit_sorted = sorted_c_byte + sorted_c_byte_next + sorted_children_pelletwise + nodes_to_visit
        return nodes_to_visit_sorted

    def sort_nodes_to_visit4(self, nodes_to_visit, children):
        """
        put the new kids which had 'divide' action on front

        or just sort by:
        - least steps & least pellets

        sort distance wise
        first -- the ones 0, +-1 to byte, rest of nodes
        then the lower ones
        """
        sorted_c_byte, sorted_c_byte_next, unsorted_c = self.sort_bytewise(children)
        sorted_children = self.sort_costwise(unsorted_c)

        nodes_to_visit_sorted = sorted_c_byte + sorted_c_byte_next + nodes_to_visit + sorted_children
        # nodes_to_visit_sorted = sorted_c_byte + sorted_c_byte_next + sorted_children + nodes_to_visit
        # nodes_to_visit_sorted = sorted_c_byte + sorted_c_byte_next + sorted_children_pelletwise + nodes_to_visit
        return nodes_to_visit_sorted


    def get_best_solution(self, nodes_solution):
        if show_hist:
            print('nodes_solution', [str(node) for node in nodes_solution])
        # filter the shortest solution
        min_steps = 1000000000000000000000
        min_id = 10000000000000000000
        for i, node in enumerate(nodes_solution):
            if node.step <= min_steps:
                min_steps = node.step
                min_id = i
        return nodes_solution[i]

    def sort_bytewise(self, children):
        """
        just sort bytewise -- at the beginning add the 0, then +-1 byte
        """
        sorted_byte = []
        sorted_byte_next = []
        normal_nodes = []
        for i, child in enumerate(children):
            # then add the SUBTR at the almost last place and ADD as last place(unless close to byte)
            dist_low, dist_high = get_dist_to_bytes(child.pellets)
            if dist_high == 0 or dist_low == 0:
                sorted_byte.insert(0, children[i])
                # children.__delitem__(i)
            elif dist_high == 1 or dist_low == 1:
                sorted_byte_next.insert(0, children[i])
                # children.__delitem__(i)
            else:
                # just add them to the list
                normal_nodes.append(children[i])
                # children.__delitem__(i)

        # sorted_bytewise = sorted_byte + sorted_byte_next + normal_nodes
        # return sorted_bytewise
        return sorted_byte, sorted_byte_next, normal_nodes

    def sort_pelletwise(self, children):
        """
        just sort the nodes miding only the pellets
        """
        pellets_children = [child.pellets for child in children]
        pellets_children.sort()
        sorted_children_pellets = []
        for i, pellets_smallest in enumerate(pellets_children):
            for j, child in enumerate(children):
                if pellets_smallest == child.pellets:
                    sorted_children_pellets.insert(i, child)
        return sorted_children_pellets

    def get_children_unique_itself(self, children):
        """
        return semi-unique childer -- 2 kids cannot have the same parent and pettles
        """
        semi_unique_children = []
        for i, child_i in enumerate(children):
            unique_cnt = 0
            for j, child_j in enumerate(children):
                if int(child_i.pellets) == int(child_j.pellets):
                    unique_cnt += 1
                    continue
            if unique_cnt == 1:
                semi_unique_children.append(child_i)
        return semi_unique_children

    def get_children_not_in_visited(self, semi_unique_children, nodes_checked):
        """
        check only the pellets state
        """

        # check the pellets state and steps taken
        unique_children = []
        for i, n_child in enumerate(semi_unique_children):
            unique = True
            """
            there might be a situation where 2 nodes have the same pellets but not the same steps
            then delete the longer one
            instead delete just dont add this new child (because it's implied only in BFS that the CHILD has more steps)
            """
            for j, n_checked in enumerate(nodes_checked):
                if int(n_child.pellets) == int(n_checked.pellets):
                    unique = False
                    continue
            if unique:
                unique_children.append(n_child)

        # # check only the pellets state
        # unique_children = []
        # for i, n_child in enumerate(semi_unique_children):
        #     unique = True
        #     """
        #     there might be a situation where 2 nodes have the same pellets but not the same steps
        #     then delete the longer one
        #     instead delete just dont add this new child (because it's implied only in BFS that the CHILD has more steps)
        #     """
        #     for j, n_checked in enumerate(nodes_checked):
        #         if int(n_child.pellets) == int(n_checked.pellets):
        #             unique = False
        #             break
        #     if unique:
        #         unique_children.append(n_child)
        return unique_children


    def sort_costwise(self, nodes):
        """
        sort the nodes miding the cost
        """
        # sorted_nodes2 = sorted(nodes, key=lambda x: x.g_cost_hist)
        sorted_nodes2 = sorted(nodes, key=lambda x: x.h_cost_now)

        # g_costs = [node.g_cost_hist for node in nodes]
        # g_costs.sort()
        # sorted_nodes = []
        # for i, g_cost in enumerate(g_costs):
        #     for j, node in enumerate(nodes):
        #         if g_cost == node.g_cost_hist:
        #             sorted_nodes.insert(i, node)
        return sorted_nodes2


def solution(n):
    # Your code here
    assert len(str(n)) <= 309
    n = int(n)

    solver = FuelInjector(is_bfs=False)
    nodes_solution = solver.solve_fuel_pellets_graph(n, no_solutions=10)
    best_solution = solver.get_best_solution(nodes_solution)
    if show_hist:
        print 'best_solution hist_pellets', best_solution.hist_pellets

    no_actions = best_solution.step
    return no_actions


def solution_shallowest(n):
    assert len(str(n)) <= 309
    n = int(n)

    solver = FuelInjector(is_bfs=True)
    nodes_solution = solver.solve_fuel_pellets_graph(n, no_solutions=1)
    best_solutions = nodes_solution[0].step
    if show_hist:
        print 'hist_pellets', nodes_solution[0].hist_pellets
    return best_solutions


if __name__ == "__main__":
    import time

    # test_inputs = ['4', '15', '77', '135', '199', '217', '314', '2137', '213789', '21378932', '213789327']
    # test_outputs = [2, 5, 9, 9, 10, 11, 11, 15, 24, 32, 37]
    test_inputs = ['213789327']
    test_outputs = [37]
    for ipt, opt in zip(test_inputs, test_outputs):
        # print 'ipt', ipt, 'sol', sol, 'opt', opt
        print 'ipt', ipt

        start_graph = time.time()
        for i in range(2):
            sol = solution(ipt)
        time_graph = time.time() - start_graph
        print('time_graph', time_graph, 'sol', sol)

        start_bfs = time.time()
        for i in range(2):
            sol_bfs = solution_shallowest(ipt)
        time_bfs = time.time() - start_bfs
        print('time_bfs', time_bfs, 'sol_bfs', sol_bfs)
        if sol != opt:
            # raise Warning("Test failed!")
            print 'TEST FAILED'
        else:
            print 'TEST OK'
        print '\n'

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
9 - OK
10 - OK
"""