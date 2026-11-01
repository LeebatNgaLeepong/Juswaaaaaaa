"""Participant class for Blackjack x Buckshot Roulette.

Represents a player or dealer in the game.
"""

from backend.hand import Hand


class Participant:
    """A participant in the game (player or dealer)."""

    def __init__(self, name: str, hp: int = 3) -> None:
        """Initialize a participant with a name and starting HP.

        Args:
            name: The participant's name
            hp: Starting hit points (default 3)
        """
        self.name = name
        self.hp = hp
        self.hand = Hand()

    def take_damage(self, amount: int) -> None:
        """Reduce HP by the given amount, never below 0.

        Args:
            amount: Damage to apply
        """
        self.hp = max(0, self.hp - amount)

    def is_dead(self) -> bool:
        """Check if the participant has 0 HP.

        Returns:
            True if HP is 0
        """
        return self.hp <= 0

    def reset_for_round(self) -> None:
        """Clear the hand for the next round."""
        self.hand.clear()

    def __str__(self) -> str:
        """Return a string representation of the participant."""
        return f"{self.name} (HP: {self.hp})"

    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        return f"Participant(name='{self.name}', hp={self.hp}, hand={self.hand})"