"""CLI test for Blackjack x Buckshot Roulette backend.

Terminal version to test the backend functionality.
"""

from backend.game import Game, GameState


def print_game_state(game: Game) -> None:
    """Print the current game state to the terminal."""
    print("\n" + "=" * 50)
    print(f"STATE: {game.state.value}")
    print(f"Player: {game.player} | Hand: {game.player.hand} (value: {game.player.hand.value()})")
    print(f"Dealer: {game.dealer} | Hand: {game.dealer.hand} (value: {game.dealer.hand.value()})")
    live, blank = game.shotgun.shells_left()
    print(f"Shotgun: {live} live, {blank} blank")
    if game.round_result:
        print(f"Round result: {game.round_result}")
    if game.last_shot_result is not None:
        result = "LIVE!" if game.last_shot_result else "BLANK"
        target_name = game.last_target.name if game.last_target else "Unknown"
        print(f"Last shot: {result} (target: {target_name})")
    print("=" * 50)


def main() -> None:
    """Run a full match in the terminal."""
    game = Game()
    game.start_match()
    game.start_round()

    print("Welcome to Blackjack x Buckshot Roulette!")
    print("Commands: hit, stand, pull, quit")

    while game.state != GameState.GAME_OVER:
        print_game_state(game)

        if game.state == GameState.PLAYER_TURN:
            cmd = input("Your move (hit/stand): ").strip().lower()
            if cmd == "hit":
                game.player_hit()
            elif cmd == "stand":
                game.player_stand()
            elif cmd == "quit":
                break
            else:
                print("Invalid command. Use 'hit' or 'stand'.")

        elif game.state == GameState.ROUND_RESULT:
            if game.round_result == "push":
                print("Push! No one pulls the trigger. Starting new round...")
                game.next_round()
            else:
                cmd = input("Press Enter to pull the trigger... ").strip()
                game.pull_trigger()

        elif game.state == GameState.TRIGGER_PULL:
            cmd = input("Press Enter for next round... ").strip()
            game.next_round()

    # Game over
    print_game_state(game)
    winner = game.get_winner()
    if winner == "player":
        print("\nYOU WIN! The dealer has been eliminated!")
    elif winner == "dealer":
        print("\nGAME OVER. You have been eliminated.")
    else:
        print("\nGame ended.")


if __name__ == "__main__":
    main()