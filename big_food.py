import random
import pygame

class BigFood:
    def __init__(self, screen_width, screen_height, grid_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.position = None
        self.spawn_time = 0

    def randomize_position(self, snake_positions):
        while True:
            new_position = (random.randint(0, (self.screen_width // self.grid_size) - 1) * self.grid_size,
                            random.randint(0, (self.screen_height // self.grid_size) - 1) * self.grid_size)
            if new_position not in snake_positions:
                self.position = new_position
                self.spawn_time = pygame.time.get_ticks()
                break

    def draw(self, surface):
        if self.position:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position, (self.grid_size, self.grid_size)))
