import random
import numpy as np
import torch

def seed_rnd(seed_value: int):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)