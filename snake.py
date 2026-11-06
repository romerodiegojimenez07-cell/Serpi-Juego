from typing import List, Sequence, Tuple

import pygame

from config import (
    CELL_SIZE,
    DARK_GREEN,
    GREEN,
    OPPOSITE_DIRECTIONS,
    RIGHT,
    START_POS,
)


class Snake:
    """Serpiente: cuerpo, dirección y movimiento."""

    def __init__(
        self,
        body: Sequence[Tuple[int, int]] = None,
        direction: Tuple[int, int] = RIGHT,
    ):
        if body is None:
            body = self._initial_body(START_POS, length=3)
        self.body: List[Tuple[int, int]] = list(body)
        self.direction = direction
        self._pending_direction = direction

    @staticmethod
    def _initial_body(
        center: Tuple[int, int], length: int = 3
    ) -> List[Tuple[int, int]]:
        cx, cy = center
        return [(cx - i, cy) for i in range(length)]

    @property
    def head(self) -> Tuple[int, int]:
        return self.body[0]
    def to_dict(self) -> dict:
        return {
            "body": [list(seg) for seg in self.body],
            "direction": list(self.direction),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Snake":
        body = [tuple(seg) for seg in data["body"]]
        direction = tuple(data["direction"])
        snake = cls(body=body, direction=direction)
        return snake
    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        if new_direction == OPPOSITE_DIRECTIONS.get(self.direction):
            return
        self._pending_direction = new_direction

    def next_head(self) -> Tuple[int, int]:
        dx, dy = self._pending_direction
        return (self.head[0] + dx, self.head[1] + dy)

    def move(self, grow: bool = False) -> None:
        self.direction = self._pending_direction
        dx, dy = self.direction
        new_head = (self.head[0] + dx, self.head[1] + dy)
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def collides_with_self(self) -> bool:
        return self.head in self.body[1:]

    def collides_with(self, position: Tuple[int, int]) -> bool:
        return self.head == position

    def draw(self, surface: pygame.Surface) -> None:
        for index, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if index == 0 else DARK_GREEN
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)