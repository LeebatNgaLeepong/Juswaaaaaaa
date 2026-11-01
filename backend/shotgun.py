"""Shotgun class for Blackjack x Buckshot Roulette.

Manages the shotgun with live and blank shells.
"""

import random


class Shotgun:
    """A shotgun loaded with live and blank shells."""

    def __init__(self) -> None:
        """Initialize an empty shotgun."""
        self.shells: list[bool] = []  # True = live, False = blank

    def load(self) -> None:
        """Load 6 shells with a random number of live shells (1-3), then shuffle."""
        num_live = random.randint(1, 3)
        num_blank = 6 - num_live
        self.shells = [True] * num_live + [False] * num_blank
        random.shuffle(self.shells)

    def fire(self) -> bool:
        """Remove and return the next shell.

        If empty, reload first.

        Returns:
            True if live shell, False if blank
        """
        if not self.shells:
            self.load()
        return self.shells.pop(0)

    def peek(self) -> bool:
        """Return the next shell without removing it.

        Used by items like Peek.

        Returns:
            True if live shell, False if blank
        """
        if not self.shells:
            self.load()
        return self.shells[0]

    def shells_left(self) -> tuple[int, int]:
        """Return the count of live and blank shells remaining.

        Returns:
            Tuple of (live_count, blank_count)
        """
        live = sum(1 for s in self.shells if s)
        blank = len(self.shells) - live
        return live, blank

    def __str__(self) -> str:
        """Return a string representation showing shell counts."""
        live, blank = self.shells_left()
        return f"Shotgun(live={live}, blank={blank})"

    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        return f"Shotgun(shells={self.shells})"