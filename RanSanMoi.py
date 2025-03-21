import pygame
import sys
import random
from big_food import BigFood
from levels import Level

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRIDSIZE

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + (x * GRIDSIZE), cur[1] + (y * GRIDSIZE))

        if (
            new[0] < 0 or new[0] >= SCREEN_WIDTH
            or new[1] < 0 or new[1] >= SCREEN_HEIGHT
            or new in self.positions[2:]
        ):
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(p, (GRIDSIZE, GRIDSIZE)))

class Food:
    def __init__(self):
        self.color = (223, 163, 49)
        self.position = (0, 0)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        while True:
            new_position = (
                random.randint(0, GRID_WIDTH - 1) * GRIDSIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            )
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position, (GRIDSIZE, GRIDSIZE)))

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, GRIDSIZE):
        for y in range(0, SCREEN_HEIGHT, GRIDSIZE):
            if (x // GRIDSIZE + y // GRIDSIZE) % 2 == 0:
                pygame.draw.rect(surface, (30, 30, 30), pygame.Rect(x, y, GRIDSIZE, GRIDSIZE))

def show_start_screen(screen):
    """ Hiển thị màn hình chờ """
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("monospace", 24)
    title_text = font.render("SNAKE GAME", 1, (0, 255, 0))
    start_text = font.render("Nhấn SPACE để bắt đầu", 1, (255, 255, 255))
    
    screen.blit(title_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface = pygame.Surface(screen.get_size()).convert()
    myfont = pygame.font.SysFont("monospace", 16)

    show_start_screen(screen)  

    level = Level(1)
    level.speed = 5  
    snake = Snake()
    food = Food()
    big_food = BigFood(SCREEN_WIDTH, SCREEN_HEIGHT, GRIDSIZE)
    food_count = 0

    game_over = False
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif game_over and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    snake.reset()
                    food.randomize_position(snake.positions)
                    big_food.position = None
                    food_count = 0
                    game_over = False
                    level.speed = 5 
                elif not paused:
                    if event.key == pygame.K_UP:
                        snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.turn((1, 0))

        if not paused and not game_over:
            surface.fill((0, 0, 0))
            draw_grid(surface)
            snake.draw(surface)
            food.draw(surface)
            if big_food.position:
                big_food.draw(surface)

        if not paused:
            if not snake.move():
                game_over = True

            if snake.get_head_position() == food.position:
                snake.score += 1
                food_count += 1
                food.randomize_position(snake.positions)

                if snake.score % 5 == 0:
                    level.increase_level()
                    level.speed += 1  # Tăng tốc độ dần

            if food_count >= 10 and not big_food.position:
                big_food.randomize_position(snake.positions)
                food_count = 0

            if big_food.position and snake.get_head_position() == big_food.position:
                snake.score += 5
                big_food.position = None

            if big_food.position and pygame.time.get_ticks() - big_food.spawn_time > 5000:
                big_food.position = None

        if paused or game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))

            if paused:
                pause_text = myfont.render("Đã tạm dừng. Nhấn P để tiếp tục", 1, (255, 255, 255))
                surface.blit(pause_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

            if game_over:
                game_over_text = myfont.render("Bạn đã thua! Nhấn SHIFT để chơi lại!", 1, (255, 0, 0))
                surface.blit(game_over_text, (SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2))

        score_text = myfont.render(f"Score: {snake.score} | Level: {level.level}", 1, (255, 255, 255))
        surface.blit(score_text, (5, 5))

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(level.speed)

if __name__ == "__main__":
    main()