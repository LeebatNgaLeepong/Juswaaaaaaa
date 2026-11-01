"""Screen drawing functions for Blackjack x Buckshot Roulette.

One draw function per Game state.
"""

import pygame
from frontend.constants import (
    WIDTH, HEIGHT, FELT_GREEN, WHITE, GOLD, RED, GREEN,
    DEALER_HAND_Y, DEALER_HP_Y, MESSAGE_Y, SHOTGUN_Y,
    PLAYER_HAND_Y, PLAYER_HP_Y, BUTTON_Y,
    get_font, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE, FONT_SIZE_TITLE
)
from frontend.ui import draw_hp_bar, draw_text_centered, draw_text
from frontend.card_view import draw_hand, draw_hand_value
from frontend.shotgun_view import ShotgunView
from backend.game import Game, GameState


# Fonts
font_medium = get_font(FONT_SIZE_MEDIUM)
font_large = get_font(FONT_SIZE_LARGE)
font_title = get_font(FONT_SIZE_TITLE)


def draw_title_screen(surface: pygame.Surface, buttons: list) -> None:
    """Draw the title/menu screen."""
    surface.fill(FELT_GREEN)

    # Title
    draw_text_centered(surface, "Blackjack x Buckshot Roulette", WIDTH // 2, HEIGHT // 3, font_title, GOLD)

    # Rules summary
    rules = [
        "Play Blackjack against the Dealer",
        "Loser pulls the trigger on a shotgun",
        "Live shell = 1 damage (2 if bust)",
        "First to 0 HP loses"
    ]
    for i, line in enumerate(rules):
        draw_text_centered(surface, line, WIDTH // 2, HEIGHT // 2 + i * 30, font_medium, WHITE)

    # Draw buttons
    for btn in buttons:
        btn.draw(surface)


def draw_player_turn(surface: pygame.Surface, game: Game, buttons: list, reveal_dealer: bool) -> None:
    """Draw the PLAYER_TURN screen."""
    surface.fill(FELT_GREEN)

    # Dealer area (top)
    draw_hp_bar(surface, "Dealer", game.dealer.hp, 3, 50, DEALER_HP_Y, font_medium)
    draw_hand(surface, game.dealer.hand, WIDTH // 2 - 100, DEALER_HAND_Y, hide_second=not reveal_dealer)
    if reveal_dealer:
        draw_hand_value(surface, game.dealer.hand, WIDTH // 2 + 120, DEALER_HAND_Y + 40, font_medium)
    else:
        draw_text(surface, "Value: ??", WIDTH // 2 + 120, DEALER_HAND_Y + 40, font_medium, WHITE)

    # Message
    draw_text_centered(surface, "Your turn. Hit or Stand?", WIDTH // 2, MESSAGE_Y, font_large, GOLD)

    # Shotgun panel
    live, blank = game.shotgun.shells_left()
    ShotgunView().draw_shell_counts(surface, live, blank, WIDTH // 2 - 150, SHOTGUN_Y)

    # Player area (bottom)
    draw_hp_bar(surface, "Player", game.player.hp, 3, 50, PLAYER_HP_Y, font_medium)
    draw_hand(surface, game.player.hand, WIDTH // 2 - 100, PLAYER_HAND_Y, hide_second=False)
    draw_hand_value(surface, game.player.hand, WIDTH // 2 + 120, PLAYER_HAND_Y + 40, font_medium)

    # Draw buttons
    for btn in buttons:
        btn.draw(surface)


def draw_dealer_turn(surface: pygame.Surface, game: Game, buttons: list, reveal_dealer: bool) -> None:
    """Draw the DEALER_TURN screen (brief reveal delay)."""
    # Same as player turn but with reveal_dealer=True and buttons disabled
    draw_player_turn(surface, game, buttons, reveal_dealer=True)

    # Overlay message
    draw_text_centered(surface, "Dealer reveals...", WIDTH // 2, MESSAGE_Y, font_large, GOLD)


def draw_round_result(surface: pygame.Surface, game: Game, buttons: list) -> None:
    """Draw the ROUND_RESULT screen."""
    surface.fill(FELT_GREEN)

    # Dealer area (revealed)
    draw_hp_bar(surface, "Dealer", game.dealer.hp, 3, 50, DEALER_HP_Y, font_medium)
    draw_hand(surface, game.dealer.hand, WIDTH // 2 - 100, DEALER_HAND_Y, hide_second=False)
    draw_hand_value(surface, game.dealer.hand, WIDTH // 2 + 120, DEALER_HAND_Y + 40, font_medium)

    # Message based on round_result (WINNER)
    if game.round_result == "player":
        msg = "You win the round! The dealer pulls the trigger."
        color = GREEN
    elif game.round_result == "dealer":
        msg = "Dealer wins the round! You pull the trigger."
        color = RED
    else:  # push
        msg = "Push! Nobody pulls the trigger."
        color = GOLD

    draw_text_centered(surface, msg, WIDTH // 2, MESSAGE_Y, font_large, color)

    # Show BUST/BLACKJACK labels
    if game.player.hand.is_bust():
        draw_text(surface, "BUST!", WIDTH // 2 - 100, DEALER_HAND_Y - 30, font_large, RED)
    elif game.player.hand.is_blackjack():
        draw_text(surface, "BLACKJACK!", WIDTH // 2 - 100, DEALER_HAND_Y - 30, font_large, GOLD)

    if game.dealer.hand.is_bust():
        draw_text(surface, "BUST!", WIDTH // 2 - 100, PLAYER_HAND_Y - 30, font_large, RED)
    elif game.dealer.hand.is_blackjack():
        draw_text(surface, "BLACKJACK!", WIDTH // 2 - 100, PLAYER_HAND_Y - 30, font_large, GOLD)

    # Shotgun panel
    live, blank = game.shotgun.shells_left()
    ShotgunView().draw_shell_counts(surface, live, blank, WIDTH // 2 - 150, SHOTGUN_Y)

    # Player area
    draw_hp_bar(surface, "Player", game.player.hp, 3, 50, PLAYER_HP_Y, font_medium)
    draw_hand(surface, game.player.hand, WIDTH // 2 - 100, PLAYER_HAND_Y, hide_second=False)
    draw_hand_value(surface, game.player.hand, WIDTH // 2 + 120, PLAYER_HAND_Y + 40, font_medium)

    # Draw buttons
    for btn in buttons:
        btn.draw(surface)


def draw_trigger_pull(surface: pygame.Surface, game: Game, buttons: list, shotgun_view: ShotgunView) -> None:
    """Draw the TRIGGER_PULL screen with shot animation."""
    # Draw the round result background (hands, HP, etc.)
    draw_round_result(surface, game, buttons)

    # Draw shot animation on top
    shotgun_view.draw_shot_result(surface, WIDTH // 2, MESSAGE_Y)


def draw_game_over(surface: pygame.Surface, game: Game, buttons: list) -> None:
    """Draw the GAME_OVER screen."""
    surface.fill(FELT_GREEN)

    winner = game.get_winner()
    if winner == "player":
        msg = "YOU WIN!"
        color = GREEN
    else:
        msg = "YOU DIED"
        color = RED

    draw_text_centered(surface, msg, WIDTH // 2, HEIGHT // 3, font_title, color)
    draw_text_centered(surface, f"Final HP - You: {game.player.hp}  Dealer: {game.dealer.hp}", WIDTH // 2, HEIGHT // 2, font_large, WHITE)

    # Draw buttons
    for btn in buttons:
        btn.draw(surface)