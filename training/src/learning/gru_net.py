import torch
import torch.nn as nn
import torch.optim as optim

class GRUNet(nn.Module):

    def __init__(self, input_shape : int, output_shape : int, hidden_size : int, layer_n : int):
        super(GRUNet, self).__init__()
        self.layer_n = layer_n
        self.hidden_size = hidden_size
        self.gru = nn.GRU(
            input_size=input_shape,
            hidden_size=hidden_size,
            num_layers=layer_n,
            batch_first=True,
        )
        self.fc = nn.Linear(hidden_size, output_shape)
        self.loss_fn = nn.MSELoss()
    
    def apply(self, input: torch.Tensor, hidden : torch.Tensor = None):
        with torch.no_grad():
            out, hidden = self.forward(input, hidden)
            return out.detach().numpy().flatten(), hidden

    def forward(self, x_step : torch.Tensor, hidden : torch.Tensor = None):
        """
        Perform a forward pass for one step.
        - x_step: shape (input_size,) or (batch, input_size)
        If hidden is None, initializes it as zeros.
        Returns:
            out: (batch, output_size)
            hidden: new hidden state
        """

        if hidden is None:
            hidden = torch.zeros(self.layer_n, 1, self.hidden_size, device=x_step.device)

        x_step = x_step.unsqueeze(1)
        out, hidden = self.gru(x_step, hidden)
        out = self.fc(out[:, -1, :])

        return out, hidden

    def train_step(self, sequence : torch.Tensor, target : torch.Tensor, learning_rate : float = 1e-3):
        optimizer = optim.Adam(self.parameters(), lr=learning_rate) # TODO optimize this for batch learning
        prediction, _ = self.forward(sequence)
        target = target.detach()
        loss = self.loss_fn(prediction, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()