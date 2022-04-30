import random
from collections import namedtuple
from enum import Enum

import pygame

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# font = pygame.font.SysFont('arial', 25)

class Action(Enum):
    Straight = 0
    RightTurn = 1
    LeftTurn = 2


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
        self._direction = Direction.RIGHT

        self._snake_head = Point(self._width / 2, self._height / 2)
        self._snake = [self._snake_head,
                       Point(self._snake_head.x - BLOCK_SIZE_PIXELS, self._snake_head.y),
                       Point(self._snake_head.x - (2 * BLOCK_SIZE_PIXELS), self._snake_head.y)]

        self._score = 0
        self._food = None
        self._place_food()
        self._frame_iteration = 0
        self._reward = 0

    def _place_food(self):
        x = random.randint(0, (self._width - BLOCK_SIZE_PIXELS) // BLOCK_SIZE_PIXELS) * BLOCK_SIZE_PIXELS
        y = random.randint(0, (self._height - BLOCK_SIZE_PIXELS) // BLOCK_SIZE_PIXELS) * BLOCK_SIZE_PIXELS
        self._food = Point(x, y)
        if self._food in self._snake:
            self._place_food()

    def _is_game_over(self) -> bool:
        return self._is_collision() or self._frame_iteration > 100 * len(self._snake)

    def _move_snake_tail(self):
        self._snake.pop()  # Remove last element (since we added one in move_snake_head)

    def play_step(self, action):
        self._frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move_snake_head(action)  # update the head
        self._snake.insert(0, self._snake_head)

        # 3. check if game over
        game_over = False
        if self._is_game_over():
            self._reward = -10
            game_over = True
            return self._reward, game_over, self._score

        # 4. place new food or just move
        if self._snake_head == self._food:
            self._score += 1
            self._reward = 10
            self._place_food()
        else:
            self._move_snake_tail()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return self._reward, game_over, self._score

    def _is_there_a_collision(self, point=None):
        # hits boundary
        if point is None:
            point = self._snake_head
        return self._collision_with_boundary(point) or self._collision_with_it_self()

    def _collision_with_boundary(self, point):
        right_boundary = self._width - BLOCK_SIZE_PIXELS
        lower_boundary = self._height - BLOCK_SIZE_PIXELS
        left_boundary = 0
        upper_boundary = 0
        if point.x > right_boundary or point.x < left_boundary or point.y > lower_boundary or point.y < upper_boundary:
            return True
        return False

    def _collision_with_it_self(self):
        if self._snake_head in self._snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self._snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE_PIXELS, BLOCK_SIZE_PIXELS))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED,
                         pygame.Rect(self._food.x, self._food.y, BLOCK_SIZE_PIXELS, BLOCK_SIZE_PIXELS))

        text = font.render("Score: " + str(self._score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move_snake_head(self, action: Action):
        # [straight, right, left] are possible actions
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self._direction)  # get index of current direction
        new_direction = None
        if action == Action.Straight:
            new_direction = clock_wise[index]  # stay in direction
        elif action == Action.RightTurn:
            new_direction = clock_wise[(index + 1) % 4]  # right -> dwon, d -> l, l->u, u -> r
        elif action == Action.LeftTurn:
            new_direction = clock_wise[(index - 1) % 4]

        self._direction = new_direction

        x = self._snake_head.x
        y = self._snake_head.y
        if self._direction == Direction.RIGHT:
            x += BLOCK_SIZE_PIXELS
        elif self._direction == Direction.LEFT:
            x -= BLOCK_SIZE_PIXELS
        elif self._direction == Direction.DOWN:
            y += BLOCK_SIZE_PIXELS
        elif self._direction == Direction.UP:
            y -= BLOCK_SIZE_PIXELS

        self._snake_head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGameAI()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
