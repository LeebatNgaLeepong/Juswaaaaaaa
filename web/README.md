# Browser frontend

This directory contains the React application built with Vite.

## Development

From this directory, install dependencies and start the development server:

```bash
npm install
npm run dev
```

The Vite development server proxies `/api` requests to the FastAPI server at
`http://localhost:8000`. Start that server from the repository root with
`python main.py`.

## Production build

```bash
npm run build
```

The generated `dist/` directory is served by FastAPI when present. Run
`npm run lint` to check the frontend.
