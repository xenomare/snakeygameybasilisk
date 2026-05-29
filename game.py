import pgzrun
import random
import os

WIDTH = 800
HEIGHT = 800
GRID_SIZE = 40
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

# Zellen pro Frame (z.B. 0.2 -> 5 Frames pro Zelle)
SPEED = 0.2

HIGHSCORE_FILE = 'highscore.txt'

# Hilfsfunktionen für Koordinatenumrechnung
def grid_to_pixel(gx, gy):
    return gx * GRID_SIZE, gy * GRID_SIZE


def pixel_to_grid(px, py):
    return int(px) // GRID_SIZE, int(py) // GRID_SIZE
#

class Game:
    def __init__(self):
        self.state = 'menu'  # menu, play, game_over, highscores
        self.menu_index = 0
        self.score = 0
        self.highscore = self.load_highscore()
        self.reset()

    def reset(self):
        start = (COLS // 2, ROWS // 2)
        self.snake = Snake(start)
        self.place_food()
        self.place_wall()
        self.score = 0

    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    return int(f.read().strip() or 0)
            except Exception:
                return 0
        return 0

    def save_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'w') as f:
                f.write(str(self.highscore))
        except Exception:
            pass

    def place_food(self):
        while True:
            fx = random.randrange(COLS)
            fy = random.randrange(ROWS)
            if (fx, fy) not in self.snake.body:
                self.food = (fx, fy)
                break
    def place_wall(self):
        while True:
            fx = random.randrange(COLS)
            fy = random.randrange(ROWS)
            if (fx, fy) not in self.snake.body:
                self.wall = (fx, fy)
                break



class Snake:
    def __init__(self, start):
        self.body = [start]
        self.grow_pending = 3
        self.direction = (1, 0)  # unit vector on grid
        self.next_direction = self.direction
        self.pixel_pos = tuple(grid_to_pixel(*start))
    # draw in draw_play, update in update
    @property
    def head_grid(self):
        return pixel_to_grid(*self.pixel_pos)

    def update(self):
        # apply turn only when aligned to grid
        px, py = self.pixel_pos
        aligned = (px % GRID_SIZE == 0) and (py % GRID_SIZE == 0)
        if aligned:
            self.direction = self.next_direction

        dx, dy = self.direction
        px += dx * SPEED * GRID_SIZE
        py += dy * SPEED * GRID_SIZE

        # collision with screen edges
        if px < 0 or px > WIDTH:
            game.state = 'game_over'
        if py < 0 or py > HEIGHT:
            game.state = 'game_over'
        
        old_cell = self.body[0]
        self.pixel_pos = (px, py)
        new_cell = self.head_grid

        if new_cell != old_cell:
            self.body.insert(0, new_cell)
            if self.grow_pending > 0:
                self.grow_pending -= 1
            else:
                self.body.pop()
    # ausgelöst in on_key_down
    def turn(self, nx, ny):
        # prevent reversing
        if (nx, ny) == (-self.direction[0], -self.direction[1]):
            return
        self.next_direction = (nx, ny)

# game startet hier
game = Game()


def draw_menu():
    screen.fill((10, 10, 10))
    screen.draw.text('Snake', center=(WIDTH//2, HEIGHT//3), fontsize=80, color='white')
    options = ['Start', 'Highscores', 'Quit']
   # enumerate stellt paare (i, opt) bereit
    for i, opt in enumerate(options):
        color = 'yellow' if i == game.menu_index else 'white'
        screen.draw.text(opt, center=(WIDTH//2, HEIGHT//2 + i*40), fontsize=40, color=color)


def draw_play():
    screen.fill((0, 0, 0))
    # grid
    for x in range(COLS + 1):
        px = x * GRID_SIZE
        screen.draw.line((px, 0), (px, HEIGHT), (40, 40, 40))
    for y in range(ROWS + 1):
        py = y * GRID_SIZE
        screen.draw.line((0, py), (WIDTH, py), (40, 40, 40))

    # food
    fx, fy = game.food
    r = Rect((fx*GRID_SIZE, fy*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
    screen.draw.filled_rect(r, 'red')
    fx, fy = game.wall
    r = Rect((fx*GRID_SIZE, fy*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
    screen.draw.filled_rect(r, 'gray')

    # snake body (grid-aligned)
    for i, (gx, gy) in enumerate(game.snake.body):
        px, py = grid_to_pixel(gx, gy)
        c = 'green' if i == 0 else (20, 180, 20)
        screen.draw.filled_rect(Rect((px, py), (GRID_SIZE, GRID_SIZE)), c)

    # head (smooth)
    hx, hy = game.snake.pixel_pos
    screen.draw.filled_rect(Rect((hx, hy), (GRID_SIZE, GRID_SIZE)), 'lime')

    screen.draw.text(f'Score: {game.score}', topleft=(10, 10), color='white')


def draw_game_over():
    screen.fill((0, 0, 0))
    screen.draw.text('Game Over', center=(WIDTH//2, HEIGHT//3), fontsize=80, color='white')
    screen.draw.text(f'Score: {game.score}', center=(WIDTH//2, HEIGHT//2), fontsize=50, color='white')
    screen.draw.text('Press Enter to return to menu', center=(WIDTH//2, HEIGHT//2 + 80), fontsize=30, color='yellow')


def draw_highscores():
    screen.fill((0, 0, 0))
    screen.draw.text('Highscore', center=(WIDTH//2, HEIGHT//4), fontsize=60, color='white')
    screen.draw.text(str(game.highscore), center=(WIDTH//2, HEIGHT//2), fontsize=50, color='yellow')
    screen.draw.text('Press Enter to return', center=(WIDTH//2, HEIGHT//2 + 80), fontsize=30, color='white')


def draw():
    if game.state == 'menu':
        draw_menu()
    elif game.state == 'play':
        draw_play()
    elif game.state == 'game_over':
        draw_game_over()
    elif game.state == 'highscores':
        draw_highscores()


def update():
    if game.state == 'play':
        game.snake.update()
        # check food
        if game.snake.body[0] == game.food:
            game.score += 1
            game.snake.grow_pending += 1
            game.place_food()
        # check wall
        if game.snake.body[0] == game.wall:
            game.state = 'game_over'
            if game.score > game.highscore:
                game.highscore = game.score
                game.save_highscore()
        # self collision
        if game.snake.body[0] in game.snake.body[1:]:
            game.state = 'game_over'
            if game.score > game.highscore:
                game.highscore = game.score
                game.save_highscore()


def on_key_down(key):
    if game.state == 'menu':
        if key == keys.UP:
            game.menu_index = (game.menu_index - 1) % len(options)
        elif key == keys.DOWN:
            game.menu_index = (game.menu_index + 1) % len(options)
        elif key == keys.RETURN:
            # menu_index 0: start, 1: highscores, 2: quit
            if game.menu_index == 0:
                game.reset()
                game.state = 'play'
            elif game.menu_index == 1:
                game.state = 'highscores'
            elif game.menu_index == 2:
                exit()
    # snake bewegung
    elif game.state == 'play':
        if key == keys.UP:
            game.snake.turn(0, -1)
        elif key == keys.DOWN:
            game.snake.turn(0, 1)
        elif key == keys.LEFT:
            game.snake.turn(-1, 0)
        elif key == keys.RIGHT:
            game.snake.turn(1, 0)

    elif game.state in ('game_over', 'highscores'):
        if key == keys.RETURN:
            game.state = 'menu'


pgzrun.go()