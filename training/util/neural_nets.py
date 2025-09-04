from torch import nn
import torch
import numpy as np

class NeuralNetwork(nn.Module):

    def __init__(self, input_shape, output_shape, hidden_sizes=(256,256), activation=nn.ReLU):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_shape, hidden_sizes[0]),
            activation(),
            nn.Linear(hidden_sizes[0], hidden_sizes[1]),
            activation(),
            nn.Linear(hidden_sizes[1], output_shape)
        )

    def forward(self, input: torch.Tensor):
        return self.net(input)
