"""Serializers for Blackjack x Buckshot Roulette server.

Converts Game state to JSON-serializable dictionaries.
"""

from backend.game import Game, GameState
from backend.card import Card


def card_to_dict(card: Card | None) -> dict | None:
    """Convert a Card to a dictionary.

    Args:
        card: Card to convert, or None for a hidden card

    Returns:
        Dictionary with rank and suit, or None
    """
    if card is None:
        return None
    return {"rank": card.rank, "suit": card.suit}


def hand_to_dict(hand, hide_second: bool = False) -> dict:
    """Convert a Hand to a dictionary.

    Args:
        hand: Hand object to convert
        hide_second: If True, hide the second card (for dealer during PLAYER_TURN)

    Returns:
        Dictionary with cards, value, is_bust, is_blackjack, and hidden_count
    """
    cards = []
    for i, card in enumerate(hand.cards):
        if hide_second and i == 1:
            cards.append(None)
        else:
            cards.append(card_to_dict(card))

    hidden_count = 1 if (hide_second and len(hand.cards) > 1) else 0

    if hide_second and len(hand.cards) > 1:
        return {
            "cards": cards,
            "value": None,
            "is_bust": False,
            "is_blackjack": False,
            "hidden_count": hidden_count,
        }

    return {
        "cards": cards,
        "value": hand.value(),
        "is_bust": hand.is_bust(),
        "is_blackjack": hand.is_blackjack(),
        "hidden_count": hidden_count,
    }


def participant_to_dict(participant, hide_second: bool = False) -> dict:
    """Convert a Participant to a dictionary.

    Args:
        participant: Participant to convert
        hide_second: If True, hide the second card of the hand

    Returns:
        Dictionary with name, hp, and hand info
    """
    return {
        "name": participant.name,
        "hp": participant.hp,
        "hand": hand_to_dict(participant.hand, hide_second),
    }


def shotgun_to_dict(shotgun) -> dict:
    """Convert a Shotgun to a dictionary.

    Args:
        shotgun: Shotgun to convert

    Returns:
        Dictionary with live and blank counts
    """
    live, blank = shotgun.shells_left()
    return {"live": live, "blank": blank}


def last_shot_to_dict(game: Game) -> dict:
    """Convert the last shot result to a dictionary.

    Args:
        game: Game object

    Returns:
        Dictionary with result, target, and damage
    """
    if game.last_shot_result is None:
        return {"result": None, "target": None, "damage": 0}

    target_name = game.last_target.name if game.last_target else None
    return {
        "result": game.last_shot_result,
        "target": target_name,
        "damage": game.last_damage,
    }


def game_to_dict(game: Game) -> dict:
    """Convert the entire Game state to a dictionary for the API.

    Args:
        game: Game object

    Returns:
        Dictionary with full game state
    """
    # During PLAYER_TURN, hide dealer's second card and value
    hide_dealer = game.state == GameState.PLAYER_TURN

    return {
        "state": game.state.value,
        "round_result": game.round_result,
        "player": participant_to_dict(game.player, hide_second=False),
        "dealer": participant_to_dict(game.dealer, hide_second=hide_dealer),
        "shotgun": shotgun_to_dict(game.shotgun),
        "last_shot": last_shot_to_dict(game),
        "winner": game.get_winner(),
    }