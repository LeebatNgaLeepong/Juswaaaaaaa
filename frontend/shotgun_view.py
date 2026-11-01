"""Shotgun view for Blackjack x Buckshot Roulette.

Draws shell counts and shot animation.
"""

import pygame
from frontend.constants import (
    SHELL_RADIUS, LIVE_SHELL_COLOR, BLANK_SHELL_COLOR,
    WHITE, RED, GRAY, GOLD,
    get_font, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE,
    SHOT_FLASH_DURATION, SHOT_SHAKE_DURATION
)


class ShotgunView:
    """Draws shotgun shell counts and shot result feedback."""

    def __init__(self) -> None:
        """Initialize the shotgun view."""
        self.font = get_font(FONT_SIZE_MEDIUM)
        self.big_font = get_font(FONT_SIZE_LARGE)

        # Shot animation state
        self.shot_timer = 0
        self.shot_live = False
        self.shot_target_name = ""
        self.shot_damage = 0
        self.flash_timer = 0
        self.shake_timer = 0

    def trigger_shot(self, is_live: bool, target_name: str, damage: int) -> None:
        """Start the shot animation.

        Args:
            is_live: Whether the shell was live
            target_name: Name of who was shot
            damage: Damage dealt
        """
        self.shot_live = is_live
        self.shot_target_name = target_name
        self.shot_damage = damage
        self.shot_timer = pygame.time.get_ticks()
        self.flash_timer = pygame.time.get_ticks()
        self.shake_timer = pygame.time.get_ticks()

    def update(self) -> None:
        """Update animation timers."""
        now = pygame.time.get_ticks()
        # Timers auto-expire when checked in draw

    def get_shake_offset(self) -> tuple[int, int]:
        """Get screen shake offset if active."""
        if self.shake_timer > 0:
            elapsed = pygame.time.get_ticks() - self.shake_timer
            if elapsed < SHOT_SHAKE_DURATION:
                import random
                return (random.randint(-4, 4), random.randint(-4, 4))
            else:
                self.shake_timer = 0
        return (0, 0)

    def draw_shell_counts(self, surface: pygame.Surface, live: int, blank: int, x: int, y: int) -> None:
        """Draw the remaining shell counts with icons."""
        # Label
        label = self.font.render("Shotgun:", True, WHITE)
        surface.blit(label, (x, y))

        # Live shells
        live_x = x + label.get_width() + 20
        for i in range(live):
            cx = live_x + i * (SHELL_RADIUS * 2 + 4)
            cy = y + SHELL_RADIUS
            pygame.draw.circle(surface, LIVE_SHELL_COLOR, (cx, cy), SHELL_RADIUS)
            pygame.draw.circle(surface, WHITE, (cx, cy), SHELL_RADIUS, 2)

        live_text = self.font.render(f"Live: {live}", True, RED)
        surface.blit(live_text, (live_x + live * (SHELL_RADIUS * 2 + 4) + 10, y))

        # Blank shells
        blank_x = live_x + live_text.get_width() + 40
        for i in range(blank):
            cx = blank_x + i * (SHELL_RADIUS * 2 + 4)
            cy = y + SHELL_RADIUS
            pygame.draw.circle(surface, BLANK_SHELL_COLOR, (cx, cy), SHELL_RADIUS)
            pygame.draw.circle(surface, WHITE, (cx, cy), SHELL_RADIUS, 2)

        blank_text = self.font.render(f"Blank: {blank}", True, GRAY)
        surface.blit(blank_text, (blank_x + blank * (SHELL_RADIUS * 2 + 4) + 10, y))

    def draw_shot_result(self, surface: pygame.Surface, x: int, y: int) -> bool:
        """Draw the shot result animation.

        Returns:
            True if animation is still playing
        """
        if self.shot_timer == 0:
            return False

        now = pygame.time.get_ticks()
        elapsed = now - self.shot_timer

        if elapsed > SHOT_FLASH_DURATION:
            self.shot_timer = 0
            return False

        # Flash background
        flash_elapsed = now - self.flash_timer
        if flash_elapsed < SHOT_FLASH_DURATION:
            alpha = int(255 * (1 - flash_elapsed / SHOT_FLASH_DURATION))
            if self.shot_live:
                flash_surf = pygame.Surface((surface.get_width(), surface.get_height()))
                flash_surf.fill(RED)
                flash_surf.set_alpha(alpha // 3)
                surface.blit(flash_surf, (0, 0))

        # Text
        if self.shot_live:
            text = f"BANG! {self.shot_target_name} takes {self.shot_damage} damage!"
            color = RED
        else:
            text = f"Click... blank. {self.shot_target_name} survives."
            color = GRAY

        text_surf = self.big_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        surface.blit(text_surf, text_rect)

        return True

    def draw(self, surface: pygame.Surface, game, x: int, y: int) -> None:
        """Draw shell counts and shot result if active.

        Args:
            surface: Surface to draw on
            game: Game object
            x: X position for shell counts
            y: Y position for shell counts
        """
        live, blank = game.shotgun.shells_left()
        self.draw_shell_counts(surface, live, blank, x, y)

        # Draw shot result if in TRIGGER_PULL state
        if game.state.name == "TRIGGER_PULL":
            self.draw_shot_result(surface, surface.get_width() // 2, y - 60)