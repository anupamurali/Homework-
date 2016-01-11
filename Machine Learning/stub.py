import numpy.random as npr
import sys
from learners import *
from statespaces import *
import numpy as np
import matplotlib.pyplot as plt

from SwingyMonkey import SwingyMonkey

class Learner:

    def __init__(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.learning_module = BasicQLearner()
        self.state_module = RawDataStateSpace()

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.learning_module.reset()

    def action_callback(self, state):
        '''Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.'''

        # You might do some learning here based on the current state and the last state.

        # You'll need to take an action, too, and return it.
        # Return 0 to swing and 1 to jump.

        # Transform the state
        state = self.state_module.transform(state)

        # Get action from learning module
        action = self.learning_module.action_callback(state, self.last_state, self.last_action, self.last_reward)
        self.last_state = state
        self.last_action = action

        """
        # OLD STUFF
        new_action = npr.rand() < 0.1
        new_state  = state

        self.last_action = new_action
        self.last_state  = new_state
        """
        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''
        self.last_reward = reward

iters = 100
avg_window_sz = 10
learner = Learner()
avgs =[0 for _ in xrange(avg_window_sz)]
all_scores = []

# TODO: MOVING AVERAGE

best_overall = (0,0)
for ii in xrange(iters):

    # Make a new monkey object.
    swing = SwingyMonkey(sound=False,            # Don't play sounds.
                         text="Epoch %d" % (ii), # Display the epoch on screen.
                         tick_length=1,          # Make game ticks super fast.
                         action_callback=learner.action_callback,
                         reward_callback=learner.reward_callback)

    # Loop until you hit something.
    best_score = 0
    while swing.game_loop():
        score = swing.score
        best_score = max(best_score, score)
        pass

    print "EPOCH %d BEST SCORE %d" % (ii, best_score)
    if best_score > best_overall[1]:
        best_overall = (ii, best_score)


    # # Shift list by 1 if too many points
    # if ii >= avg_window_sz:
    #     avgs = avgs[1:9] + [0]
    # # Add to moving average
    # avgs[min(ii,avg_window_sz - 1)] = best_score

    # Add to best scores
    all_scores.append(best_score)


    # Reset the state of the learner.
    learner.reset()

# Plot best score for each epoch
x = np.arange(0, 100)
y = np.array(all_scores)
plt.plot(x, y)
plt.show()
print "BEST OVERALL SCORE EPOCH %d: %d" % best_overall



    
