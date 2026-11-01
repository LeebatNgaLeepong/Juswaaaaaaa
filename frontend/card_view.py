"""Card drawing for Blackjack x Buckshot Roulette.

Draws cards face up or face down using pygame primitives.
"""

import pygame
from frontend.constants import (
    CARD_WIDTH, CARD_HEIGHT, CARD_RADIUS, CARD_OVERLAP,
    CARD_FACE_DOWN_COLOR, CARD_PATTERN_COLOR,
    RED, BLACK, WHITE, GOLD,
    get_font, FONT_SIZE_SMALL, FONT_SIZE_MEDIUM
)
from backend.card import Card


# Suit symbols using Unicode (fallback to letters)
SUIT_SYMBOLS = {
    "hearts": "♥",
    "diamonds": "♦",
    "clubs": "♣",
    "spades": "♠",
}

SUIT_LETTERS = {
    "hearts": "H",
    "diamonds": "D",
    "clubs": "C",
    "spades": "S",
}

SUIT_COLORS = {
    "hearts": RED,
    "diamonds": RED,
    "clubs": BLACK,
    "spades": BLACK,
}


def draw_card(
    surface: pygame.Surface,
    card: Card,
    x: int,
    y: int,
    face_up: bool = True,
    font_small: pygame.font.Font | None = None,
    font_medium: pygame.font.Font | None = None
) -> None:
    """Draw a single card.

    Args:
        surface: Surface to draw on
        card: Card to draw
        x: Left position
        y: Top position
        face_up: Whether to show face (True) or back (False)
        font_small: Font for rank/suit in corners
        font_medium: Font for center suit symbol
    """
    font_small = font_small or get_font(FONT_SIZE_SMALL)
    font_medium = font_medium or get_font(FONT_SIZE_MEDIUM)

    card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

    if face_up:
        # White card background
        pygame.draw.rect(surface, WHITE, card_rect, border_radius=CARD_RADIUS)
        pygame.draw.rect(surface, BLACK, card_rect, 2, border_radius=CARD_RADIUS)

        suit = card.suit
        color = SUIT_COLORS[suit]
        symbol = SUIT_SYMBOLS.get(suit, SUIT_LETTERS[suit])

        # Rank in top-left and bottom-right corners
        rank_text = card.rank
        rank_surf = font_small.render(rank_text, True, color)
        surface.blit(rank_surf, (x + 4, y + 2))
        # Bottom-right (rotated 180 would be ideal, but just place it)
        rank_surf2 = font_small.render(rank_text, True, color)
        surface.blit(rank_surf2, (x + CARD_WIDTH - rank_surf2.get_width() - 4, y + CARD_HEIGHT - rank_surf2.get_height() - 2))

        # Suit symbol in center
        suit_surf = font_medium.render(symbol, True, color)
        suit_rect = suit_surf.get_rect(center=card_rect.center)
        surface.blit(suit_surf, suit_rect)

        # Small suit symbols in corners
        suit_small = font_small.render(symbol, True, color)
        surface.blit(suit_small, (x + 4, y + font_small.get_height() + 2))
        surface.blit(suit_small, (x + CARD_WIDTH - suit_small.get_width() - 4, y + CARD_HEIGHT - font_small.get_height() * 2 - 2))

    else:
        # Face down: solid color with pattern
        pygame.draw.rect(surface, CARD_FACE_DOWN_COLOR, card_rect, border_radius=CARD_RADIUS)
        pygame.draw.rect(surface, WHITE, card_rect, 2, border_radius=CARD_RADIUS)

        # Simple diagonal pattern
        for i in range(-CARD_HEIGHT, CARD_WIDTH + CARD_HEIGHT, 20):
            pygame.draw.line(
                surface,
                CARD_PATTERN_COLOR,
                (x + i, y + CARD_HEIGHT),
                (x + i + CARD_HEIGHT, y),
                1
            )


def draw_hand(
    surface: pygame.Surface,
    hand,
    x: int,
    y: int,
    hide_second: bool = False,
    font_small: pygame.font.Font | None = None,
    font_medium: pygame.font.Font | None = None
) -> None:
    """Draw a hand of cards left to right with overlap.

    Args:
        surface: Surface to draw on
        hand: Hand object with .cards list
        x: Left position of first card
        y: Top position
        hide_second: If True, draw second card face down
        font_small: Font for card corners
        font_medium: Font for card center
    """
    for i, card in enumerate(hand.cards):
        card_x = x + i * CARD_OVERLAP
        face_up = not (hide_second and i == 1)
        draw_card(surface, card, card_x, y, face_up, font_small, font_medium)


def draw_hand_value(surface: pygame.Surface, hand, x: int, y: int, font: pygame.font.Font, hide_value: bool = False) -> None:
    """Draw the hand value next to the hand."""
    if hide_value:
        text = "Value: ??"
    else:
        text = f"Value: {hand.value()}"
    draw_text(surface, text, x, y, font, WHITE)


# Re-export draw_text from ui for convenience
from frontend.ui import draw_text