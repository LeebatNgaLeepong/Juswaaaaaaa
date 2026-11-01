"""Main entry point for Blackjack x Buckshot Roulette.

Starts the FastAPI server (which also serves the built React app in production).
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)