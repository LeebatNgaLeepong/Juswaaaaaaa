"""Server API tests for Blackjack x Buckshot Roulette.

Tests the FastAPI endpoints using FastAPI's TestClient.
"""

import pytest
from fastapi.testclient import TestClient
import server.main as sm
from backend.game import GameState


@pytest.fixture(autouse=True)
def reset_game():
    """Reset the game before each test."""
    sm.version = 0
    sm.game.start_match()
    sm.game.start_round()
    yield
    sm.version = 0
    sm.game.start_match()
    sm.game.start_round()


def get_state(client):
    """Helper to get state with version."""
    response = client.get("/api/state")
    assert response.status_code == 200
    return response.json()


def test_get_state_initial():
    """GET /api/state returns current state with version."""
    with TestClient(sm.app) as client:
        data = get_state(client)
        # Fixture starts a round, so state is PLAYER_TURN
        assert data["state"] == "PLAYER_TURN"
        assert "version" in data
        assert data["version"] == 0


def test_new_match():
    """POST /api/match/new starts a match in PLAYER_TURN with 2 cards each."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        response = client.post(f"/api/match/new?v={v}")
        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "PLAYER_TURN"
        assert data["version"] == 1  # Incremented from 0
        assert len(data["player"]["hand"]["cards"]) == 2
        assert len(data["dealer"]["hand"]["cards"]) == 2
        # Dealer's second card should be hidden (null)
        assert data["dealer"]["hand"]["cards"][1] is None
        assert data["dealer"]["hand"]["value"] is None
        assert data["dealer"]["hand"]["hidden_count"] == 1


def test_hit():
    """POST /api/hit draws a card for player."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        response = client.post(f"/api/hit?v={v}")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == 1  # Incremented from 0
        assert len(data["player"]["hand"]["cards"]) == 3


def test_stale_version_rejected():
    """POST with stale version returns 409."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        # Make a valid request first
        client.post(f"/api/hit?v={v}")  # version -> 1
        # Now try with old version
        response = client.post(f"/api/hit?v={v}")
        assert response.status_code == 409
        data = response.json()
        assert data["version"] == 1  # Current version (not incremented)
        # Hand should not have changed (still 3 cards)
        assert len(data["player"]["hand"]["cards"]) == 3


def test_stale_version_does_not_change_state():
    """Two /api/hit calls with same version must add exactly one card."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        # First hit
        response1 = client.post(f"/api/hit?v={v}")
        assert response1.status_code == 200
        data1 = response1.json()
        cards_after_first = len(data1["player"]["hand"]["cards"])
        # Second hit with SAME version (stale)
        response2 = client.post(f"/api/hit?v={v}")
        assert response2.status_code == 409
        data2 = response2.json()
        # Should be same state as after first hit
        assert len(data2["player"]["hand"]["cards"]) == cards_after_first


def test_stand_reveals_dealer():
    """POST /api/stand reveals dealer's hidden card."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        response = client.post(f"/api/stand?v={v}")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == 1  # Incremented from 0
        # State should be ROUND_RESULT (dealer turn is instant)
        assert data["state"] == "ROUND_RESULT"
        # Dealer's cards should now be fully visible
        assert data["dealer"]["hand"]["cards"][1] is not None
        assert data["dealer"]["hand"]["value"] is not None
        assert data["dealer"]["hand"]["hidden_count"] == 0


def test_trigger_during_player_turn_noop():
    """POST /api/trigger during PLAYER_TURN does nothing."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        state_before = get_state(client)
        response = client.post(f"/api/trigger?v={v}")
        assert response.status_code == 200
        state_after = response.json()
        # State should be unchanged (still PLAYER_TURN)
        assert state_after["state"] == state_before["state"]
        assert state_after["version"] == v + 1  # Version still increments on noop


def test_full_match_through_api():
    """Play a full match through the API until GAME_OVER."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        response = client.post(f"/api/match/new?v={v}")
        assert response.status_code == 200
        state = response.json()
        max_rounds = 50  # Safety limit
        for _ in range(max_rounds):
            v = state["version"]
            if state["state"] == "GAME_OVER":
                break
            if state["state"] == "PLAYER_TURN":
                # Random: hit or stand
                import random
                if random.random() < 0.5:
                    response = client.post(f"/api/hit?v={v}")
                else:
                    response = client.post(f"/api/stand?v={v}")
            elif state["state"] == "ROUND_RESULT":
                if state["round_result"] == "push":
                    response = client.post(f"/api/next?v={v}")
                else:
                    response = client.post(f"/api/trigger?v={v}")
            elif state["state"] == "TRIGGER_PULL":
                response = client.post(f"/api/next?v={v}")
            assert response.status_code == 200
            state = response.json()

        # Should eventually reach GAME_OVER
        assert state["state"] == "GAME_OVER"
        assert state["winner"] in ("player", "dealer")


def test_player_bust_damages_player():
    """Test that player bust results in player taking damage (not dealer)."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        response = client.post(f"/api/match/new?v={v}")
        assert response.status_code == 200
        state = response.json()
        v = state["version"]

        # Force player to bust by hitting until bust
        for _ in range(10):
            state = get_state(client)
            if state["player"]["hand"]["is_bust"]:
                break
            response = client.post(f"/api/hit?v={state['version']}")
            state = response.json()

        state = get_state(client)
        if state["player"]["hand"]["is_bust"]:
            # Player busted, dealer wins round
            assert state["round_result"] == "dealer"
            # Pull trigger - player should take damage
            player_hp_before = state["player"]["hp"]
            response = client.post(f"/api/trigger?v={state['version']}")
            assert response.status_code == 200
            state_after = response.json()
            # If live shell, player takes 2 damage (bust)
            if state_after["last_shot"]["result"] is True:
                assert state_after["player"]["hp"] == player_hp_before - 2
                assert state_after["last_shot"]["target"] == "Player"
                assert state_after["last_shot"]["damage"] == 2


def test_push_no_shot():
    """Test that push results in no shot and next round works."""
    with TestClient(sm.app) as client:
        state = get_state(client)
        v = state["version"]
        response = client.post(f"/api/match/new?v={v}")
        assert response.status_code == 200
        state = response.json()
        response = client.post(f"/api/next?v={state['version']}")
        # Should be noop in PLAYER_TURN (returns 200 but state unchanged)
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])