import torch
import torch.nn as nn
import torch.optim as optim

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
        self.loss_fn = nn.MSELoss()

    def forward(self, input: torch.Tensor):
        return self.net(input)

    def train_step(self, input: torch.Tensor, target: torch.Tensor, learning_rate: float):
        optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        prediction = self.forward(input).squeeze()
        loss = self.loss_fn(prediction, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
