class Level:
    def __init__(self, difficulty):
        self.level = difficulty
        self.base_speed = 10

    def get_speed(self):
        return self.base_speed + (self.level - 1) * 5

    def increase_level(self):
        self.level += 1
