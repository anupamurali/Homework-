from collections import Counter
import random
import math

"""
The sequence is:
ACTION -> REWARD -> ACTION -> REWARD

This means that action_callback always gets called before reward_callback
"""
class BasicQLearner(object):
    def __init__(self):
        self.Q = Counter()
        self.N = Counter() # # of visits to state S taking action A
        self.gamma = 0.70
        self.alpha = 0.9
        self.num_iters = 0
        self.num_trials = 1

    def reset(self):
        self.num_trials += 1

    def update_Q(self, last_state, last_action, curr_state, last_reward):
        # Update based on the last action we took/reward we got
        Q = self.Q
        s = last_state
        a = last_action
        sp = curr_state
        if last_reward is not None:
            Q[(s,a)] = Q[(s,a)] + self.alpha * ( (last_reward + self.gamma * max(Q[(sp,0)], Q[(sp,1)])) - Q[(s,a)])

    def should_exploit(self, curr_state):
        # Returns TRUE if the learner should exploit
        return True

    def get_action(self, curr_state):
        # Returns the action that should be done. Always returns the optimal action.
        Q = self.Q
        if Q[(curr_state, 0)] > Q[(curr_state, 1)]:
            action = 0
        elif Q[(curr_state, 0)] < Q[(curr_state, 1)]:
            action = 1
        else:
            action = random.randint(0,1)
        return action

    def action_callback(self, curr_state, last_state, last_action, last_reward):
        """
        Returns action to perform (0 or 1)
        """
        Q = self.Q
        self.num_iters += 1

        # Update Q values
        self.update_Q(last_state, last_action, curr_state, last_reward)

        # Decide which action to perform
        action = self.get_action(curr_state)

        # Increase count
        self.N[(curr_state,action)] += 1
        return action

class EGreedyQLearner(BasicQLearner):
    def __init__(self):
        super(EGreedyQLearner, self).__init__()

    def get_action(self, curr_state):
        epsilon = 1.0 / self.num_trials
        if random.random() > epsilon:
            # Do action with greatest Q value if exploiting
            return super(EGreedyQLearner, self).get_action(curr_state)
        else:
            # Otherwise do random action
            return random.randint(0,1)

    def update_Q(self, last_state, last_action, curr_state, last_reward):
        self.alpha = 1.0 / (1.0 + self.N[(last_state, last_action)])
        super(EGreedyQLearner, self).update_Q(last_state, last_action, curr_state, last_reward)
        print self.Q[("SPECIAL!", 0)], self.Q[("SPECIAL!", 1)]

class BoltzmannQLearner(BasicQLearner):
    def __init__(self):
        super(BoltzmannQLearner, self).__init__()

    def get_action(self, curr_state):
        Q = self.Q
        tao = 0.10 + math.exp(-self.num_trials)
        prob_do_0 = math.exp(Q[(curr_state, 0)]/tao) / sum([math.exp(Q[(curr_state, i)]/tao) for i in xrange(2)])
        return int((random.random() >= prob_do_0))

    def update_Q(self, last_state, last_action, curr_state, last_reward):
        self.alpha = 1.0 / (1.0 + self.N[(last_state, last_action)])
        super(BoltzmannQLearner, self).update_Q(last_state, last_action, curr_state, last_reward)


class ModelBasedLearner(object):
    def __init__(self):
        self.R = Counter()
        self.N = Counter()

