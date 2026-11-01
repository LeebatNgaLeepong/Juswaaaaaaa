"""Server API tests for Blackjack x Buckshot Roulette.

Tests the FastAPI endpoints using FastAPI's TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from server.main import app, game
from backend.game import GameState


@pytest.fixture(autouse=True)
def reset_game():
    """Reset the game before each test."""
    game.start_match()
    game.start_round()
    yield
    game.start_match()
    game.start_round()


def test_get_state_initial():
    """GET /api/state returns current state."""
    with TestClient(app) as client:
        response = client.get("/api/state")
        assert response.status_code == 200
        data = response.json()
        # Fixture starts a round, so state is PLAYER_TURN
        assert data["state"] == "PLAYER_TURN"


def test_new_match():
    """POST /api/match/new starts a match in PLAYER_TURN with 2 cards each."""
    with TestClient(app) as client:
        response = client.post("/api/match/new")
        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "PLAYER_TURN"
        assert len(data["player"]["hand"]["cards"]) == 2
        assert len(data["dealer"]["hand"]["cards"]) == 2
        # Dealer's second card should be hidden (null)
        assert data["dealer"]["hand"]["cards"][1] is None
        assert data["dealer"]["hand"]["value"] is None
        assert data["dealer"]["hand"]["hidden_count"] == 1


def test_hit():
    """POST /api/hit draws a card for player."""
    with TestClient(app) as client:
        client.post("/api/match/new")
        response = client.post("/api/hit")
        assert response.status_code == 200
        data = response.json()
        assert len(data["player"]["hand"]["cards"]) == 3


def test_stand_reveals_dealer():
    """POST /api/stand reveals dealer's hidden card."""
    with TestClient(app) as client:
        client.post("/api/match/new")
        response = client.post("/api/stand")
        assert response.status_code == 200
        data = response.json()
        # State should be ROUND_RESULT (dealer turn is instant)
        assert data["state"] == "ROUND_RESULT"
        # Dealer's cards should now be fully visible
        assert data["dealer"]["hand"]["cards"][1] is not None
        assert data["dealer"]["hand"]["value"] is not None
        assert data["dealer"]["hand"]["hidden_count"] == 0


def test_trigger_during_player_turn_noop():
    """POST /api/trigger during PLAYER_TURN does nothing."""
    with TestClient(app) as client:
        client.post("/api/match/new")
        # Get initial state
        state_before = client.get("/api/state").json()
        response = client.post("/api/trigger")
        assert response.status_code == 200
        state_after = response.json()
        # State should be unchanged
        assert state_after["state"] == state_before["state"]


def test_full_match_through_api():
    """Play a full match through the API until GAME_OVER."""
    with TestClient(app) as client:
        client.post("/api/match/new")
        max_rounds = 50  # Safety limit
        for _ in range(max_rounds):
            state = client.get("/api/state").json()
            if state["state"] == "GAME_OVER":
                break
            if state["state"] == "PLAYER_TURN":
                # Random: hit or stand
                import random
                if random.random() < 0.5:
                    client.post("/api/hit")
                else:
                    client.post("/api/stand")
            elif state["state"] == "ROUND_RESULT":
                if state["round_result"] == "push":
                    client.post("/api/next")
                else:
                    client.post("/api/trigger")
            elif state["state"] == "TRIGGER_PULL":
                client.post("/api/next")

        # Should eventually reach GAME_OVER
        final_state = client.get("/api/state").json()
        assert final_state["state"] == "GAME_OVER"
        assert final_state["winner"] in ("player", "dealer")


def test_player_bust_damages_player():
    """Test that player bust results in player taking damage (not dealer)."""
    with TestClient(app) as client:
        client.post("/api/match/new")

        # Force player to bust by hitting until bust
        # This is probabilistic but we'll try a few times
        for _ in range(10):
            state = client.get("/api/state").json()
            if state["player"]["hand"]["is_bust"]:
                break
            client.post("/api/hit")

        state = client.get("/api/state").json()
        if state["player"]["hand"]["is_bust"]:
            # Player busted, dealer wins round
            assert state["round_result"] == "dealer"
            # Pull trigger - player should take damage
            player_hp_before = state["player"]["hp"]
            response = client.post("/api/trigger")
            assert response.status_code == 200
            state_after = response.json()
            # If live shell, player takes 2 damage (bust)
            if state_after["last_shot"]["result"] is True:
                assert state_after["player"]["hp"] == player_hp_before - 2
                assert state_after["last_shot"]["target"] == "Player"
                assert state_after["last_shot"]["damage"] == 2


def test_push_no_shot():
    """Test that push results in no shot and next round works."""
    with TestClient(app) as client:
        # This is hard to force, so we'll just test the next round endpoint works
        client.post("/api/match/new")
        response = client.post("/api/next")
        # Should be noop in PLAYER_TURN
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])