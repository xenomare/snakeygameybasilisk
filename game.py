import pgzrun

WIDTH = 800
HEIGHT = 800
GRID_SIZE = 50
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE
SPEED = 0.1

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
        self.direction = (SPEED, 0) 
        self.move_counter = 8
        self.move_delay = 1

    def draw(self):
        px, py = Grid.to_pixel(*self.head)
        screen.blit('unbenannt', (px, py))

    def update(self):
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.move_counter = 0
            self.move()

    def move(self):
        x, y = self.head
        dx, dy = self.direction
        x = (x + dx) % COLS
        y = (y + dy) % ROWS
        self.head = (x, y)

snake = Snake(COLS // 2, ROWS // 2)

def on_key_down(key):
    if key == keys.UP:
        snake.direction = (0, -SPEED)
    elif key == keys.DOWN:
        snake.direction = (0, SPEED)
    elif key == keys.LEFT:
        snake.direction = (-SPEED, 0)
    elif key == keys.RIGHT:
        snake.direction = (SPEED, 0)

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
    snake.update()

pgzrun.go()