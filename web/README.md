# Bharathiyar web

React + TypeScript + Vite app for the public Bharathiyar shelf. Production build is copied to `../docs/` for GitHub Pages.

## Develop

```bash
npm install
npm run sync-data
npm run dev
```

Open `http://127.0.0.1:5173/Bharathiyar/`.

## Test

```bash
npm test
npm run test:e2e
```

## Build for Pages

```bash
npm run build
```

Then from the repo root, refresh `docs/` from `web/dist` and push `main`. Pages folder must be **`/docs`**.

Live URL: https://Gopal9797.github.io/Bharathiyar/ (not `/web/`).
