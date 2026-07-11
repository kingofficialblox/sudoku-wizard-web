import pygame

PRIMARY = (0, 120, 255)
BADGE_BLUE = (52, 120, 246)
BADGE_GREEN = (40, 167, 69)
BADGE_TEXT = (255, 255, 255)

class Button:

    def __init__(self, x, y, width, height, text, icon = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            26
        )
        self.count_font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            16
        )
        self.check_icon = pygame.image.load(
            "assets/images/check.png"
        ).convert_alpha()

        self.check_icon = pygame.transform.smoothscale(
            self.check_icon,
            (42, 42)
        )
        self.hover_amount = 0
        self.count = None
        self.selected = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        hover = self.rect.collidepoint(mouse_pos)
        # Smooth hover animation
        if hover:
            self.hover_amount = min(self.hover_amount + 0.15, 1)
        else:
            self.hover_amount = max(self.hover_amount - 0.15, 0)

        # Button moves down slightly when clicked
        # Button animation
        if self.selected:
            offset = -3

        elif mouse_pressed and hover:
            offset = 1

        else:
            offset = int(-3 * self.hover_amount)

        draw_rect = self.rect.copy()
        draw_rect.y += offset

        # Shadow
        shadow_rect = draw_rect.copy()

        if self.selected:
            shadow_rect.y += 7
        else:
            shadow_rect.y += 5 + int(self.hover_amount * 2)

        pygame.draw.rect(
            screen,
            (190, 195, 205),
            shadow_rect,
            border_radius=12
        )

        # Colors
        # ---------------- Colors ----------------
        if self.selected:
            fill = (225, 238, 255)
            border = PRIMARY
            text_color = PRIMARY
        else:
            fill = (
                int(250 - 15 * self.hover_amount),
                int(250 - 8 * self.hover_amount),
                255
            )

            border = (
                int(215 - 40 * self.hover_amount),
                int(220 - 50 * self.hover_amount),
                int(228 - 20 * self.hover_amount)
            )

            text_color = (
                int(45 - 10 * self.hover_amount),
                int(45 + 40 * self.hover_amount),
                int(45 + 170 * self.hover_amount)
            )

        # Button
        pygame.draw.rect(
            screen,
            fill,
            draw_rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            border,
            draw_rect,
            3 if self.selected else 2,
            border_radius=12
        )

        text = self.font.render(
            self.text,
            True,
            text_color
        )

        if self.icon:

            spacing = 8

            total_width = self.icon.get_width() + spacing + text.get_width()

            start_x = draw_rect.centerx - total_width // 2

            icon_rect = self.icon.get_rect(
                midleft=(start_x, draw_rect.centery)
            )

            text_rect = text.get_rect(
                midleft=(icon_rect.right + spacing, draw_rect.centery)
            )

            screen.blit(self.icon, icon_rect)

        else:

            text_rect = text.get_rect(center=draw_rect.center)

        screen.blit(text, text_rect)

        if self.count is not None:
            badge_x = draw_rect.right - 14
            badge_y = draw_rect.top + 14
            radius = 11

            if self.count == 0:
                # Green badge
                pygame.draw.circle(
                    screen,
                    BADGE_GREEN,
                    (badge_x, badge_y),
                    radius
                )

                icon_rect = self.check_icon.get_rect(
                    center=(badge_x + 1, badge_y)
                )

                screen.blit(self.check_icon, icon_rect)

            else:
                # Blue badge
                pygame.draw.circle(
                    screen,
                    BADGE_BLUE,
                    (badge_x, badge_y),
                    radius
                )

                count = self.count_font.render(
                    str(self.count),
                    True,
                    BADGE_TEXT
                )

                count_rect = count.get_rect(
                    center=(badge_x, badge_y)
                )

                screen.blit(count, count_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
