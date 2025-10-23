from training.util.classes import State

import random

class ReplayBuffer:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = []

    def push(self, state : State, action : int, reward : float, next_state : State, done : bool):
        while len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        if batch_size > len(self.buffer):
            return random.sample(self.buffer, len(self.buffer))
        return random.sample(self.buffer, batch_size)