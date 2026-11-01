# Blackjack x Buckshot Roulette

A turn-based card game combining Blackjack with Buckshot Roulette mechanics.

## Project Overview

- **Course**: CPROG 1 Final Project
- **Language**: Python with Pygame (frontend)
- **Mode**: Solo only (player vs computer dealer)

## Game Rules

1. Player and dealer play rounds of Blackjack
2. Loser of each round pulls the trigger on a shotgun loaded with live/blank shells
3. Live shell = 1 HP damage (2 if busted)
4. First to 0 HP loses the match

## File Structure

```
├── main.py              # Entry point (Pygame loop later)
├── cli_test.py          # Terminal version to test backend
├── test_backend.py      # Automated test suite
├── backend/
│   ├── card.py          # Card class
│   ├── deck.py          # Deck class
│   ├── hand.py          # Hand class
│   ├── shotgun.py       # Shotgun class
│   ├── player.py        # Participant class (player & dealer)
│   ├── dealer_ai.py     # Dealer decision logic
│   └── game.py          # Game controller & state machine
├── assets/              # Images and sounds (later)
└── README.md
```

## Running the Tests

```bash
python test_backend.py
```

## Running the CLI Version

```bash
python cli_test.py
```

## Backend Classes

- **Card**: Rank/suit with base_value() for Blackjack
- **Deck**: 52 cards, shuffle, draw, auto-rebuild
- **Hand**: Cards collection, value calculation with Ace handling
- **Shotgun**: 6 shells (1-3 live), fire, peek, shell counts
- **Participant**: Name, HP (3), Hand, damage/reset
- **DealerAI**: Hits below 17, stands at 17+
- **Game**: State machine (MENU, PLAYER_TURN, DEALER_TURN, ROUND_RESULT, TRIGGER_PULL, GAME_OVER)

## Next Steps

1. Implement Pygame frontend in `main.py`
2. Add assets (images, sounds)
3. Implement optional features (items, difficulty levels, score tracking)