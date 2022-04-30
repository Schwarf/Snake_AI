from collections import deque

from snake_game_ai import SnakeGameAI

MAX_ITEMS_IN_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class Agent:
    def __init__(self):
        self.number_of_games = 0
        self._epsilon_for_randomness = 0
        self._discount_rate = 0
        self._memory = deque(maxlen=MAX_ITEMS_IN_MEMORY)

    def get_state(self, snake_game):
        pass

    def remember(self, state, action, reward, next_state, game_over_state):
        pass

    def train_on_long_memory(self):
        pass

    def train_on_short_memory(self, state, action, reward, next_state, game_over_state):
        pass

    def get_action(self, state):
        pass


def train():
    plot_scores = []
    plot_average_scores = []
    total_score = 0
    record_score = 0
    agent = Agent()
    snake_game = SnakeGameAI()
    while True:
        # get current state
        current_state = agent.get_state(snake_game)
        # get move
        final_move = agent.get_action(current_state)
        reward, game_over, score = snake_game.play_step(final_move)
        new_state = agent.get_state(snake_game)
        # train short memory
        agent.train_on_short_memory(current_state, final_move, reward, new_state, game_over)
        agent.remember(current_state, final_move, reward, new_state, game_over)
        if game_over:
            # train the long term memory, experience replay and plot the result
            snake_game.reset()
            agent.number_of_games += 1


if __name__ == '__main__':
    train()
