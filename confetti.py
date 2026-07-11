import pygame
import random
from constants import WIDTH, HEIGHT


class Confetti:

    COLORS = [
        (255, 80, 80),
        (255, 210, 0),
        (0, 210, 120),
        (60, 170, 255),
        (170, 90, 255),
        (255, 110, 180)
    ]

    def __init__(self):

        # Left cannon or right cannon
        self.side = random.choice(("left", "right"))

        if self.side == "left":
            self.x = random.randint(40, 220)
            self.vx = random.uniform(2, 10)
        else:
            self.x = random.randint(WIDTH - 220, WIDTH - 40)
            self.vx = random.uniform(-10, -2)

        # Spawn near the top
        self.y = 120

        # Shoot upward
        self.vy = random.uniform(-13, -8)   

        self.width = random.randint(5, 9)
        self.height = random.randint(10, 18)

        self.color = random.choice(self.COLORS)

        self.angle = random.randint(0, 360)
        self.spin = random.uniform(-12, 12)

    def update(self):

        self.x += self.vx
        self.y += self.vy

        # Gravity
        self.vy += 0.35

        # Air resistance
        self.vx *= 0.995

        self.angle += self.spin

    def draw(self, screen):

        surface = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            surface,
            self.color,
            (0, 0, self.width, self.height),
            border_radius=2
        )

        rotated = pygame.transform.rotate(
            surface,
            self.angle
        )

        rect = rotated.get_rect(
            center=(self.x, self.y)
        )

        screen.blit(rotated, rect)