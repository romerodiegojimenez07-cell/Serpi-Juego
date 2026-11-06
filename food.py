import random
from typing import Sequence, Tuple

import pygame

from config import CELL_SIZE, GRID_COLUMNS, GRID_ROWS, RED


class Food:
    """Representa la comida en el tablero."""

    def __init__(self, snake: Sequence[Tuple[int, int]]):
        self.position = self._random_position(snake)

    @staticmethod
    def _random_position(snake: Sequence[Tuple[int, int]]) -> Tuple[int, int]:
        occupied = set(snake)
        while True:
            pos = (
                random.randint(0, GRID_COLUMNS - 1),
                random.randint(0, GRID_ROWS - 1),
            )
            if pos not in occupied:
                return pos

    def respawn(self, snake: Sequence[Tuple[int, int]]) -> None:
        self.position = self._random_position(snake)

    def draw(self, surface: pygame.Surface) -> None:
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)