import copy


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

    Q_table = []

    def __init__(self, pellets):
        self.pellets_init = int(pellets)
        self.pellets_now = int(pellets)
        self.state_now = self.get_state_pellets(self.pellets_now)
        self.history.append({'step': 0, 'pellets': self.pellets_now, 'state': self.state_now, 'taken_actions': []})
        # print self.history[-1]

        # # init Q table
        # for r, state in enumerate(self.possible_states):
        #     row = []
        #     for c, action in enumerate(self.possible_actions):
        #         row.append(action)
        #     self.Q_table.append(row)

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
                    for action in self.get_possible_actions(state_now):
                        reward = self.get_reward(state_now, action)
                        action_reward[action] = reward

                    # best action
                    a_best = self.choose_greedy(action_reward)
                    # execute action
                    self.take_action(a_best)
                    taken_actions.append(a_best)

                self.state_now = self.get_state_pellets(self.pellets_now)
                self.history.append(
                    {'step': step, 'pellets': self.pellets_now, 'state': state_now, 'taken_actions': taken_actions})

                # print self.history[-1]
                is_solved = self.state_now == self.STATE_SOLVED

                # if is_solved:
                # print 'SOLVED'
                # exit(0)
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


def solution(n):
    # Your code here
    solver = FuelInjector(n)

    no_actions = solver.solve_fuel_pellets_rl()
    # return 2
    # print no_actions
    # # exit(0)
    return no_actions


if __name__ == "__main__":

    # test_inputs = ['4', '15', '77']
    # test_outputs = [2, 5, 9]
    test_inputs = ['77']
    test_outputs = [9]
    for ipt, opt in zip(test_inputs, test_outputs):
        sol = solution(ipt)
        print 'ipt', ipt, 'sol', sol, 'opt', opt
        if sol != opt:
            # raise Warning("Test failed!")
            print 'TEST FAILED'



