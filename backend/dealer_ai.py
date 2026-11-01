"""DealerAI class for Blackjack x Buckshot Roulette.

Contains the dealer's decision logic, kept separate for easy difficulty adjustment.
"""


class DealerAI:
    """Dealer decision logic for blackjack."""

    def __init__(self, hit_threshold: int = 17) -> None:
        """Initialize the dealer AI with a hit threshold.

        Args:
            hit_threshold: Dealer hits below this value, stands at or above (default 17)
        """
        self.hit_threshold = hit_threshold

    def decide(self, dealer_hand) -> str:
        """Decide whether the dealer should hit or stand.

        Args:
            dealer_hand: The dealer's Hand object

        Returns:
            "hit" if hand value is below threshold, otherwise "stand"
        """
        if dealer_hand.value() < self.hit_threshold:
            return "hit"
        return "stand"