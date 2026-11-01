"""Deck class for Blackjack x Buckshot Roulette.

Manages a standard 52-card deck with shuffling and drawing.
"""

import random
from backend.card import Card


class Deck:
    """A standard 52-card deck."""

    def __init__(self) -> None:
        """Initialize an empty deck and build it."""
        self.cards: list[Card] = []
        self.build()

    def build(self) -> None:
        """Create a standard 52-card deck with all ranks and suits."""
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["hearts", "diamonds", "clubs", "spades"]
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self) -> None:
        """Randomize the order of cards in the deck."""
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """Remove and return the top card.

        If the deck is empty, rebuild and reshuffle first.

        Returns:
            The drawn Card
        """
        if not self.cards:
            self.build()
            self.shuffle()
        return self.cards.pop()

    def remaining(self) -> int:
        """Return the number of cards left in the deck.

        Returns:
            Count of remaining cards
        """
        return len(self.cards)