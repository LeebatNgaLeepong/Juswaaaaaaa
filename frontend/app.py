"""Main App class for Blackjack x Buckshot Roulette.

Handles the main loop, event handling, state management, and rendering.
"""

import pygame
from frontend.constants import (
    WIDTH, HEIGHT, TITLE, FPS, FELT_GREEN,
    BUTTON_WIDTH, BUTTON_HEIGHT,
    DEALER_REVEAL_DELAY,
    get_font, FONT_SIZE_MEDIUM
)
from frontend.ui import Button
from frontend.sound import SoundManager
from frontend.shotgun_view import ShotgunView
from frontend.screens import (
    draw_title_screen, draw_player_turn, draw_dealer_turn,
    draw_round_result, draw_trigger_pull, draw_game_over
)
from backend.game import Game, GameState


class App:
    """Main application class."""

    def __init__(self) -> None:
        """Initialize the application."""
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font = get_font(FONT_SIZE_MEDIUM)

        # Backend game
        self.game = Game()

        # Sound
        self.sound = SoundManager()

        # Shotgun view (for animation state)
        self.shotgun_view = ShotgunView()

        # UI state
        self.reveal_dealer = False
        self.dealer_reveal_timer = 0
        self.shot_played = False  # Prevent multiple sound plays per state
        self.game_over_shown = False
        self.game_over_timer = 0

        # Buttons (created dynamically per state)
        self.buttons: list[Button] = []

        # Start at title screen
        self.screen_state = "TITLE"
        self.create_title_buttons()

    def create_title_buttons(self) -> None:
        """Create buttons for the title screen."""
        self.buttons = [
            Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 80, "Play"),
            Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 150, "Quit"),
        ]

    def create_player_turn_buttons(self) -> None:
        """Create Hit and Stand buttons."""
        self.buttons = [
            Button(WIDTH // 2 - BUTTON_WIDTH - 20, BUTTON_Y, "Hit"),
            Button(WIDTH // 2 + 20, BUTTON_Y, "Stand"),
        ]

    def create_round_result_buttons(self) -> None:
        """Create Pull Trigger or Next Round button."""
        if self.game.round_result == "push":
            self.buttons = [
                Button(WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y, "Next Round"),
            ]
        else:
            self.buttons = [
                Button(WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y, "Pull Trigger"),
            ]

    def create_trigger_pull_buttons(self) -> None:
        """Create Next Round button."""
        self.buttons = [
            Button(WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_Y, "Next Round"),
        ]

    def create_game_over_buttons(self) -> None:
        """Create Play Again and Quit buttons."""
        self.buttons = [
            Button(WIDTH // 2 - BUTTON_WIDTH - 20, BUTTON_Y, "Play Again"),
            Button(WIDTH // 2 + 20, BUTTON_Y, "Quit"),
        ]

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def handle_events(self) -> None:
        """Process pygame events."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Update button hover
            for btn in self.buttons:
                btn.update(mouse_pos)

            # Handle button clicks
            for btn in self.buttons:
                if btn.handle_event(event):
                    self.on_button_click(btn.text)
                    self.sound.play("click")

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                self.handle_key(event.key)

    def handle_key(self, key: int) -> None:
        """Handle keyboard input."""
        if self.screen_state == "TITLE":
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                self.start_new_match()
            elif key == pygame.K_ESCAPE:
                self.running = False

        elif self.screen_state == "PLAYER_TURN":
            if key == pygame.K_h:
                self.on_hit()
            elif key == pygame.K_s:
                self.on_stand()

        elif self.screen_state == "ROUND_RESULT":
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                if self.game.round_result == "push":
                    self.on_next_round()
                else:
                    self.on_pull_trigger()

        elif self.screen_state == "TRIGGER_PULL":
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                self.on_next_round()

        elif self.screen_state == "GAME_OVER":
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                self.start_new_match()
            elif key == pygame.K_ESCAPE:
                self.screen_state = "TITLE"
                self.create_title_buttons()

    def on_button_click(self, text: str) -> None:
        """Handle button clicks by text label."""
        if text == "Play":
            self.start_new_match()
        elif text == "Quit":
            self.running = False
        elif text == "Hit":
            self.on_hit()
        elif text == "Stand":
            self.on_stand()
        elif text == "Pull Trigger":
            self.on_pull_trigger()
        elif text == "Next Round":
            self.on_next_round()
        elif text == "Play Again":
            self.start_new_match()

    def on_hit(self) -> None:
        """Handle Hit button."""
        if self.screen_state == "PLAYER_TURN":
            self.game.player_hit()
            self.sound.play("card")

            # Check if player busted (backend moves to ROUND_RESULT)
            if self.game.state == GameState.ROUND_RESULT:
                self.transition_to_round_result()

    def on_stand(self) -> None:
        """Handle Stand button."""
        if self.screen_state == "PLAYER_TURN":
            self.game.player_stand()
            self.sound.play("card")

            # Backend runs dealer instantly and goes to ROUND_RESULT
            self.transition_to_round_result()

    def on_pull_trigger(self) -> None:
        """Handle Pull Trigger button."""
        if self.screen_state == "ROUND_RESULT" and self.game.round_result != "push":
            self.game.pull_trigger()
            self.shot_played = False
            self.screen_state = "TRIGGER_PULL"
            self.create_trigger_pull_buttons()

    def on_next_round(self) -> None:
        """Handle Next Round button."""
        if self.screen_state == "ROUND_RESULT" and self.game.round_result == "push":
            self.game.next_round()
            self.reveal_dealer = False
            self.screen_state = "PLAYER_TURN"
            self.create_player_turn_buttons()
        elif self.screen_state == "TRIGGER_PULL":
            self.game.next_round()
            self.reveal_dealer = False
            self.screen_state = "PLAYER_TURN"
            self.create_player_turn_buttons()

    def transition_to_round_result(self) -> None:
        """Transition to ROUND_RESULT screen with dealer reveal delay."""
        self.screen_state = "ROUND_RESULT"
        self.reveal_dealer = True
        self.dealer_reveal_timer = pygame.time.get_ticks() + DEALER_REVEAL_DELAY
        self.create_round_result_buttons()

    def start_new_match(self) -> None:
        """Start a new match."""
        self.game.start_match()
        self.game.start_round()
        self.reveal_dealer = False
        self.shot_played = False
        self.game_over_shown = False
        self.screen_state = "PLAYER_TURN"
        self.create_player_turn_buttons()
        # Play initial card sounds for the deal (2 cards each)
        self.sound.play("card")
        self.sound.play("card")

    def update(self) -> None:
        """Update timers and state transitions."""
        now = pygame.time.get_ticks()

        # Dealer reveal delay in ROUND_RESULT
        if self.screen_state == "ROUND_RESULT" and self.dealer_reveal_timer > 0:
            if now >= self.dealer_reveal_timer:
                self.dealer_reveal_timer = 0
                # Buttons are already created, they just become enabled

        # Shot animation in TRIGGER_PULL
        if self.screen_state == "TRIGGER_PULL":
            if not self.shot_played:
                self.shot_played = True
                # Trigger shot animation and sound
                if self.game.last_shot_result is not None:
                    target = self.game.last_target
                    if target:
                        damage = 2 if target.hand.is_bust() else 1
                        self.shotgun_view.trigger_shot(
                            self.game.last_shot_result,
                            target.name,
                            damage
                        )
                        if self.game.last_shot_result:
                            self.sound.play("shot_live")
                        else:
                            self.sound.play("shot_blank")

        # Game over delay
        if self.screen_state == "GAME_OVER" and not self.game_over_shown:
            self.game_over_shown = True
            self.game_over_timer = now + 1500
            winner = self.game.get_winner()
            if winner == "player":
                self.sound.play("win")
            else:
                self.sound.play("lose")

        # Check for game over transition from TRIGGER_PULL
        if self.screen_state == "TRIGGER_PULL" and self.game.state == GameState.GAME_OVER:
            self.screen_state = "GAME_OVER"
            self.create_game_over_buttons()

    def draw(self) -> None:
        """Draw the current screen."""
        # Apply screen shake if active
        shake_offset = self.shotgun_view.get_shake_offset()
        if shake_offset != (0, 0):
            # Create a subsurface offset for shake effect
            shake_surf = pygame.Surface((WIDTH, HEIGHT))
            self.draw_screen(shake_surf)
            self.screen.blit(shake_surf, shake_offset)
        else:
            self.draw_screen(self.screen)

    def draw_screen(self, surface: pygame.Surface) -> None:
        """Draw the current screen to the given surface."""
        if self.screen_state == "TITLE":
            draw_title_screen(surface, self.buttons)

        elif self.screen_state == "PLAYER_TURN":
            draw_player_turn(surface, self.game, self.buttons, self.reveal_dealer)

        elif self.screen_state == "DEALER_TURN":
            draw_dealer_turn(surface, self.game, self.buttons, self.reveal_dealer)

        elif self.screen_state == "ROUND_RESULT":
            draw_round_result(surface, self.game, self.buttons)

        elif self.screen_state == "TRIGGER_PULL":
            draw_trigger_pull(surface, self.game, self.buttons, self.shotgun_view)

        elif self.screen_state == "GAME_OVER":
            draw_game_over(surface, self.game, self.buttons)


def main() -> None:
    """Entry point."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()