"""Game class for Blackjack x Buckshot Roulette.

Orchestrates the entire game flow, round management, and state machine.
"""

from enum import Enum
from backend.deck import Deck
from backend.shotgun import Shotgun
from backend.player import Participant
from backend.hand import Hand
from backend.dealer_ai import DealerAI


class GameState(Enum):
    """Game state enumeration."""
    MENU = "MENU"
    PLAYER_TURN = "PLAYER_TURN"
    DEALER_TURN = "DEALER_TURN"
    ROUND_RESULT = "ROUND_RESULT"
    TRIGGER_PULL = "TRIGGER_PULL"
    GAME_OVER = "GAME_OVER"


class Game:
    """Main game controller managing rounds, state, and win conditions."""

    def __init__(self) -> None:
        """Initialize the game components."""
        self.deck = Deck()
        self.shotgun = Shotgun()
        self.player = Participant("Player")
        self.dealer = Participant("Dealer")
        self.state = GameState.MENU
        self.round_result: str | None = None
        self.last_shot_result: bool | None = None
        self.last_target: Participant | None = None
        self.dealer_ai = DealerAI()

    def start_match(self) -> None:
        """Reset HP, build and shuffle the deck, load the shotgun."""
        self.player.hp = 3
        self.dealer.hp = 3
        self.deck.build()
        self.deck.shuffle()
        self.shotgun.load()
        self.state = GameState.MENU

    def start_round(self) -> None:
        """Clear hands, deal 2 cards each, set state to PLAYER_TURN."""
        self.player.reset_for_round()
        self.dealer.reset_for_round()

        # Deal 2 cards each (alternating)
        for _ in range(2):
            self.player.hand.add_card(self.deck.draw())
            self.dealer.hand.add_card(self.deck.draw())

        self.state = GameState.PLAYER_TURN
        self.round_result = None
        self.last_shot_result = None
        self.last_target = None

    def player_hit(self) -> None:
        """Draw a card for the player; if bust, end the round."""
        if self.state != GameState.PLAYER_TURN:
            return  # Ignore action in wrong state

        self.player.hand.add_card(self.deck.draw())

        if self.player.hand.is_bust():
            self._end_round()

    def player_stand(self) -> None:
        """Move to DEALER_TURN."""
        if self.state != GameState.PLAYER_TURN:
            return  # Ignore action in wrong state

        self.state = GameState.DEALER_TURN
        self.dealer_play()

    def dealer_play(self) -> None:
        """Dealer keeps hitting or standing based on DealerAI until done."""
        if self.state != GameState.DEALER_TURN:
            return

        while True:
            decision = self.dealer_ai.decide(self.dealer.hand)
            if decision == "hit":
                self.dealer.hand.add_card(self.deck.draw())
                if self.dealer.hand.is_bust():
                    break
            else:
                break

        self._end_round()

    def _end_round(self) -> None:
        """Resolve the round and determine the loser."""
        self.resolve_round()
        self.state = GameState.ROUND_RESULT

    def resolve_round(self) -> None:
        """Determine the round loser based on blackjack rules.

        Rules:
        1. If player busts, dealer wins.
        2. If dealer busts, player wins.
        3. Otherwise higher hand value wins.
        4. Equal values = push (no one pulls trigger).
        5. Natural blackjack beats regular 21.
        """
        player_bust = self.player.hand.is_bust()
        dealer_bust = self.dealer.hand.is_bust()
        player_blackjack = self.player.hand.is_blackjack()
        dealer_blackjack = self.dealer.hand.is_blackjack()
        player_value = self.player.hand.value()
        dealer_value = self.dealer.hand.value()

        # Both bust - dealer wins (house advantage)
        if player_bust and dealer_bust:
            self.round_result = "dealer"
            return

        # Player busts
        if player_bust:
            self.round_result = "dealer"
            return

        # Dealer busts
        if dealer_bust:
            self.round_result = "player"
            return

        # Both have blackjack - push
        if player_blackjack and dealer_blackjack:
            self.round_result = "push"
            return

        # Player has blackjack, dealer doesn't
        if player_blackjack:
            self.round_result = "player"
            return

        # Dealer has blackjack, player doesn't
        if dealer_blackjack:
            self.round_result = "dealer"
            return

        # Compare values
        if player_value > dealer_value:
            self.round_result = "player"
        elif dealer_value > player_value:
            self.round_result = "dealer"
        else:
            self.round_result = "push"

    def pull_trigger(self) -> bool | None:
        """Fire the shotgun at the round LOSER and apply damage.

        Returns:
            True if live, False if blank, None if push or wrong state
        """
        if self.state != GameState.ROUND_RESULT:
            return None
        if self.round_result == "push":
            return None  # no shot; the frontend calls next_round()

        # round_result holds the WINNER, so the loser is the other side
        if self.round_result == "player":
            target = self.dealer
        else:
            target = self.player
        bust_damage = target.hand.is_bust()

        is_live = self.shotgun.fire()
        self.last_shot_result = is_live
        self.last_target = target  # so the UI can show who was shot
        if is_live:
            target.take_damage(2 if bust_damage else 1)

        if self.check_match_over():
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.TRIGGER_PULL  # stays here until next_round()
        return is_live

    def next_round(self) -> None:
        """Start the next round after the result or shot has been shown."""
        if self.state == GameState.TRIGGER_PULL or (
            self.state == GameState.ROUND_RESULT and self.round_result == "push"
        ):
            self.start_round()

    def check_match_over(self) -> bool:
        """Check if either side has 0 HP.

        Returns:
            True if match should end
        """
        return self.player.is_dead() or self.dealer.is_dead()

    def get_winner(self) -> str | None:
        """Get the match winner.

        Returns:
            "player" if player won, "dealer" if dealer won, None if ongoing
        """
        if self.dealer.is_dead():
            return "player"
        if self.player.is_dead():
            return "dealer"
        return None

    def __str__(self) -> str:
        """Return a string representation of the game state."""
        return (f"Game(state={self.state.value}, "
                f"player={self.player}, dealer={self.dealer}, "
                f"shotgun={self.shotgun})")

    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        return (f"Game(state={self.state}, "
                f"player={self.player!r}, dealer={self.dealer!r}, "
                f"deck_remaining={self.deck.remaining()}, "
                f"shotgun={self.shotgun!r})")