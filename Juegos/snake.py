import pygame
import sys
import time
import random

# Inicialización de Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (40, 40, 40)

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Definir tamaño de la cuadrícula
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Configuración de velocidad
EASY_SPEED = 10
NORMAL_SPEED = 20
HARD_SPEED = 30

# Inicializar la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Establecer icono de la ventana
icon_path = 'Juegos/utils/img/snake.jpeg'
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# Fuente
font = pygame.font.Font(None, 36)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

class Snake:
    def __init__(self):
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = (0, -1)
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if len(self.positions) > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False
        else:
            self.positions.insert(0, new)
            if not self.grow:
                self.positions.pop()
            else:
                self.grow = False
            return True

    def reset(self):
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = (0, -1)
        self.grow = False

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, GREEN, pygame.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.turn((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    return 'pause'

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def game_over_screen(score, duration):
    screen.fill(BLACK)
    draw_text(screen, 'Game Over', 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    draw_text(screen, f'Score: {score}', 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(screen, f'Time: {duration}s', 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, 'Press any key to return to main menu', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()
    time.sleep(1)  # Pequeña pausa para evitar que se detecte la última tecla presionada durante el juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

def main(speed):
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    start_time = time.time()
    paused = False

    while True:
        if not paused:
            result = snake.handle_keys()
            if result == 'pause':
                paused = True

            if not snake.move():
                duration = int(time.time() - start_time)
                game_over_screen(score, duration)
                return

            if snake.get_head_position() == food.position:
                score += 1
                snake.grow = True
                food.randomize_position()

            screen.fill(BLACK)
            draw_grid()
            snake.draw(screen)
            food.draw(screen)
            draw_text(screen, f'Score: {score}', 24, 50, 10)
            draw_text(screen, f'Time: {int(time.time() - start_time)}s', 24, 150, 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(speed)

        else:
            draw_text(screen, 'Paused', 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, 'Press ESC to resume or Q to quit', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

def start_screen():
    while True:
        screen.fill(BLACK)
        draw_text(screen, 'Snake Game', 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text(screen, 'Press 1 for Easy', 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        draw_text(screen, 'Press 2 for Normal', 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        draw_text(screen, 'Press 3 for Hard', 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return EASY_SPEED
                elif event.key == pygame.K_2:
                    return NORMAL_SPEED
                elif event.key == pygame.K_3:
                    return HARD_SPEED

if __name__ == '__main__':
    while True:
        speed = start_screen()
        main(speed)
