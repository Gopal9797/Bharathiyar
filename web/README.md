# Bharathiyar web

GenZ static site for Subramania Bharati’s public-domain shelf. Built with Vite + React. Hosted on GitHub Pages.

## Local

```bash
cd web
npm install
npm run sync-data
npm run dev
```

Open the URL Vite prints. The app expects to live at `/Bharathiyar/` in production; local preview uses that base path too.

```bash
npm run build
npm run preview
```

```bash
npm test
npm run test:e2e
```

Playwright rebuilds/previews the site (or reuses `http://127.0.0.1:4173/Bharathiyar/`), crawls routes, and checks scroll-to-top, images, and search/read flows.

## GitHub Pages

Push `main`. The workflow in `.github/workflows/deploy-pages.yml` builds `web/` and publishes `web/dist`. In the GitHub repo settings, set Pages source to **GitHub Actions**.

Public URL shape: `https://<user>.github.io/Bharathiyar/`

## Notes

- Tamil bodies stay as in `data/works.json`. English under titles are short glosses only.
- The Streamlit app at the repo root remains for local browsing.
- Image licenses live in `public/assets/credits.json`.
