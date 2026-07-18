import pygame

from constants import *
from themes import DARK, LIGHT


class SettingsMenu:
    """The settings view used from the main menu."""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 60)
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 28)
        self.small_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 21)
        self.dragging = None
        self.music_slider = pygame.Rect(0, 0, 420, 10)
        self.sfx_slider = pygame.Rect(0, 0, 420, 10)
        self.theme_button = pygame.Rect(0, 0, 420, 62)
        self.back_button = pygame.Rect(0, 0, 220, 60)
        self._layout()

    def _layout(self):
        center_x = WIDTH // 2
        self.music_slider.center = (center_x, 380)
        self.sfx_slider.center = (center_x, 520)
        self.theme_button.center = (center_x, 675)
        self.back_button.center = (center_x, 830)

    @staticmethod
    def _hit_box(slider):
        return slider.inflate(0, 34)

    def _set_volume(self, slider_name, mouse_x):
        slider = self.music_slider if slider_name == "music" else self.sfx_slider
        volume = max(0.0, min(1.0, (mouse_x - slider.left) / slider.width))
        if slider_name == "music":
            self.game.set_music_volume(volume)
        else:
            self.game.set_sfx_volume(volume)
        self.game.save_settings()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self._hit_box(self.music_slider).collidepoint(pos):
                self.dragging = "music"
                self._set_volume("music", pos[0])
            elif self._hit_box(self.sfx_slider).collidepoint(pos):
                self.dragging = "sfx"
                self._set_volume("sfx", pos[0])
            elif self.theme_button.collidepoint(pos):
                self.game.theme = DARK if self.game.theme == LIGHT else LIGHT
                self.game.save_settings()
                self.game.play_sound(self.game.click_sound)
            elif self.back_button.collidepoint(pos):
                self.game.play_sound(self.game.click_sound)
                self.game.settings_open = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_volume(self.dragging, event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = None

    def _draw_slider(self, label, slider, value, icon):
        theme = self.game.theme
        label_y = slider.y - 65
        self.screen.blit(icon, (slider.x, label_y - 2))
        text = self.font.render(label, True, theme["text"])
        self.screen.blit(text, (slider.x + 38, label_y))
        percent = self.small_font.render(f"{round(value * 100)}%", True, theme["secondary"])
        self.screen.blit(percent, percent.get_rect(midright=(slider.right, label_y + 15)))
        pygame.draw.rect(self.screen, theme["popup_border"], slider, border_radius=5)
        filled = slider.copy()
        filled.width = round(slider.width * value)
        if filled.width:
            pygame.draw.rect(self.screen, theme["accent"], filled, border_radius=5)
        knob_x = round(slider.left + slider.width * value)
        pygame.draw.circle(self.screen, (*theme["shadow"], 90), (knob_x + 2, slider.centery + 3), 15)
        pygame.draw.circle(self.screen, theme["popup"], (knob_x, slider.centery), 14)
        pygame.draw.circle(self.screen, theme["accent"], (knob_x, slider.centery), 14, 3)

    def _draw_button(self, rect, text):
        theme = self.game.theme
        color = theme["button_hover"] if rect.collidepoint(pygame.mouse.get_pos()) else theme["button"]
        pygame.draw.rect(self.screen, theme["popup_border"], rect.move(0, 4), border_radius=15)
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        pygame.draw.rect(self.screen, theme["popup_border"], rect, 2, border_radius=15)
        label = self.small_font.render(text, True, theme["text"])
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw(self):
        self._layout()
        theme = self.game.theme
        self.screen.fill(theme["background"])
        panel = pygame.Rect(WIDTH // 2 - 310, 105, 620, 810)
        pygame.draw.rect(self.screen, theme["shadow"], panel.move(0, 8), border_radius=28)
        pygame.draw.rect(self.screen, theme["popup"], panel, border_radius=28)
        pygame.draw.rect(self.screen, theme["popup_border"], panel, 2, border_radius=28)
        title = self.title_font.render("Settings", True, theme["text"])
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 185)))
        subtitle = self.small_font.render("Customize your game experience", True, theme["secondary"])
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 230)))
        pygame.draw.line(self.screen, theme["popup_border"], (panel.x + 55, 275), (panel.right - 55, 275), 2)
        self._draw_slider("Music", self.music_slider, self.game.music_volume, self.game.music_icon)
        self._draw_slider("Sound effects", self.sfx_slider, self.game.sfx_volume, self.game.sfx_icon)
        mode = "Dark" if self.game.theme == DARK else "Light"
        self._draw_button(self.theme_button, f"Theme: {mode}   •   Change theme")
        self._draw_button(self.back_button, "Back")
