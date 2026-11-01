"""Hand class for Blackjack x Buckshot Roulette.

Represents a player's or dealer's hand of cards with blackjack value calculation.
"""

from backend.card import Card


class Hand:
    """A hand of cards in blackjack."""

    def __init__(self) -> None:
        """Initialize an empty hand."""
        self.cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        """Add a card to the hand.

        Args:
            card: The Card to add
        """
        self.cards.append(card)

    def value(self) -> int:
        """Calculate the total value of the hand.

        Aces count as 11 initially, then are reduced to 1 one at a time
        while the total exceeds 21.

        Returns:
            The blackjack value of the hand
        """
        total = sum(card.base_value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "A")

        # Reduce aces from 11 to 1 while over 21
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_bust(self) -> bool:
        """Check if the hand is over 21.

        Returns:
            True if hand value exceeds 21
        """
        return self.value() > 21

    def is_blackjack(self) -> bool:
        """Check if the hand is a natural blackjack (2 cards totaling 21).

        Returns:
            True if exactly 2 cards with value 21
        """
        return len(self.cards) == 2 and self.value() == 21

    def clear(self) -> None:
        """Empty the hand for the next round."""
        self.cards.clear()

    def __str__(self) -> str:
        """Return a string representation of the hand."""
        return ", ".join(str(card) for card in self.cards)

    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        return f"Hand(cards={self.cards})"