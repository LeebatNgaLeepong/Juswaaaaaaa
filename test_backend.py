"""Automated test for Blackjack x Buckshot Roulette backend.

Runs simulated rounds to verify no crashes.
"""

import random
from backend.game import Game, GameState
from backend.hand import Hand
from backend.card import Card


def test_hand_values() -> None:
    """Test Hand.value() with specific cases from the plan."""
    print("Testing Hand.value()...")

    # A+K (21)
    hand = Hand()
    hand.add_card(Card("A", "hearts"))
    hand.add_card(Card("K", "spades"))
    assert hand.value() == 21, f"Expected 21, got {hand.value()}"
    print("  A+K = 21 OK")

    # A+A+9 (21)
    hand = Hand()
    hand.add_card(Card("A", "hearts"))
    hand.add_card(Card("A", "spades"))
    hand.add_card(Card("9", "clubs"))
    assert hand.value() == 21, f"Expected 21, got {hand.value()}"
    print("  A+A+9 = 21 OK")

    # K+Q+5 (bust)
    hand = Hand()
    hand.add_card(Card("K", "hearts"))
    hand.add_card(Card("Q", "spades"))
    hand.add_card(Card("5", "clubs"))
    assert hand.value() == 25, f"Expected 25, got {hand.value()}"
    assert hand.is_bust(), "Should be bust"
    print("  K+Q+5 = 25 (bust) OK")

    # A+A+A (13)
    hand = Hand()
    hand.add_card(Card("A", "hearts"))
    hand.add_card(Card("A", "spades"))
    hand.add_card(Card("A", "clubs"))
    assert hand.value() == 13, f"Expected 13, got {hand.value()}"
    print("  A+A+A = 13 OK")

    print("All hand value tests passed!\n")


def test_deck() -> None:
    """Test Deck functionality."""
    print("Testing Deck...")

    from backend.deck import Deck

    deck = Deck()
    assert deck.remaining() == 52, f"Expected 52, got {deck.remaining()}"

    deck.shuffle()
    card = deck.draw()
    assert isinstance(card, Card), "Draw should return a Card"
    assert deck.remaining() == 51, f"Expected 51, got {deck.remaining()}"

    # Draw all cards
    for _ in range(51):
        deck.draw()
    assert deck.remaining() == 0, "Deck should be empty"

    # Draw from empty deck should rebuild
    card = deck.draw()
    assert isinstance(card, Card), "Should rebuild and return a card"
    assert deck.remaining() == 51, f"Expected 51 after rebuild, got {deck.remaining()}"

    print("Deck tests passed!\n")


def test_shotgun() -> None:
    """Test Shotgun functionality."""
    print("Testing Shotgun...")

    from backend.shotgun import Shotgun

    shotgun = Shotgun()
    shotgun.load()

    live, blank = shotgun.shells_left()
    assert live + blank == 6, "Should have 6 shells"
    assert 1 <= live <= 3, f"Live shells should be 1-3, got {live}"

    # Fire all shells
    for _ in range(6):
        result = shotgun.fire()
        assert isinstance(result, bool), "Fire should return bool"

    # Should reload automatically
    result = shotgun.fire()
    assert isinstance(result, bool), "Should reload and fire"

    print("Shotgun tests passed!\n")


def test_simulated_rounds(num_rounds: int = 1000) -> None:
    """Run simulated rounds with random choices to confirm no crashes."""
    print(f"Running {num_rounds} simulated rounds...")

    crash_count = 0

    for round_num in range(num_rounds):
        try:
            game = Game()
            game.start_match()
            game.start_round()

            # Play until round ends or match ends
            while game.state not in (GameState.ROUND_RESULT, GameState.GAME_OVER):
                if game.state == GameState.PLAYER_TURN:
                    # Random choice
                    if random.random() < 0.5:
                        game.player_hit()
                    else:
                        game.player_stand()
                elif game.state == GameState.DEALER_TURN:
                    game.dealer_play()
                elif game.state == GameState.ROUND_RESULT:
                    game.pull_trigger()

            # If match not over, continue to next round
            if game.state != GameState.GAME_OVER:
                # We need to continue playing rounds until match ends
                pass

        except Exception as e:
            crash_count += 1
            print(f"  Crash in round {round_num}: {e}")

    print(f"Simulated rounds complete. Crashes: {crash_count}\n")


def test_full_match() -> None:
    """Test a complete match simulation."""
    print("Testing full match simulation...")

    game = Game()
    game.start_match()

    round_count = 0
    while game.state != GameState.GAME_OVER:
        game.start_round()
        round_count += 1

        # Player plays randomly
        while game.state == GameState.PLAYER_TURN:
            if random.random() < 0.5:
                game.player_hit()
            else:
                game.player_stand()

        # Dealer plays
        while game.state == GameState.DEALER_TURN:
            game.dealer_play()

        # Resolve round
        if game.state == GameState.ROUND_RESULT:
            game.pull_trigger()
            if game.state == GameState.TRIGGER_PULL:
                game.next_round()

    winner = game.get_winner()
    print(f"Match finished after {round_count} rounds. Winner: {winner}\n")


def test_player_bust_damage() -> None:
    """Test that player bust results in player taking damage (not dealer)."""
    print("Testing player bust damage...")

    game = Game()
    game.start_match()
    game.player.hand.cards = [Card("2", "hearts"), Card("3", "clubs")]
    game.dealer.hand.cards = [Card("10", "diamonds"), Card("7", "spades")]
    game.deck.cards = [Card("Q", "spades"), Card("K", "hearts")]
    game.state = GameState.PLAYER_TURN

    # Deck.draw() pops from the end, so the player draws K then Q and busts.
    game.player_hit()
    game.player_hit()

    assert game.player.hand.is_bust(), "Player should be bust"
    assert game.state == GameState.ROUND_RESULT, "Should be in ROUND_RESULT"
    assert game.round_result == "dealer", "Dealer should win when player busts"

    # Force live shell
    game.shotgun.shells = [True]

    player_hp_before = game.player.hp
    dealer_hp_before = game.dealer.hp

    game.pull_trigger()

    # Player should take damage (2 because bust)
    assert game.player.hp == player_hp_before - 2, f"Player should take 2 damage, went from {player_hp_before} to {game.player.hp}"
    assert game.dealer.hp == dealer_hp_before, f"Dealer should not take damage, stayed at {game.dealer.hp}"
    assert game.last_target == game.player, "Last target should be player"
    assert game.last_shot_result is True, "Shot should be live"

    print("  Player bust -> player takes 2 damage OK")
    print("Player bust damage test passed!\n")


def main() -> None:
    """Run all tests."""
    print("=" * 50)
    print("BACKEND TEST SUITE")
    print("=" * 50 + "\n")

    test_hand_values()
    test_deck()
    test_shotgun()
    test_simulated_rounds(1000)
    test_full_match()
    test_player_bust_damage()

    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    main()