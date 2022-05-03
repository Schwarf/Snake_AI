import torch


class Trainer:
    def __init__(self, model, learning_rate, gamma):
        self._learning_rate = learning_rate
        self._gamma = gamma
        self._model = model
        self._optimizer = torch.optim.Adam(model.parameters(), lr=self._learning_rate)
        self.criterion = torch.nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over_state):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
