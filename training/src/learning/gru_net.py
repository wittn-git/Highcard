import torch
import torch.nn as nn
import torch.optim as optim

class GRUNet(nn.Module):

    def __init__(self, input_shape : int, output_shape : int, hidden_size : int, hidden_layers_n : int):
        super(GRUNet, self).__init__()
        self.gru = nn.GRU(
            input_size=input_shape,
            hidden_size=output_shape,
            num_layers=hidden_layers_n,
            batch_first=True,
        )
        self.fc = nn.Linear(hidden_size, output_shape)
    
    def apply(self, input: torch.Tensor, hidden : torch.Tensor = None):
        with torch.no_grad():
            return self.forward(input, hidden).detach().numpy().flatten()

    def forward(self, x_step : torch.Tensor, hidden : torch.Tensor = None):
        """
        Perform a forward pass for one step.
        - x_step: shape (input_size,) or (batch, input_size)
        If hidden is None, initializes it as zeros.
        Returns:
            out: (batch, output_size)
            hidden: new hidden state
        """

        if x_step.dim() == 1:
            x_step = x_step.unsqueeze(0)

        batch_size = x_step.size(0)

        if hidden is None:
            hidden = torch.zeros(self.hidden_layers_n, batch_size, self.hidden_size, device=x_step.device)

        x_step = x_step.unsqueeze(1)
        out, hidden = self.gru(x_step, hidden)
        out = self.fc(out[:, -1, :])

        return out, hidden


    def train_step(self, sequence : torch.Tensor, targets : torch.Tensor, learning_rate : float = 1e-3):
        """
        - sequence: (batch, seq_len, input_size)
        - targets:  (batch, seq_len, output_size) or (batch, output_size)
        """
        self.train()
        optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        criterion = nn.MSELoss()

        optimizer.zero_grad()
        out, _ = self.gru(sequence)
        out = self.fc(out)

        if targets.dim() == 2:
            targets = targets.unsqueeze(1).expand_as(out)

        loss = criterion(out, targets)
        loss.backward()
        optimizer.step()

        return loss.item()
