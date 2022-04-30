import random
from collections import namedtuple
from enum import Enum

import numpy
import pygame

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE_PIXELS = 20
SPEED = 10


class SnakeGameAI:

    def __init__(self, width=640, height=480):
        self._width = width
        self._height = height
        # init display
        self.display = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self._width / 2, self._height / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE_PIXELS, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE_PIXELS), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self._frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self._width - BLOCK_SIZE_PIXELS) // BLOCK_SIZE_PIXELS) * BLOCK_SIZE_PIXELS
        y = random.randint(0, (self._height - BLOCK_SIZE_PIXELS) // BLOCK_SIZE_PIXELS) * BLOCK_SIZE_PIXELS
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self._frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self._is_collision() or self._frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def _is_collision(self, point=None):
        # hits boundary
        if point is None:
            point = self.head
        if point.x > self._width - BLOCK_SIZE_PIXELS or point.x < 0 or point.y > self._height - BLOCK_SIZE_PIXELS or point.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE_PIXELS, BLOCK_SIZE_PIXELS))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE_PIXELS, BLOCK_SIZE_PIXELS))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left] ar possible action
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)
        if numpy.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[index]
        elif numpy.array_equal(action, [0, 1, 0]):
            new_direction = clock_wise[(index + 1) % 4]
        elif numpy.array_equal(action, [0, 0, 1]):
            new_direction = clock_wise[(index - 1) % 4]

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE_PIXELS
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE_PIXELS
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE_PIXELS
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE_PIXELS

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGameAI()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
