import pygame

from button import Button
from constants import HEIGHT, WIDTH, PORTRAIT_MODE


class AchievementsMenu:
    ACHIEVEMENTS = (
        ("first_win", "FIRST SPELL", "Win your first Sudoku puzzle.", 50),
        ("perfect_win", "PERFECT FOCUS", "Win a puzzle with no mistakes.", 75),
        ("score_10000", "HIGH SCORER", "Win a game with 10,000+ points.", 100),
        ("streak_3", "ON FIRE", "Reach a 3-game win streak.", 100),
        ("all_modes", "TRUE WIZARD", "Win an Easy, Medium, and Hard game.", 150),
        ("streak_5", "UNSTOPPABLE", "Reach a 5-game win streak.", 175),
        ("hintless_win", "CLEAR MIND", "Win without using a Hint Token.", 100),
        ("speed_demon", "SPEED DEMON", "Win a puzzle in under 5 minutes.", 125),
        ("hard_hero", "HARD HERO", "Win a Hard puzzle.", 125),
        ("coin_collector", "COIN COLLECTOR", "Earn 500 Coins.", 150),
        ("easy_graduate", "EASY GRADUATE", "Win an Easy puzzle.", 25),
        ("medium_conqueror", "MEDIUM CONQUEROR", "Win a Medium puzzle.", 45),
        ("easy_trio", "GENTLE HAT-TRICK", "Win 3 Easy puzzles.", 60),
        ("medium_trio", "STEADY SPELLCASTER", "Win 3 Medium puzzles.", 90),
        ("hard_trio", "HARD HAT-TRICK", "Win 3 Hard puzzles.", 150),
        ("wins_10", "TENFOLD", "Win 10 puzzles in total.", 125),
        ("wins_25", "PUZZLE VETERAN", "Win 25 puzzles in total.", 250),
        ("matches_10", "DEDICATED PLAYER", "Complete 10 matches.", 75),
        ("matches_50", "SUDOKU REGULAR", "Complete 50 matches.", 200),
        ("streak_10", "BLAZING TRAIL", "Reach a 10-game win streak.", 300),
        ("score_20000", "ARCANE SCORE", "Score 20,000 points in one win.", 175),
        ("score_30000", "LEGENDARY SCORE", "Score 30,000 points in one win.", 300),
        ("lightning_easy", "LIGHTNING LEARNER", "Win Easy in under 2 minutes.", 100),
        ("rapid_medium", "RAPID RUNE", "Win Medium in under 4 minutes.", 150),
        ("flawless_hard", "IRON FOCUS", "Win Hard with no mistakes.", 225),
        ("number_scribe", "NUMBER SCRIBE", "Enter 100 numbers in total.", 75),
        ("number_legend", "NUMBER LEGEND", "Enter 500 numbers in total.", 200),
        ("hint_vault", "HINT VAULT", "Use 20 hints across your games.", 80),
        ("coin_tycoon", "COIN TYCOON", "Earn 1,000 Coins.", 300),
        ("all_modes_three", "TRIPLE CROWN", "Win 3 games in every mode.", 350),
        ("score_i", "HIGH SCORER I", "Score 5,000 points in one win.", 50),
        ("score_ii", "HIGH SCORER II", "Score 15,000 points in one win.", 150),
        ("score_iii", "HIGH SCORER III", "Score 30,000 points in one win.", 300),
        ("streak_i", "ON FIRE I", "Reach a 2-game win streak.", 50),
        ("streak_ii", "ON FIRE II", "Reach a 5-game win streak.", 175),
        ("streak_iii", "ON FIRE III", "Reach a 10-game win streak.", 300),
        ("coins_i", "COIN COLLECTOR I", "Earn 100 Coins.", 50),
        ("coins_ii", "COIN COLLECTOR II", "Earn 500 Coins.", 150),
        ("coins_iii", "COIN COLLECTOR III", "Earn 1,000 Coins.", 300),
        ("wins_i", "PUZZLE WINNER I", "Win 3 puzzles in total.", 50),
        ("wins_ii", "PUZZLE WINNER II", "Win 10 puzzles in total.", 125),
        ("wins_iii", "PUZZLE WINNER III", "Win 25 puzzles in total.", 250),
        ("wins_50", "MASTER SOLVER", "Win 50 puzzles in total.", 400),
        ("wins_75", "RUNE VETERAN", "Win 75 puzzles in total.", 550),
        ("wins_100", "CENTURY OF WINS", "Win 100 puzzles in total.", 750),
        ("wins_150", "ARCANE CHAMPION", "Win 150 puzzles in total.", 1000),
        ("wins_250", "SUDOKU IMMORTAL", "Win 250 puzzles in total.", 1500),
        ("matches_100", "LOYAL APPRENTICE", "Complete 100 matches.", 350),
        ("matches_200", "DEVOTED WIZARD", "Complete 200 matches.", 650),
        ("matches_500", "ENDLESS JOURNEY", "Complete 500 matches.", 1250),
        ("numbers_1000", "THOUSAND GLYPHS", "Enter 1,000 numbers in total.", 250),
        ("numbers_2500", "RUNE WRITER", "Enter 2,500 numbers in total.", 450),
        ("numbers_5000", "NUMBER ARCHIVIST", "Enter 5,000 numbers in total.", 750),
        ("numbers_10000", "TEN THOUSAND RUNES", "Enter 10,000 numbers in total.", 1250),
        ("hints_50", "GUIDED PATH I", "Use 50 hints across your games.", 125),
        ("hints_100", "GUIDED PATH II", "Use 100 hints across your games.", 225),
        ("hints_250", "GUIDED PATH III", "Use 250 hints across your games.", 450),
        ("hints_500", "ORACLE'S ALLY", "Use 500 hints across your games.", 750),
        ("streak_15", "WHITE HOT", "Reach a 15-game win streak.", 450),
        ("streak_20", "INFERNO", "Reach a 20-game win streak.", 600),
        ("streak_30", "ETERNAL FLAME", "Reach a 30-game win streak.", 900),
        ("streak_50", "UNBROKEN LEGEND", "Reach a 50-game win streak.", 1500),
        ("coins_2500", "HEAVY PURSE", "Hold 2,500 Coins at once.", 400),
        ("coins_5000", "TREASURE CHEST", "Hold 5,000 Coins at once.", 650),
        ("coins_10000", "DRAGON'S HOARD", "Hold 10,000 Coins at once.", 1000),
        ("coins_25000", "GOLDEN KINGDOM", "Hold 25,000 Coins at once.", 2000),
        ("easy_wins_10", "EASY ADEPT", "Win 10 Easy puzzles.", 150),
        ("easy_wins_25", "EASY EXPERT", "Win 25 Easy puzzles.", 300),
        ("easy_wins_50", "EASY MASTER", "Win 50 Easy puzzles.", 550),
        ("medium_wins_10", "MEDIUM ADEPT", "Win 10 Medium puzzles.", 225),
        ("medium_wins_25", "MEDIUM EXPERT", "Win 25 Medium puzzles.", 425),
        ("medium_wins_50", "MEDIUM MASTER", "Win 50 Medium puzzles.", 750),
        ("hard_wins_10", "HARD ADEPT", "Win 10 Hard puzzles.", 350),
        ("hard_wins_25", "HARD EXPERT", "Win 25 Hard puzzles.", 650),
        ("hard_wins_50", "HARD MASTER", "Win 50 Hard puzzles.", 1100),
        ("total_score_100k", "SCORE SAGE I", "Earn 100,000 lifetime points.", 200),
        ("total_score_250k", "SCORE SAGE II", "Earn 250,000 lifetime points.", 400),
        ("total_score_500k", "SCORE SAGE III", "Earn 500,000 lifetime points.", 700),
        ("total_score_1m", "MILLION-POINT MAGE", "Earn 1,000,000 lifetime points.", 1250),
        ("mistakes_100", "LESSON LEARNER I", "Make 100 lifetime mistakes.", 100),
        ("mistakes_250", "LESSON LEARNER II", "Make 250 lifetime mistakes.", 225),
        ("mistakes_500", "LESSON LEARNER III", "Make 500 lifetime mistakes.", 450),
        ("losses_10", "RISE AGAIN I", "Finish 10 games without a win.", 100),
        ("losses_25", "RISE AGAIN II", "Finish 25 games without a win.", 225),
        ("losses_50", "RISE AGAIN III", "Finish 50 games without a win.", 400),
        ("perfect_easy", "PURE BEGINNING", "Win Easy with no mistakes.", 75),
        ("perfect_medium", "PURE DISCIPLINE", "Win Medium with no mistakes.", 125),
        ("hintless_easy", "SOLO APPRENTICE", "Win Easy without using a hint.", 75),
        ("hintless_medium", "SOLO SPELLCASTER", "Win Medium without using a hint.", 125),
        ("hintless_hard", "SOLO ARCHMAGE", "Win Hard without using a hint.", 200),
        ("swift_hard", "HARD AND SWIFT", "Win Hard in under 10 minutes.", 250),
        ("score_40000", "MYTHIC SCORE", "Score 40,000 points in one win.", 500),
    )

    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 40 if PORTRAIT_MODE else 48)
        self.heading_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 20 if PORTRAIT_MODE else 23)
        self.body_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 16 if PORTRAIT_MODE else 18)
        self.score_icon = pygame.transform.smoothscale(
            pygame.image.load("assets/images/score.png").convert_alpha(), (48, 48)
        )
        self.back_button = Button(WIDTH // 2 - 110, HEIGHT - (350 if PORTRAIT_MODE else 180), 220, 55, "BACK")
        self.scroll_offset = 0
        self.max_scroll = 0
        self.dragging = False
        self.last_drag_y = 0
        self.list_area = pygame.Rect(0, 0, 0, 0)
        self.scroll_track = pygame.Rect(0, 0, 0, 0)
        self.scroll_thumb = pygame.Rect(0, 0, 0, 0)
        self.dragging_scrollbar = False
        self.thumb_grab_offset = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y * 48))
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.back_button.clicked(event.pos):
                self.game.play_sound(self.game.click_sound)
                self.game.achievements_open = False
                return
            if event.button == 1 and self.scroll_thumb.collidepoint(event.pos):
                self.dragging_scrollbar = True
                self.thumb_grab_offset = event.pos[1] - self.scroll_thumb.y
                return
            if event.button == 1 and self.scroll_track.collidepoint(event.pos):
                usable_height = max(1, self.scroll_track.height - self.scroll_thumb.height)
                ratio = max(0.0, min(1.0, (event.pos[1] - self.scroll_track.y - self.scroll_thumb.height // 2) / usable_height))
                self.scroll_offset = int(ratio * self.max_scroll)
                return
            if event.button == 4:
                self.scroll_offset = max(0, self.scroll_offset - 48)
            elif event.button == 5:
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 48)
            elif event.button == 1 and self.list_area.collidepoint(event.pos):
                self.dragging = True
                self.last_drag_y = event.pos[1]
            return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            self.dragging_scrollbar = False
        elif event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
            usable_height = max(1, self.scroll_track.height - self.scroll_thumb.height)
            ratio = max(0.0, min(1.0, (event.pos[1] - self.scroll_track.y - self.thumb_grab_offset) / usable_height))
            self.scroll_offset = int(ratio * self.max_scroll)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset + self.last_drag_y - event.pos[1]))
            self.last_drag_y = event.pos[1]

    def draw(self):
        screen, theme = self.game.screen, self.game.theme
        screen.fill(theme["background"])
        panel = pygame.Rect(WIDTH // 2 - min(WIDTH - 50, 780) // 2, 55, min(WIDTH - 50, 780), HEIGHT - (285 if PORTRAIT_MODE else 175))
        pygame.draw.rect(screen, theme["shadow"], panel.move(0, 8), border_radius=28)
        pygame.draw.rect(screen, theme["popup"], panel, border_radius=28)
        pygame.draw.rect(screen, theme["popup_border"], panel, 2, border_radius=28)

        title = self.title_font.render("ACHIEVEMENTS", True, theme["text"])
        screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.y + 55)))
        unlocked = self.game.stats.data.get("achievements", {})
        ordered_achievements = sorted(
            self.ACHIEVEMENTS,
            key=lambda achievement: not unlocked.get(achievement[0], False),
        )
        card_height = 92
        card_gap = 10
        # One focused column works on both desktop and phone; scroll to see
        # the rest instead of squeezing achievements beside one another.
        card_width = panel.width - 56
        list_area = pygame.Rect(panel.x + 16, panel.y + 118, panel.width - 32, panel.height - 215)
        self.list_area = list_area
        total_height = len(ordered_achievements) * (card_height + card_gap) - card_gap
        self.max_scroll = max(0, total_height - list_area.height)
        self.scroll_offset = min(self.scroll_offset, self.max_scroll)
        previous_clip = screen.get_clip()
        screen.set_clip(list_area)
        for index, (achievement_id, title, description, reward) in enumerate(ordered_achievements):
            card = pygame.Rect(
                panel.x + 28,
                list_area.y + index * (card_height + card_gap) - self.scroll_offset,
                card_width,
                card_height,
            )
            earned = unlocked.get(achievement_id, False)
            pygame.draw.rect(screen, theme["button"], card, border_radius=16)
            pygame.draw.rect(screen, theme["accent"] if earned else theme["popup_border"], card, 2, border_radius=16)
            medal_center = (card.x + 44, card.centery)
            score_icon = self.score_icon.copy()
            if not earned:
                score_icon.set_alpha(90)
            screen.blit(score_icon, score_icon.get_rect(center=medal_center))
            heading = self.heading_font.render(title, True, theme["text"])
            detail_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 15 if PORTRAIT_MODE else 14)
            detail = detail_font.render(description, True, theme["secondary"])
            reward_text = self.body_font.render(f"{reward} COINS", True, (245, 190, 35) if earned else theme["secondary"])
            screen.blit(heading, (card.x + 82, card.y + 18))
            screen.blit(detail, (card.x + 82, card.y + 49))
            screen.blit(reward_text, reward_text.get_rect(midright=(card.right - 14, card.bottom - 18)))
        screen.set_clip(previous_clip)

        if self.max_scroll:
            track = pygame.Rect(panel.right - 18, list_area.y, 5, list_area.height)
            thumb_height = max(36, int(list_area.height * list_area.height / total_height))
            thumb_y = list_area.y + int((list_area.height - thumb_height) * self.scroll_offset / self.max_scroll)
            self.scroll_track = track
            self.scroll_thumb = pygame.Rect(track.x - 3, thumb_y, track.width + 6, thumb_height)
            pygame.draw.rect(screen, theme["popup_border"], track, border_radius=3)
            pygame.draw.rect(screen, theme["accent"], self.scroll_thumb, border_radius=4)
        else:
            self.scroll_track = pygame.Rect(0, 0, 0, 0)
            self.scroll_thumb = pygame.Rect(0, 0, 0, 0)

        self.back_button.bg_color = theme["button"]
        self.back_button.hover_color = theme["button_hover"]
        self.back_button.border_color = theme["grid"]
        self.back_button.text_color = theme["text"]
        self.back_button.draw(screen)
