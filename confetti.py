import pygame
import random
import math
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

        # Spawn randomly across the top
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT * 4, 0)

        # Slow falling motion
        self.vx = random.uniform(-0.4, 0.4)
        self.vy = random.uniform(2.2, 5.5)

        self.width = random.randint(4, 10)
        self.height = random.randint(6, 18)

        self.color = random.choice(self.COLORS)

        self.angle = random.randint(0, 360)
        self.spin = random.uniform(-18, 18)

    def update(self):
        # Update position from velocity
        self.x += self.vx
        self.y += self.vy

        # Update rotation
        self.angle += self.spin

        # Gentle side-to-side drifting
        self.x += math.sin(self.y * 0.02 + self.angle * 0.03) * 0.8

        # Reappear at the top after leaving the screen
        if self.y > HEIGHT + 20:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(-HEIGHT * 4, -20)

            self.vx = random.uniform(-0.4, 0.4)
            self.vy = random.uniform(2.2, 5.5)

            self.angle = random.randint(0, 360)

    def draw(self, screen):

        surface = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )

        shape = random.randint(0, 2)

        if shape == 0:
            pygame.draw.rect(
                surface,
                self.color,
                (0, 0, self.width, self.height),
                border_radius=2
            )

        elif shape == 1:
            pygame.draw.ellipse(
                surface,
                self.color,
                (0, 0, self.width, self.height)
            )

        else:
            pygame.draw.polygon(
                surface,
                self.color,
                [
                    (self.width//2, 0),
                    (self.width, self.height//2),
                    (self.width//2, self.height),
                    (0, self.height//2)
                ]
            )

        rotated = pygame.transform.rotate(
            surface,
            self.angle
        )

        rect = rotated.get_rect(
            center=(self.x, self.y)
        )
        alpha = 255
        if self.y < 80:
            alpha = int((self.y + 80) / 160 * 255)
            alpha = max(0, min(alpha, 255))
        rotated.set_alpha(alpha)

        screen.blit(rotated, rect)