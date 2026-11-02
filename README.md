# Blackjack x Buckshot Roulette

A turn-based Blackjack game with Buckshot Roulette mechanics. The game engine is
written in Python, the API is served by FastAPI, and the browser UI is built with
React and Vite.

## Requirements

- Python dependencies from `requirements.txt`
- Node.js and npm

## Run locally

Install the Python dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

In one terminal, start the API server:

```bash
python main.py
```

In another terminal, start the Vite development server:

```bash
cd web
npm install
npm run dev
```

Open the local URL printed by Vite. Its `/api` requests are proxied to the
FastAPI server on port 8000.

To build the React app for FastAPI to serve, run `npm run build` in `web/`, then
start the server with `python main.py`.

## Game rules

1. The player and dealer play Blackjack rounds.
2. The loser of each round pulls the trigger on a shotgun loaded with live and
   blank shells.
3. A live shell causes 1 HP damage (2 if the target busted).
4. The first player to reach 0 HP loses the match.

## Project layout

- `backend/` — cards, hands, dealer logic, shotgun, and game state
- `server/` — FastAPI endpoints and game-state serialization
- `web/` — React + Vite browser application and public assets
- `test_backend.py`, `test_server.py` — automated tests
- `cli_test.py` — terminal interface for exercising the game engine

## Run tests

```bash
python -m pytest
```

To play the terminal version instead of the browser UI:

```bash
python cli_test.py
```
