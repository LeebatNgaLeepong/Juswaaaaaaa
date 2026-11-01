"""FastAPI server for Blackjack x Buckshot Roulette.

Exposes the game engine as a JSON API with version guard.
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
version = 0


def state_with_version():
    """Return game state with current version."""
    data = game_to_dict(game)
    data['version'] = version
    return data


@app.get("/api/state")
def get_state():
    """Return the current game state with version."""
    return state_with_version()


def check_version(v: int = Query(...)):
    """Check if client version matches server version. Return 409 if stale."""
    global version
    if v != version:
        return JSONResponse(status_code=409, content=state_with_version())
    return None


@app.post("/api/match/new")
def new_match(v: int = Query(...)):
    """Start a new match and round."""
    stale = check_version(v)
    if stale:
        return stale
    global version
    game.start_match()
    game.start_round()
    version += 1
    return state_with_version()


@app.post("/api/hit")
def hit(v: int = Query(...)):
    """Player hits (draws a card)."""
    stale = check_version(v)
    if stale:
        return stale
    global version
    game.player_hit()
    version += 1
    return state_with_version()


@app.post("/api/stand")
def stand(v: int = Query(...)):
    """Player stands (dealer plays)."""
    stale = check_version(v)
    if stale:
        return stale
    global version
    game.player_stand()
    version += 1
    return state_with_version()


@app.post("/api/trigger")
def pull_trigger(v: int = Query(...)):
    """Pull the trigger (resolve round with shotgun)."""
    stale = check_version(v)
    if stale:
        return stale
    global version
    game.pull_trigger()
    version += 1
    return state_with_version()


@app.post("/api/next")
def next_round(v: int = Query(...)):
    """Start the next round."""
    stale = check_version(v)
    if stale:
        return stale
    global version
    game.next_round()
    version += 1
    return state_with_version()


# Serve built React app in production
from pathlib import Path
from fastapi.staticfiles import StaticFiles

dist = Path(__file__).resolve().parent.parent / "web" / "dist"
if dist.exists():
    app.mount("/", StaticFiles(directory=dist, html=True), name="web")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)