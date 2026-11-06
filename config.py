"""Constantes de configuración del juego Snake."""

# Ventana
WINDOW_TITLE = "Serpi"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_COLUMNS = SCREEN_WIDTH // CELL_SIZE
GRID_ROWS = SCREEN_HEIGHT // CELL_SIZE
FPS = 10

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (25, 25, 25)
LIGHT_GRAY = (75, 75, 75)
GREEN = (72, 209, 102)
DARK_GREEN = (32, 151, 72)
RED = (220, 53, 69)
ORANGE = (255, 153, 51)
BLUE = (66, 135, 245)
# Niveles y guardado
POINTS_PER_LEVEL = 5
SAVE_FILE = "records.json"
# Direcciones
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

# Estado inicial
START_POS = (GRID_COLUMNS // 2, GRID_ROWS // 2)
INITIAL_SCORE = 0