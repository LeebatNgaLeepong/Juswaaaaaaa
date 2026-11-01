"""FastAPI server for Blackjack x Buckshot Roulette.

Exposes the game engine as a JSON API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.game import Game
from server.serializers import game_to_dict

app = FastAPI(title="Blackjack x Buckshot Roulette")

# Enable CORS for local development (Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single game instance in memory (solo play on one machine)
game = Game()


@app.get("/api/state")
def get_state():
    """Return the current game state."""
    return game_to_dict(game)


@app.post("/api/match/new")
def new_match():
    """Start a new match and round."""
    game.start_match()
    game.start_round()
    return game_to_dict(game)


@app.post("/api/hit")
def hit():
    """Player hits (draws a card)."""
    game.player_hit()
    return game_to_dict(game)


@app.post("/api/stand")
def stand():
    """Player stands (dealer plays)."""
    game.player_stand()
    return game_to_dict(game)


@app.post("/api/trigger")
def pull_trigger():
    """Pull the trigger (resolve round with shotgun)."""
    game.pull_trigger()
    return game_to_dict(game)


@app.post("/api/next")
def next_round():
    """Start the next round."""
    game.next_round()
    return game_to_dict(game)


# Serve built React app in production
from pathlib import Path
from fastapi.staticfiles import StaticFiles

dist = Path(__file__).resolve().parent.parent / "web" / "dist"
if dist.exists():
    app.mount("/", StaticFiles(directory=dist, html=True), name="web")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)