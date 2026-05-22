import pgzrun

WIDTH = 800
HEIGHT = 800
GRID_SIZE = 50
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

class Grid:

    """Umrechnung zwischen Grid-Koordinaten und Pixel-Positionen"""
    @staticmethod
    def to_pixel(grid_x, grid_y):
        """Grid-Koordinate (z.B. 5, 3) -> Pixel-Position (250, 150)"""
        return grid_x * GRID_SIZE, grid_y * GRID_SIZE
    
    @staticmethod
    def to_grid(pixel_x, pixel_y):
        """Pixel-Position (z.B. 250, 150) -> Grid-Koordinate (5, 3)"""
        return pixel_x // GRID_SIZE, pixel_y // GRID_SIZE

class Snake:
    def __init__(self, x, y):
        self.head = (x, y)

    def draw(self):
        px, py = Grid.to_pixel(*self.head)
        screen.blit('unbenannt', (px, py))

snake = Snake(COLS // 2, ROWS // 2)

def draw():
    screen.fill((0, 0, 0))
    # Gitternetz zeichnen
    for x in range(COLS + 1):
        px = x * GRID_SIZE
        screen.draw.line((px, 0), (px, HEIGHT), (40, 40, 40))
    
    for y in range(ROWS + 1):
        py = y * GRID_SIZE
        screen.draw.line((0, py), (WIDTH, py), (40, 40, 40))

    # Schlangenkopf zeichnen
    snake.draw()

def update():
    pass
pgzrun.go()