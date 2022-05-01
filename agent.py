from collections import deque

from snake_game_ai import SnakeGameAI, BLOCK_SIZE_PIXELS, Point, Direction

MAX_ITEMS_IN_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class Agent:
    def __init__(self):
        self.number_of_games = 0
        self._epsilon_for_randomness = 0
        self._discount_rate = 0
        self._memory = deque(maxlen=MAX_ITEMS_IN_MEMORY)

    def determine_danger_values(self):


    def get_state(self, snake_game):
        snake_head = snake_game.snake_head
        point_left_of_head = Point(snake_head.x - BLOCK_SIZE_PIXELS, snake_head.y)
        point_right_of_head = Point(snake_head.x + BLOCK_SIZE_PIXELS, snake_head.y)
        point_below_of_head = Point(snake_head.x, snake_head.y - BLOCK_SIZE_PIXELS)
        point_above_of_head = Point(snake_head.x, snake_head.y + BLOCK_SIZE_PIXELS)

        is_snake_heading_left = snake_game.snake_direction == Direction.LEFT
        is_snake_heading_right = snake_game.snake_direction == Direction.RIGHT
        is_snake_heading_up = snake_game.snake_direction == Direction.UP
        is_snake_heading_down = snake_game.snake_direction == Direction.DOWN



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
            agent.train_on_long_memory()
            if score > record_score:
                record_score = score
                # agent mode.save()
                print("Game: ", agent.number_of_games, " Score: ", score, " Record: ", record_score)


if __name__ == '__main__':
    train()
