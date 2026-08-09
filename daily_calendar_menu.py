import calendar
from datetime import date, timedelta

import pygame

from button import Button
from constants import HEIGHT, WIDTH, PORTRAIT_MODE


class DailyCalendarMenu:
    """A compact month view of Daily Challenge progress."""

    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 42 if PORTRAIT_MODE else 48)
        self.font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 18 if PORTRAIT_MODE else 20)
        self.small_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 15 if PORTRAIT_MODE else 16)
        self.streak_value_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 32 if PORTRAIT_MODE else 36)
        self.streak_icon = pygame.transform.smoothscale(
            pygame.image.load("assets/images/streak_fire.png").convert_alpha(), (52, 52)
        )
        self.back_button = Button(WIDTH // 2 - 110, HEIGHT - (290 if PORTRAIT_MODE else 150), 220, 55, "BACK")
        today = date.today()
        self.view_year, self.view_month = today.year, today.month
        self.previous_month_button = pygame.Rect(0, 0, 42, 38)
        self.next_month_button = pygame.Rect(0, 0, 42, 38)

    def _completed_dates(self, daily):
        completed = set(daily.get("completed_dates", []))
        if daily.get("last_completed") and daily.get("streak", 0):
            try:
                latest = date.fromisoformat(daily["last_completed"])
                completed.update((latest - timedelta(days=offset)).isoformat() for offset in range(daily["streak"]))
            except ValueError:
                pass
        return completed

    def _change_month(self, offset):
        month = self.view_month + offset
        year = self.view_year
        if month < 1:
            year, month = year - 1, 12
        elif month > 12:
            year, month = year + 1, 1
        self.view_year, self.view_month = year, month

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.clicked(event.pos):
                self.game.play_sound(self.game.click_sound)
                self.game.daily_calendar_open = False
                return
            daily = self.game.stats.data.get("daily", {})
            completed = self._completed_dates(daily)
            earliest = min((date.fromisoformat(value) for value in completed), default=date.today())
            current = date(self.view_year, self.view_month, 1)
            if self.previous_month_button.collidepoint(event.pos) and current > date(earliest.year, earliest.month, 1):
                self._change_month(-1)
                self.game.play_sound(self.game.click_sound)
            elif self.next_month_button.collidepoint(event.pos) and current < date(date.today().year, date.today().month, 1):
                self._change_month(1)
                self.game.play_sound(self.game.click_sound)

    def draw(self):
        screen, theme = self.game.screen, self.game.theme
        screen.fill(theme["background"])
        panel = pygame.Rect(WIDTH // 2 - min(WIDTH - 50, 680) // 2, 70, min(WIDTH - 50, 680), HEIGHT - (300 if PORTRAIT_MODE else 220))
        pygame.draw.rect(screen, theme["shadow"], panel.move(0, 8), border_radius=28)
        pygame.draw.rect(screen, theme["popup"], panel, border_radius=28)
        pygame.draw.rect(screen, theme["popup_border"], panel, 2, border_radius=28)
        daily = self.game.stats.data.get("daily", {})
        title = self.title_font.render("DAILY CALENDAR", True, theme["text"])
        screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 58)))
        streak = daily.get("streak", 0)
        best = daily.get("best_streak", 0)
        card_w = (panel.width - 110) // 2
        for index, (label, value) in enumerate((("CURRENT STREAK", streak), ("BEST STREAK", best))):
            card = pygame.Rect(panel.x + 45 + index * (card_w + 20), panel.y + 92, card_w, 82)
            glow = pygame.Surface((card.width + 14, card.height + 14), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*theme["accent"], 38), glow.get_rect(), border_radius=22)
            screen.blit(glow, (card.x - 7, card.y - 7))
            pygame.draw.rect(screen, theme["shadow"], card.move(0, 7), border_radius=18)
            pygame.draw.rect(screen, theme["popup"], card, border_radius=18)
            pygame.draw.rect(screen, theme["accent"], card, 2, border_radius=18)
            pygame.draw.rect(screen, theme["accent"], (card.x + 18, card.y + 8, card.width - 36, 4), border_radius=2)
            screen.blit(self.streak_icon, self.streak_icon.get_rect(center=(card.x + 45, card.centery)))
            label_surface = self.small_font.render(label, True, theme["secondary"])
            value_surface = self.streak_value_font.render(str(value), True, theme["accent"])
            unit_surface = self.small_font.render("DAYS", True, theme["text"])
            screen.blit(label_surface, (card.x + 86, card.y + 13))
            value_rect = value_surface.get_rect(midleft=(card.x + 86, card.y + 55))
            screen.blit(value_surface, value_rect)
            screen.blit(unit_surface, unit_surface.get_rect(midleft=(value_rect.right + 9, card.y + 57)))
        today = date.today()
        month_date = date(self.view_year, self.view_month, 1)
        month_title = self.font.render(month_date.strftime("%B %Y").upper(), True, theme["text"])
        screen.blit(month_title, month_title.get_rect(center=(panel.centerx, panel.y + 210)))
        self.previous_month_button.center = (panel.centerx - 150, panel.y + 210)
        self.next_month_button.center = (panel.centerx + 150, panel.y + 210)
        completed = self._completed_dates(daily)
        earliest = min((date.fromisoformat(value) for value in completed), default=today)
        can_go_back = month_date > date(earliest.year, earliest.month, 1)
        can_go_forward = month_date < date(today.year, today.month, 1)
        for rect, arrow, enabled in ((self.previous_month_button, "<", can_go_back), (self.next_month_button, ">", can_go_forward)):
            color = theme["accent"] if enabled else theme["popup_border"]
            pygame.draw.rect(screen, theme["button"], rect, border_radius=10)
            pygame.draw.rect(screen, color, rect, 2, border_radius=10)
            arrow_surface = self.font.render(arrow, True, color)
            screen.blit(arrow_surface, arrow_surface.get_rect(center=rect.center))
        grid = pygame.Rect(panel.x + 52, panel.y + 245, panel.width - 104, min(440, panel.height - 370))
        tracked_from = min(completed) if completed else None
        weekdays = ("M", "T", "W", "T", "F", "S", "S")
        cell_w, cell_h = grid.width // 7, grid.height // 7
        for col, label in enumerate(weekdays):
            text = self.small_font.render(label, True, theme["secondary"])
            screen.blit(text, text.get_rect(center=(grid.x + col * cell_w + cell_w // 2, grid.y + cell_h // 2)))
        for row, week in enumerate(calendar.monthcalendar(month_date.year, month_date.month), start=1):
            for col, day in enumerate(week):
                if not day:
                    continue
                rect = pygame.Rect(grid.x + col * cell_w + 4, grid.y + row * cell_h + 4, cell_w - 8, cell_h - 8)
                day_date = date(month_date.year, month_date.month, day)
                day_key = day_date.isoformat()
                if day_key in completed:
                    fill, border, color = (255, 156, 45), (255, 194, 90), (255, 255, 255)
                elif tracked_from and day_key >= tracked_from and day_date < today:
                    fill, border, color = (115, 42, 48), (220, 75, 82), (255, 230, 230)
                elif day_date == today:
                    fill, border, color = (115, 42, 48), (220, 75, 82), (255, 230, 230)
                else:
                    fill, border = theme["button"], theme["popup_border"]
                    color = theme["secondary"]
                pygame.draw.rect(screen, fill, rect, border_radius=10)
                pygame.draw.rect(screen, border, rect, 2, border_radius=10)
                value = self.font.render(str(day), True, color)
                screen.blit(value, value.get_rect(center=rect.center))
        key = self.small_font.render("Orange = completed  •  Red = missed / today", True, theme["secondary"])
        screen.blit(key, key.get_rect(center=(panel.centerx, grid.bottom + 30)))
        self.back_button.bg_color = theme["button"]
        self.back_button.hover_color = theme["button_hover"]
        self.back_button.border_color = theme["grid"]
        self.back_button.text_color = theme["text"]
        self.back_button.draw(screen)
