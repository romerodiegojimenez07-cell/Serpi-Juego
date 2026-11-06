"""Punto de entrada del juego Snake con menú, guardado y niveles."""

import sys
from typing import Tuple

import pygame

from config import (
    BLACK,
    BLUE,
    CELL_SIZE,
    DOWN,
    FPS,
    GRID_COLUMNS,
    GRID_ROWS,
    LEFT,
    LIGHT_GRAY,
    ORANGE,
    POINTS_PER_LEVEL,
    RIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UP,
    WHITE,
    WINDOW_TITLE,
)
from food import Food
from save import (
    clear_saved_game,
    has_saved_game,
    load_game,
    load_record,
    save_game,
    save_record,
)
from snake import Snake

# Estados
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}


def is_out_of_bounds(position: Tuple[int, int]) -> bool:
    x, y = position
    return x < 0 or x >= GRID_COLUMNS or y < 0 or y >= GRID_ROWS


def draw_grid(surface: pygame.Surface) -> None:
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, LIGHT_GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, LIGHT_GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_hud(surface, score, level, record, font):
    hud = font.render(
        f"Puntaje: {score}   Nivel: {level}   Récord: {record}", True, WHITE
    )
    surface.blit(hud, (10, 10))


class Button:
    def __init__(self, rect: pygame.Rect, text: str, enabled: bool = True):
        self.rect = rect
        self.text = text
        self.enabled = enabled

    def draw(self, surface, font, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos) and self.enabled
        color = BLUE if hovered else (LIGHT_GRAY if self.enabled else (40, 40, 40))
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        text_color = WHITE if self.enabled else (120, 120, 120)
        label = font.render(self.text, True, text_color)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event, mouse_pos) -> bool:
        return (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(mouse_pos)
        )


def build_menu_buttons():
    cx = SCREEN_WIDTH // 2
    width, height = 240, 50
    return {
        "new": Button(pygame.Rect(cx - width // 2, 200, width, height), "Nuevo juego"),
        "load": Button(
            pygame.Rect(cx - width // 2, 270, width, height),
            "Cargar partida",
            enabled=has_saved_game(),
        ),
        "exit": Button(pygame.Rect(cx - width // 2, 340, width, height), "Salir"),
    }


def reset_game():
    snake = Snake()
    food = Food(snake.body)
    return snake, food, 0, 1, False


def load_saved_game():
    data = load_game()
    if not data:
        return None
    snake = Snake.from_dict({"body": data["snake"], "direction": data["direction"]})
    food = Food(snake.body)
    return snake, food, int(data["score"]), int(data["level"]), False


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)
    title_font = pygame.font.SysFont("arial", 48, bold=True)

    state = MENU
    buttons = build_menu_buttons()
    record = load_record()

    snake, food, score, level, game_over = reset_game()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # ---- MENÚ ----
            if state == MENU:
                if buttons["new"].clicked(event, mouse_pos):
                    clear_saved_game()
                    snake, food, score, level, game_over = reset_game()
                    state = PLAYING

                elif buttons["load"].clicked(event, mouse_pos):
                    loaded = load_saved_game()
                    if loaded:
                        snake, food, score, level, game_over = loaded
                        state = PLAYING

                elif buttons["exit"].clicked(event, mouse_pos):
                    pygame.quit()
                    sys.exit()

            # ---- JUGANDO ----
            elif state == PLAYING:
                if event.type == pygame.KEYDOWN and event.key in KEY_DIRECTIONS:
                    snake.change_direction(KEY_DIRECTIONS[event.key])

            # ---- GAME OVER ----
            elif state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        clear_saved_game()
                        snake, food, score, level, game_over = reset_game()
                        state = PLAYING
                    elif event.key == pygame.K_m:
                        buttons = build_menu_buttons()
                        state = MENU

        # ---- LÓGICA DEL JUEGO ----
        if state == PLAYING:
            next_pos = snake.next_head()
            will_eat = next_pos == food.position

            if is_out_of_bounds(next_pos):
                game_over = True
            else:
                snake.move(grow=will_eat)
                if snake.collides_with_self():
                    game_over = True
                elif will_eat:
                    score += 1

                    # Subida de nivel con guardado automático
                    new_level = score // POINTS_PER_LEVEL + 1
                    if new_level > level:
                        level = new_level
                        save_game(snake.body, snake.direction, score, level)

                    food.respawn(snake.body)

            if game_over:
                save_record(score)
                record = load_record()
                #clear_saved_game()
                state = GAME_OVER

        # ---- DIBUJO ----
        screen.fill(BLACK)

        if state == MENU:
            title = title_font.render("Serpi", True, ORANGE)
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 110)))
            subtitle = font.render(f"Récord: {record}", True, WHITE)
            screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 160)))
            for button in buttons.values():
                button.draw(screen, font, mouse_pos)

        elif state == PLAYING:
            draw_grid(screen)
            food.draw(screen)
            snake.draw(screen)
            draw_hud(screen, score, level, record, font)

        elif state == GAME_OVER:
            draw_grid(screen)
            food.draw(screen)
            snake.draw(screen)
            draw_hud(screen, score, level, record, font)
            msg = font.render("Game Over", True, ORANGE)
            screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            hint = font.render("R = reiniciar   M = menú", True, WHITE)
            screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run()