"""Card class for Blackjack x Buckshot Roulette.

Represents a single playing card with a rank and suit.
"""


class Card:
    """A standard playing card."""

    def __init__(self, rank: str, suit: str) -> None:
        """Initialize a card with the given rank and suit.

        Args:
            rank: Card rank (2-10, J, Q, K, A)
            suit: Card suit (hearts, diamonds, clubs, spades)
        """
        self.rank = rank
        self.suit = suit

    def base_value(self) -> int:
        """Return the base blackjack value of the card.

        Returns:
            2-10 for number cards, 10 for face cards (J, Q, K), 11 for Ace
        """
        if self.rank in ("J", "Q", "K"):
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            String like "K of spades"
        """
        return f"{self.rank} of {self.suit}"

    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        return f"Card(rank='{self.rank}', suit='{self.suit}')"