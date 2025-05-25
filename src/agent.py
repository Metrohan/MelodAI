
import random

class FeedbackAgent:
    def __init__(self):
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1

    def get_state(self, melody):
        return tuple(n.pitch.midi for n in melody)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(["same", "variation"])
        return "same" if self.q_table.get(state, [0, 0])[0] >= self.q_table.get(state, [0, 0])[1] else "variation"

    def update_q_table(self, state, action, reward):
        actions = ["same", "variation"]
        if state not in self.q_table:
            self.q_table[state] = [0, 0]
        a_idx = actions.index(action)
        self.q_table[state][a_idx] = (1 - self.alpha) * self.q_table[state][a_idx] + self.alpha * reward
