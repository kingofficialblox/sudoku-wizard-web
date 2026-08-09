import pygame

from button import Button
from constants import HEIGHT, WIDTH, PORTRAIT_MODE


class StoreMenu:
    HINT_COST = 1_000
    AUTO_NOTES_COST = 1_750

    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 42 if PORTRAIT_MODE else 48)
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 18 if PORTRAIT_MODE else 20)
        self.value_font = pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 24 if PORTRAIT_MODE else 28)
        self.hint_buy_button = Button(0, 0, 250, 54, "BUY - 1000")
        self.auto_notes_buy_button = Button(0, 0, 250, 54, "BUY - 1750")
        self.cosmetic_ids = ("violet", "ocean", "emerald", "sunset")
        self.cosmetic_buttons = [Button(0, 0, 150, 54, "") for _ in self.cosmetic_ids]
        self.back_button = Button(WIDTH // 2 - 110, HEIGHT - (290 if PORTRAIT_MODE else 150), 220, 55, "BACK")
        self.message = ""
        self.message_until = 0
        self.aura_scroll = 0
        self.aura_max_scroll = 0
        self.aura_area = pygame.Rect(0, 0, 0, 0)
        self.aura_dragging = False
        self.aura_drag_y = 0
        self.aura_scroll_track = pygame.Rect(0, 0, 0, 0)
        self.aura_scroll_thumb = pygame.Rect(0, 0, 0, 0)
        self.aura_dragging_thumb = False
        self.aura_thumb_offset = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.aura_scroll = max(0, min(self.aura_max_scroll, self.aura_scroll - event.y * 48))
            return
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.aura_dragging = False
            self.aura_dragging_thumb = False
            return
        if event.type == pygame.MOUSEMOTION and self.aura_dragging_thumb:
            usable_height = max(1, self.aura_scroll_track.height - self.aura_scroll_thumb.height)
            ratio = max(0.0, min(1.0, (event.pos[1] - self.aura_scroll_track.y - self.aura_thumb_offset) / usable_height))
            self.aura_scroll = int(ratio * self.aura_max_scroll)
            return
        if event.type == pygame.MOUSEMOTION and self.aura_dragging:
            self.aura_scroll = max(0, min(self.aura_max_scroll, self.aura_scroll + self.aura_drag_y - event.pos[1]))
            self.aura_drag_y = event.pos[1]
            return
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if event.button in (4, 5):
            self.aura_scroll = max(0, min(self.aura_max_scroll, self.aura_scroll + (48 if event.button == 5 else -48)))
            return
        if event.button != 1:
            return
        if self.back_button.clicked(event.pos):
            self.game.play_sound(self.game.click_sound)
            self.game.store_open = False
            return
        if self.aura_scroll_thumb.collidepoint(event.pos):
            self.aura_dragging_thumb = True
            self.aura_thumb_offset = event.pos[1] - self.aura_scroll_thumb.y
            return
        if self.aura_scroll_track.collidepoint(event.pos):
            usable_height = max(1, self.aura_scroll_track.height - self.aura_scroll_thumb.height)
            ratio = max(0.0, min(1.0, (event.pos[1] - self.aura_scroll_track.y - self.aura_scroll_thumb.height // 2) / usable_height))
            self.aura_scroll = int(ratio * self.aura_max_scroll)
            return
        if self.hint_buy_button.clicked(event.pos):
            self.game.play_sound(self.game.click_sound)
            if self.game.stats.buy_hint(None, self.HINT_COST):
                self.message = "1 shared Hint Token added!"
                self.game.logic.hint_tokens = self.game.stats.get_hint_tokens()
            else:
                self.message = "Not enough Coins yet."
            self.message_until = pygame.time.get_ticks() + 1800
            return
        if self.auto_notes_buy_button.clicked(event.pos):
            self.game.play_sound(self.game.click_sound)
            if self.game.stats.buy_auto_notes(self.AUTO_NOTES_COST):
                self.message = "1 Auto Notes Token added!"
                self.game.logic.auto_notes_tokens = self.game.stats.get_auto_notes_tokens()
            else:
                self.message = "Not enough Coins yet."
            self.message_until = pygame.time.get_ticks() + 1800
            return
        for cosmetic_id, button in zip(self.cosmetic_ids, self.cosmetic_buttons):
            if button.clicked(event.pos):
                self.game.play_sound(self.game.click_sound)
                result = self.game.stats.buy_or_equip_cosmetic(cosmetic_id)
                item = self.game.stats.COSMETICS[cosmetic_id]
                self.message = (
                    f"{item['name']} equipped!" if result == "equipped"
                    else "Not enough Coins yet."
                )
                if result == "equipped":
                    self.game.apply_cosmetic_aura()
                self.message_until = pygame.time.get_ticks() + 1800
                return
        if self.aura_area.collidepoint(event.pos):
            self.aura_dragging = True
            self.aura_drag_y = event.pos[1]

    def draw(self):
        screen, theme = self.game.screen, self.game.theme
        screen.fill(theme["background"])
        panel = pygame.Rect(WIDTH // 2 - min(WIDTH - 50, 720) // 2, 80, min(WIDTH - 50, 720), HEIGHT - (330 if PORTRAIT_MODE else 240))
        pygame.draw.rect(screen, theme["shadow"], panel.move(0, 8), border_radius=28)
        pygame.draw.rect(screen, theme["popup"], panel, border_radius=28)
        pygame.draw.rect(screen, theme["popup_border"], panel, 2, border_radius=28)
        title = self.title_font.render("WIZARD STORE", True, theme["text"])
        screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.y + 65)))
        coins = self.game.stats.data.get("coins", 0)
        coin_line = self.value_font.render(f"{coins} COINS", True, (245, 190, 35))
        screen.blit(coin_line, coin_line.get_rect(center=(WIDTH // 2, panel.y + 118)))
        pygame.draw.line(screen, theme["accent"], (panel.x + 50, panel.y + 150), (panel.right - 50, panel.y + 150), 2)

        item = pygame.Rect(panel.x + 38, panel.y + 185, panel.width - 76, 135)
        pygame.draw.rect(screen, theme["button"], item, border_radius=20)
        pygame.draw.rect(screen, theme["accent"], item, 2, border_radius=20)
        hint_title = self.value_font.render("HINT TOKEN", True, theme["text"])
        detail = self.font.render("One shared balance for every difficulty and mode.", True, theme["secondary"])
        screen.blit(hint_title, hint_title.get_rect(center=(WIDTH // 2, item.y + 30)))
        screen.blit(detail, detail.get_rect(center=(WIDTH // 2, item.y + 59)))

        shared = self.game.stats.get_hint_tokens()
        balance = self.font.render(f"AVAILABLE: {shared}", True, theme["accent"])
        screen.blit(balance, balance.get_rect(center=(panel.right - 110, item.y + 30)))
        self.hint_buy_button.rect.center = (WIDTH // 2, item.bottom - 32)
        self.hint_buy_button.bg_color = theme["button"]
        self.hint_buy_button.hover_color = theme["button_hover"]
        self.hint_buy_button.border_color = theme["accent"]
        self.hint_buy_button.text_color = theme["text"]
        self.hint_buy_button.draw(screen)

        auto_item = pygame.Rect(panel.x + 38, panel.y + 335, panel.width - 76, 135)
        pygame.draw.rect(screen, theme["button"], auto_item, border_radius=20)
        pygame.draw.rect(screen, (55, 150, 255), auto_item, 2, border_radius=20)
        auto_title = self.value_font.render("AUTO NOTES TOKEN", True, theme["text"])
        auto_detail = self.font.render("Fills every empty cell with valid candidates.", True, theme["secondary"])
        auto_balance = self.font.render(f"AVAILABLE: {self.game.stats.get_auto_notes_tokens()}", True, (55, 150, 255))
        screen.blit(auto_title, auto_title.get_rect(center=(WIDTH // 2, auto_item.y + 30)))
        screen.blit(auto_detail, auto_detail.get_rect(center=(WIDTH // 2, auto_item.y + 59)))
        screen.blit(auto_balance, auto_balance.get_rect(center=(panel.right - 120, auto_item.y + 30)))
        self.auto_notes_buy_button.rect.center = (WIDTH // 2, auto_item.bottom - 32)
        self.auto_notes_buy_button.bg_color = theme["button"]
        self.auto_notes_buy_button.hover_color = theme["button_hover"]
        self.auto_notes_buy_button.border_color = (55, 150, 255)
        self.auto_notes_buy_button.text_color = theme["text"]
        self.auto_notes_buy_button.draw(screen)

        cosmetic_title = self.value_font.render("COLOR AURAS", True, theme["text"])
        screen.blit(cosmetic_title, cosmetic_title.get_rect(center=(WIDTH // 2, panel.y + 520)))
        owned = self.game.stats.data.get("cosmetics", {}).get("owned", ["violet"])
        equipped = self.game.stats.data.get("cosmetics", {}).get("equipped", "violet")
        self.aura_area = pygame.Rect(panel.x + 42, panel.y + 550, panel.width - 64, panel.bottom - (panel.y + 650))
        content_height = len(self.cosmetic_ids) * 86
        self.aura_max_scroll = max(0, content_height - self.aura_area.height)
        self.aura_scroll = min(self.aura_scroll, self.aura_max_scroll)
        previous_clip = screen.get_clip()
        screen.set_clip(self.aura_area)
        for index, (cosmetic_id, button) in enumerate(zip(self.cosmetic_ids, self.cosmetic_buttons)):
            item_data = self.game.stats.COSMETICS[cosmetic_id]
            button.rect = pygame.Rect(panel.x + 70, self.aura_area.y + index * 86 - self.aura_scroll, panel.width - 140, 60)
            is_owned = cosmetic_id in owned
            is_equipped = cosmetic_id == equipped
            button.bg_color = item_data["accent"] if is_equipped else theme["button"]
            button.hover_color = item_data["accent"] if is_owned else theme["button_hover"]
            button.border_color = item_data["accent"]
            button.text_color = theme["popup"] if is_equipped else theme["text"]
            action = "EQUIPPED" if is_equipped else ("EQUIP" if is_owned else f"{item_data['cost']} COINS")
            button.text = f"{item_data['name']}  •  {action}"
            button.draw(screen)
        screen.set_clip(previous_clip)
        if self.aura_max_scroll:
            track = pygame.Rect(panel.right - 25, self.aura_area.y, 5, self.aura_area.height)
            thumb_height = max(32, int(self.aura_area.height * self.aura_area.height / content_height))
            thumb_y = self.aura_area.y + int((self.aura_area.height - thumb_height) * self.aura_scroll / self.aura_max_scroll)
            self.aura_scroll_track = track
            self.aura_scroll_thumb = pygame.Rect(track.x - 3, thumb_y, 11, thumb_height)
            pygame.draw.rect(screen, theme["popup_border"], track, border_radius=3)
            pygame.draw.rect(screen, theme["accent"], self.aura_scroll_thumb, border_radius=5)
        else:
            self.aura_scroll_track = pygame.Rect(0, 0, 0, 0)
            self.aura_scroll_thumb = pygame.Rect(0, 0, 0, 0)

        if pygame.time.get_ticks() < self.message_until:
            message = self.font.render(self.message, True, theme["success"] if "added" in self.message else (220, 70, 70))
            screen.blit(message, message.get_rect(center=(WIDTH // 2, panel.bottom - 45)))

        self.back_button.bg_color = theme["button"]
        self.back_button.hover_color = theme["button_hover"]
        self.back_button.border_color = theme["grid"]
        self.back_button.text_color = theme["text"]
        self.back_button.draw(screen)
