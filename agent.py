import random
from collections import deque, namedtuple

import numpy
import torch

from model import Linear_QNet
from snake_game_ai import SnakeGameAI, BLOCK_SIZE_PIXELS, Point, Direction
from trainer import Trainer
from plot_helper import plot

MAX_ITEMS_IN_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class Agent:
    def __init__(self):
        self.number_of_games = 0
        self._epsilon_for_randomness = 0
        self._discount_rate = 0.9
        self._deque = deque(maxlen=MAX_ITEMS_IN_MEMORY)
        self.model = Linear_QNet(input_size=11, hidden_size=256, output_size=3)
        self.trainer = Trainer(self.model, learning_rate=LEARNING_RATE, gamma=self._discount_rate)

    def _compute_state(self, snake_game, points_near_snake_head, snake_heading_direction):
        danger_straight = \
            (snake_heading_direction.right and snake_game.is_there_a_collision(points_near_snake_head.right)) or \
            (snake_heading_direction.left and snake_game.is_there_a_collision(points_near_snake_head.left)) or \
            (snake_heading_direction.up and snake_game.is_there_a_collision(points_near_snake_head.above)) or \
            (snake_heading_direction.down and snake_game.is_there_a_collision(points_near_snake_head.below))
        danger_left = \
            (snake_heading_direction.right and snake_game.is_there_a_collision(points_near_snake_head.above)) or \
            (snake_heading_direction.left and snake_game.is_there_a_collision(points_near_snake_head.below)) or \
            (snake_heading_direction.up and snake_game.is_there_a_collision(points_near_snake_head.left)) or \
            (snake_heading_direction.down and snake_game.is_there_a_collision(points_near_snake_head.right))

        danger_right = \
            (snake_heading_direction.right and snake_game.is_there_a_collision(points_near_snake_head.below)) or \
            (snake_heading_direction.left and snake_game.is_there_a_collision(points_near_snake_head.above)) or \
            (snake_heading_direction.up and snake_game.is_there_a_collision(points_near_snake_head.right)) or \
            (snake_heading_direction.down and snake_game.is_there_a_collision(points_near_snake_head.left))

        food_left = snake_game.food.x < snake_game.snake_head.x
        food_right = snake_game.food.x > snake_game.snake_head.x
        food_up = snake_game.food.y > snake_game.snake_head.y
        food_down = snake_game.food.y < snake_game.snake_head.y

        state = numpy.array([danger_straight, danger_right, danger_left,
                             snake_heading_direction.left, snake_heading_direction.right,
                             snake_heading_direction.up, snake_heading_direction.down,
                             food_left, food_right, food_up, food_down], dtype=int)
        return state

    def get_state(self, snake_game):
        snake_head = snake_game.snake_head
        points_near_snake_head = namedtuple("PointsNearSnakeHead", "left right below above")
        points_near_snake_head.left = Point(snake_head.x - BLOCK_SIZE_PIXELS, snake_head.y)
        points_near_snake_head.right = Point(snake_head.x + BLOCK_SIZE_PIXELS, snake_head.y)
        points_near_snake_head.below = Point(snake_head.x, snake_head.y - BLOCK_SIZE_PIXELS)
        points_near_snake_head.above = Point(snake_head.x, snake_head.y + BLOCK_SIZE_PIXELS)

        snake_heading_direction = namedtuple("SnakeHeadingDirection", "left right up down")

        snake_heading_direction.left = snake_game.snake_direction == Direction.LEFT
        snake_heading_direction.right = snake_game.snake_direction == Direction.RIGHT
        snake_heading_direction.up = snake_game.snake_direction == Direction.UP
        snake_heading_direction.down = snake_game.snake_direction == Direction.DOWN
        return self._compute_state(snake_game, points_near_snake_head, snake_heading_direction)

    def remember(self, state, action, reward, next_state, game_over_state):
        self._deque.append((state, action, reward, next_state, game_over_state))

    def train_on_long_memory(self):
        if len(self._deque) > BATCH_SIZE:
            mini_sample = random.sample(self._deque, BATCH_SIZE)
        else:
            mini_sample = self._deque

        states, actions, rewards, next_states, game_over_states = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_over_states)

    def train_on_short_memory(self, state, action, reward, next_state, game_over_state):
        self.trainer.train_step(state, action, reward, next_state, game_over_state)

    def get_action(self, state):
        start_epsilon = 80  # should be a hyper-parameter
        self.epsilon = start_epsilon - self.number_of_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move_index = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_index = torch.argmax(prediction).item()

        final_move[move_index] = 1
        return final_move


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
                agent.model.save()
            print("Game: ", agent.number_of_games, " Score: ", score, " Record: ", record_score)
            plot_scores.append(score)
            total_score += score
            mean_score = total_score /agent.number_of_games
            plot_average_scores.append(mean_score)
            plot(plot_scores, plot_average_scores)


if __name__ == '__main__':
    train()
