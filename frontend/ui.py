"""UI components for Blackjack x Buckshot Roulette.

Button class, HP bar drawing, and text helpers.
"""

import pygame
from frontend.constants import (
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_RADIUS,
    BUTTON_COLOR, BUTTON_HOVER, BUTTON_DISABLED, BUTTON_TEXT_COLOR,
    HP_BAR_WIDTH, HP_BAR_HEIGHT, HP_BAR_RADIUS,
    HEART_SIZE, HEART_SPACING, RED, GREEN, WHITE, GRAY,
    get_font, FONT_SIZE_MEDIUM
)


class Button:
    """A clickable button with hover and disabled states."""

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        width: int = BUTTON_WIDTH,
        height: int = BUTTON_HEIGHT,
        font: pygame.font.Font | None = None
    ) -> None:
        """Initialize a button.

        Args:
            x: Left position
            y: Top position
            text: Button label
            width: Button width
            height: Button height
            font: Font to use for text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.enabled = True
        self.hovered = False
        self.font = font or get_font(FONT_SIZE_MEDIUM)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button on the surface."""
        # Choose color based on state
        if not self.enabled:
            color = BUTTON_DISABLED
        elif self.hovered:
            color = BUTTON_HOVER
        else:
            color = BUTTON_COLOR

        # Draw rounded rectangle
        pygame.draw.rect(surface, color, self.rect, border_radius=BUTTON_RADIUS)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=BUTTON_RADIUS)

        # Draw centered text
        text_surf = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """Update hover state based on mouse position."""
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle a pygame event.

        Returns:
            True if the button was clicked (left mouse released over enabled button)
        """
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def draw_hp_bar(surface: pygame.Surface, name: str, hp: int, max_hp: int, x: int, y: int, font: pygame.font.Font) -> None:
    """Draw HP as heart icons.

    Args:
        surface: Surface to draw on
        name: Label (e.g., "Player")
        hp: Current HP
        max_hp: Maximum HP
        x: Left position
        y: Top position
        font: Font for name label
    """
    # Draw name
    name_surf = font.render(name, True, WHITE)
    surface.blit(name_surf, (x, y))

    heart_y = y + font.get_height() + 4

    for i in range(max_hp):
        heart_x = x + i * (HEART_SIZE + HEART_SPACING)
        heart_rect = pygame.Rect(heart_x, heart_y, HEART_SIZE, HEART_SIZE)

        if i < hp:
            # Filled heart (red)
            pygame.draw.rect(surface, RED, heart_rect, border_radius=4)
        else:
            # Empty heart (gray outline)
            pygame.draw.rect(surface, GRAY, heart_rect, 2, border_radius=4)


def draw_text_centered(surface: pygame.Surface, text: str, x: int, y: int, font: pygame.font.Font, color: tuple[int, int, int] = WHITE) -> None:
    """Draw text centered at (x, y)."""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)


def draw_text(surface: pygame.Surface, text: str, x: int, y: int, font: pygame.font.Font, color: tuple[int, int, int] = WHITE) -> None:
    """Draw text at (x, y)."""
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (x, y))