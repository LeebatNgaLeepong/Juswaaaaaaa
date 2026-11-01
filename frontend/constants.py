"""Frontend constants for Blackjack x Buckshot Roulette.

All sizes, colors, fonts, and timings in one place.
"""

import pygame

# Window
WIDTH = 1280
HEIGHT = 720
TITLE = "Blackjack x Buckshot Roulette"
FPS = 60

# Colors (R, G, B)
FELT_GREEN = (34, 87, 46)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
DARK_RED = (180, 30, 30)
GREEN = (50, 180, 50)
DARK_GREEN = (30, 140, 30)
GOLD = (255, 215, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (200, 200, 200)
BLUE = (50, 100, 220)
CYAN = (0, 200, 200)
ORANGE = (255, 165, 0)

# Card
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_RADIUS = 8
CARD_OVERLAP = 30
CARD_FACE_DOWN_COLOR = (60, 60, 100)
CARD_PATTERN_COLOR = (80, 80, 120)

# Fonts
FONT_NAME = "arial"
FONT_SIZE_SMALL = 18
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 36
FONT_SIZE_TITLE = 64

# Buttons
BUTTON_WIDTH = 160
BUTTON_HEIGHT = 50
BUTTON_RADIUS = 8
BUTTON_COLOR = (70, 70, 100)
BUTTON_HOVER = (100, 100, 140)
BUTTON_DISABLED = (50, 50, 70)
BUTTON_TEXT_COLOR = WHITE

# HP Bar
HP_BAR_WIDTH = 200
HP_BAR_HEIGHT = 30
HP_BAR_RADIUS = 6
HEART_SIZE = 28
HEART_SPACING = 8

# Layout positions (proportional)
DEALER_HAND_Y = 80
DEALER_HP_Y = 30
MESSAGE_Y = HEIGHT // 2 - 60
SHOTGUN_Y = HEIGHT // 2 + 40
PLAYER_HAND_Y = HEIGHT - 180
PLAYER_HP_Y = HEIGHT - 60
BUTTON_Y = HEIGHT - 110

# Timings (milliseconds)
DEALER_REVEAL_DELAY = 800
DEALER_CARD_DELAY = 400
SHOT_FLASH_DURATION = 300
SHOT_SHAKE_DURATION = 300
GAME_OVER_DELAY = 1500
CARD_SLIDE_DURATION = 300

# Shell icons
SHELL_RADIUS = 10
LIVE_SHELL_COLOR = (200, 50, 50)
BLANK_SHELL_COLOR = (150, 150, 150)

# Sound names
SOUND_CARD = "card"
SOUND_CLICK = "click"
SOUND_SHOT_LIVE = "shot_live"
SOUND_SHOT_BLANK = "shot_blank"
SOUND_WIN = "win"
SOUND_LOSE = "lose"

# Assets paths
ASSETS_DIR = "assets"
SOUNDS_DIR = "assets/sounds"
IMAGES_DIR = "assets/images"


def get_font(size: int) -> pygame.font.Font:
    """Get a pygame font with fallback."""
    return pygame.font.SysFont(FONT_NAME, size, bold=(size >= FONT_SIZE_TITLE))