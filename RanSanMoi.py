import pygame
import sys
import random
import os

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

class Snake:
    def __init__(self):
        self.high_score = load_high_score() 
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.head_color = (255, 0, 0)
        self.body_color = (0, 255, 0)

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
        for i, p in enumerate(self.positions):
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            color = self.head_color if i == 0 else self.body_color
            pygame.draw.rect(surface, color, r)

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score) 

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
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

class BigFood:
    def __init__(self):
        self.color = (255, 165, 0)
        self.position = None 
        self.spawn_time = None 

    def randomize_position(self, snake_positions):
        while True:
            new_position = (
                random.randint(0, GRID_WIDTH - 1) * GRIDSIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE,
            )
            if new_position not in snake_positions:
                self.position = new_position
                self.spawn_time = pygame.time.get_ticks()
                break

    def draw(self, surface):
        if self.position:
            r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (255, 69, 0), r, 1)

def draw_grid(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = (93, 216, 228) if (x + y) % 2 == 0 else (84, 194, 205)
            r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, color, r)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size()).convert()
    myfont = pygame.font.SysFont("monospace", 16)

    snake = Snake()
    food = Food()
    big_food = BigFood()
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
                elif event.key == pygame.K_SPACE and game_over:  
                    snake.reset()
                    food.randomize_position(snake.positions)
                    big_food.position = None
                    food_count = 0
                    game_over = False  
                elif not paused:
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)

        if not paused: 
            draw_grid(surface)

            if not snake.move():
                game_over = True
                snake.update_high_score()

            if snake.get_head_position() == food.position:
                snake.score += 1
                food_count += 1 
                food.randomize_position(snake.positions)

            if food_count >= 10 and not big_food.position:
                big_food.randomize_position(snake.positions)
                food_count = 0

            if big_food.position and snake.get_head_position() == big_food.position:
                snake.score += 5 
                big_food.position = None

            if big_food.position and pygame.time.get_ticks() - big_food.spawn_time > 5000:
                big_food.position = None

            snake.draw(surface)
            food.draw(surface)
            if big_food.position:
                big_food.draw(surface)

        if paused or game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)  
            overlay.fill((0, 0, 0))  
            surface.blit(overlay, (0, 0))

            if paused:
                pause_text = myfont.render("Đã tạm dừng. Nhấn P để chơi tiếp", 1, (255, 255, 255))
                surface.blit(pause_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
            elif game_over:
                game_over_text = myfont.render("Bạn đã thua! Bấm phím SPACE để chơi lại!", 1, (255, 0, 0))
                surface.blit(game_over_text, (SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2))

        score_text = myfont.render(f"Score: {snake.score}", 1, (0, 0, 0))
        high_score_text = myfont.render(f"High Score: {snake.high_score}", 1, (0, 0, 0))
        
        surface.blit(score_text, (5, 5))
        surface.blit(high_score_text, (5, 25))

        screen.blit(surface, (0, 0))
        pygame.display.update()

        clock.tick(5)

if __name__ == "__main__":
    main()
