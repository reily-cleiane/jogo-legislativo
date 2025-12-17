import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, obs, act):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, act)
        )

    def forward(self, x):
        return self.net(x)
