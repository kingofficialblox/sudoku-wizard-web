import pygame

PRIMARY = (0, 120, 255)
BADGE_BLUE = (52, 120, 246)
BADGE_GREEN = (40, 167, 69)
BADGE_TEXT = (255, 255, 255)
TEXT_LIGHT = (45, 45, 45)
TEXT_DARK = (240, 240, 240)

class Button:

    def __init__(
    self,
    x,
    y,
    width,
    height,
    text,
    icon=None,
    bg_color=(245,245,250),
    hover_color=(255,255,255),
    border_color=(0,0,0)
):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.font = pygame.font.Font(
            "assets/fonts/Poppins-Bold.ttf",
            22
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
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.count = None
        self.selected = False
        self.text_color = TEXT_LIGHT

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

        # Image-only buttons use the PNG artwork as the complete control.
        # They keep the same hover glow and pressed motion without a second box.
        if self.icon and not self.text:
            scale = 1 + self.hover_amount * 0.08
            if mouse_pressed and hover:
                scale = 0.94
            image_size = (
                max(1, round(self.icon.get_width() * scale)),
                max(1, round(self.icon.get_height() * scale)),
            )
            icon = pygame.transform.smoothscale(self.icon, image_size)
            icon_rect = icon.get_rect(center=draw_rect.center)

            if self.hover_amount or self.selected:
                glow = pygame.Surface(
                    (icon_rect.width + 20, icon_rect.height + 20),
                    pygame.SRCALPHA,
                )
                pygame.draw.ellipse(
                    glow,
                    (*self.border_color, 80 if self.selected else int(55 * self.hover_amount)),
                    glow.get_rect(),
                )
                screen.blit(glow, (icon_rect.x - 10, icon_rect.y - 10))

            if self.selected:
                pygame.draw.circle(
                    screen,
                    PRIMARY,
                    icon_rect.center,
                    max(icon_rect.width, icon_rect.height) // 2 + 5,
                    3,
                )

            screen.blit(icon, icon_rect)
            return

        # Shadow
        shadow_rect = draw_rect.copy()

        if self.selected:
            shadow_rect.y += 7
        else:
            shadow_rect.y += 5 + int(self.hover_amount * 2)

        pygame.draw.rect(
            screen,
            self.border_color,
            shadow_rect,
            border_radius=12
        )

        # Colors
        # ---------------- Colors ----------------
        if self.selected:

            fill = (180, 210, 255)

            border = PRIMARY

            text_color = PRIMARY

        else:

            fill = (
                int(self.bg_color[0] + (self.hover_color[0] - self.bg_color[0]) * self.hover_amount),
                int(self.bg_color[1] + (self.hover_color[1] - self.bg_color[1]) * self.hover_amount),
                int(self.bg_color[2] + (self.hover_color[2] - self.bg_color[2]) * self.hover_amount)
            )

            border = self.border_color

            text_color = self.text_color
        if hover:
            glow = pygame.Surface(
                (draw_rect.width + 18, draw_rect.height + 18),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                glow,
                (*border, 45),
                glow.get_rect(),
                border_radius=18
            )

            screen.blit(
                glow,
                (draw_rect.x - 9, draw_rect.y - 9)
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
            2,
            border_radius=12
        )

        # Render text
        text = self.font.render(
            self.text,
            True,
            text_color
        )

        spacing = 14

        # -----------------------------
        # Button with icon
        # -----------------------------
        if self.icon:
            total_width = self.icon.get_width() + spacing + text.get_width()

            start_x = draw_rect.centerx - total_width // 2

            # Icon position
            icon = pygame.transform.smoothscale(
                self.icon,
                (32, 32)
            )
            icon_x = start_x
            icon_y = draw_rect.centery - self.icon.get_height() // 2

            screen.blit(self.icon, (icon_x, icon_y))

            # Text position
            text_x = icon_x + self.icon.get_width() + spacing
            text_y = draw_rect.centery - text.get_height() // 2

            screen.blit(text, (text_x, text_y))
        # -----------------------------
        # Button without icon
        # -----------------------------
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
                    PRIMARY,
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
