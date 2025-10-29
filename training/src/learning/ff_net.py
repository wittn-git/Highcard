import torch
import torch.nn as nn
import torch.optim as optim
from typing import Type

class FFNet(nn.Module):

    def __init__(self, input_shape: int, output_shape: int, hidden_sizes: tuple[int, int] = (256,256), activation: Type[nn.Module] = nn.ReLU):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_shape, hidden_sizes[0]),
            activation(),
            nn.Linear(hidden_sizes[0], hidden_sizes[1]),
            activation(),
            nn.Linear(hidden_sizes[1], output_shape)
        )
        self.loss_fn = nn.MSELoss()

    def forward(self, input: torch.Tensor):
        return self.net(input)
    
    def apply(self, input: torch.Tensor):
        with torch.no_grad():
            return self.forward(input).detach().numpy().flatten()

    def train_step(self, input: torch.Tensor, target: torch.Tensor, learning_rate: float):
        optimizer = optim.Adam(self.parameters(), lr=learning_rate) # TODO optimize this for batch learning
        prediction = self.forward(input)
        target = target.detach()
        loss = self.loss_fn(prediction, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
