"""Sound manager for Blackjack x Buckshot Roulette.

Safe loading and playing of sound effects.
"""

import os
import pygame
from frontend.constants import (
    SOUNDS_DIR,
    SOUND_CARD, SOUND_CLICK, SOUND_SHOT_LIVE, SOUND_SHOT_BLANK,
    SOUND_WIN, SOUND_LOSE
)


class SoundManager:
    """Manages game sound effects with safe loading."""

    def __init__(self) -> None:
        """Initialize the sound manager."""
        self.sounds: dict[str, pygame.mixer.Sound | None] = {}
        self.enabled = True

        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False

        # Sound name to filename mapping
        self.sound_files = {
            SOUND_CARD: "card_flip.wav",
            SOUND_CLICK: "click.wav",
            SOUND_SHOT_LIVE: "shot_live.wav",
            SOUND_SHOT_BLANK: "shot_blank.wav",
            SOUND_WIN: "win.wav",
            SOUND_LOSE: "lose.wav",
        }

        # Load all sounds
        for name, filename in self.sound_files.items():
            self.load(name, filename)

    def load(self, name: str, filename: str) -> None:
        """Load a sound file if it exists.

        Args:
            name: Internal name to reference the sound
            filename: Filename in assets/sounds/
        """
        if not self.enabled:
            self.sounds[name] = None
            return

        path = os.path.join(SOUNDS_DIR, filename)
        try:
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
            else:
                self.sounds[name] = None
        except pygame.error:
            self.sounds[name] = None

    def play(self, name: str) -> None:
        """Play a sound by name.

        Args:
            name: Sound name (must have been loaded)
        """
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def stop(self, name: str) -> None:
        """Stop a sound by name."""
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.stop()