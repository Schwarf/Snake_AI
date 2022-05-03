import torch


class Trainer:
    def __init__(self, model, learning_rate, gamma):
        self._learning_rate = learning_rate
        self._gamma = gamma
        self._model = model
        self._optimizer = torch.optim.Adam(model.parameters(), lr=self._learning_rate)
        self._criterion = torch.nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over_state):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over_state = (game_over_state, )

        # predicted Q values with the current state
        prediction = self._model(state)

        target = prediction.clone()
        for index in range(len(game_over_state)):
            Q_new  = reward[index]
            if not game_over_state[index]:
                    Q_new = reward[index] + self._gamma * torch.max(self._model(next_state[index]))
            target[index][torch.argmax(action).item()] = Q_new
        # Q_new = reward + gamma * max(next_predicted Q value) -> only do this if not game_over_state
        # pred.clone()
        # predictions[argmax(action)] = Q_new
        self._optimizer.zero_grad()
        loss = self._criterion(target, prediction)
        loss.backward()
        self._optimizer.step()


