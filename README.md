# Bharathiyar

A public archive of **Subramania Bharati (Bharathiyar)** — poems, essays, stories, printed speech texts, and life writing — with Tamil keyword search and a GenZ web experience.

| | |
|---|---|
| **Live site** | https://Gopal9797.github.io/Bharathiyar/ |
| **Repository** | https://github.com/Gopal9797/Bharathiyar |

> Open the live URL **without** `/web/` at the end. `/web/` is the React *source* tree and shows a blank page on GitHub Pages.

His writings (d. 1921) are in the **public domain** (nationalised 1949). English under titles are **short glosses only**, not full verse translations.

---

## Features

- **Shelf of 400+ works** from Project Madurai editions (poems, articles, stories, speech summary, life writing)
- **Search** with Tamil word-start matching (e.g. பெண் → பெண்கள்) and English theme aliases (`freedom`, `women`, …)
- **Explore** by kind and collection
- **Reader** with related works
- **Visuals** — historical photos + licensed modern art
- **Films** — YouTube links to the 2000 film and songs
- **Books** — published biographies (titles and notes only)
- **About** — life timeline, speeches in context, source list

---

## Tech stack

### Public website (`web/` → built into `docs/`)

| Layer | Technology |
|-------|------------|
| UI | React 19, TypeScript |
| Bundler | Vite |
| Routing | React Router |
| Animation | Framer Motion |
| Hosting | GitHub Pages (static) |
| Unit tests | Vitest |
| E2E tests | Playwright (full-site crawl) |
| Optional CI | GitHub Actions (`.github/workflows/deploy-pages.yml`) |

### Catalog & local tools

| Layer | Technology |
|-------|------------|
| Catalog builder | Python (`scripts/build_catalog.py`) |
| Text sources | Project Madurai Unicode HTML |
| Data file | `data/works.json` |
| Local explorer | Streamlit ≥ 1.67 (`streamlit_app.py`) |

---

## Repository layout

```
Bharathiyar/
├── docs/                  # Built site served by GitHub Pages (commit after npm run build)
├── web/                   # React + TypeScript source
│   ├── e2e/               # Playwright tests
│   ├── src/               # Pages, search, media, life data
│   └── public/            # Catalog + images copied into the build
├── bharathi/              # Python catalog + search (Streamlit)
├── app_pages/             # Streamlit pages
├── scripts/build_catalog.py
├── data/works.json        # Master catalog
├── assets/                # Historical portraits
└── .github/workflows/     # Optional Actions deploy
```

---

## GitHub Pages setup

**Recommended (branch + `/docs`):**

1. Build and refresh `docs/`:
   ```bash
   cd web
   npm install
   npm run build
   # from repo root on Windows PowerShell:
   Remove-Item -Recurse -Force ..\docs -ErrorAction SilentlyContinue
   Copy-Item -Recurse dist ..\docs
   ```
2. Commit and push `docs/` to `main`.
3. Repo **Settings → Pages**:
   - Source: **Deploy from a branch**
   - Branch: `main`
   - Folder: **`/docs`**
4. Visit https://Gopal9797.github.io/Bharathiyar/

**Alternative:** set Pages source to **GitHub Actions** and use `.github/workflows/deploy-pages.yml` (publishes `web/dist` directly).

---

## Run locally

### Web app

```bash
cd web
npm install
npm run sync-data
npm run dev
```

Open `http://127.0.0.1:5173/Bharathiyar/` (base path is `/Bharathiyar/`).

```bash
npm test              # Vitest — search / catalog smoke tests
npm run test:e2e      # Playwright crawl
npm run build && npm run preview
```

### Streamlit shelf (optional)

```bash
.\.venv\Scripts\streamlit.exe run streamlit_app.py --server.headless=true --server.address=127.0.0.1 --server.port=8765
```

### Rebuild catalog from Project Madurai HTML

```bash
.\.venv\Scripts\python.exe .\scripts\build_catalog.py
cd web && npm run sync-data
```

---

## What’s on the shelf (examples)

| Kind | Examples |
|------|----------|
| Poems | தேசிய கீதங்கள், கண்ணன் பாட்டு, பாஞ்சாலி சபதம், விநாயகர் நான்மணிமாலை |
| Articles | கட்டுரைகள், பகவத் கீதை commentary, என் ஈரோடு யாத்திரை |
| Stories | கதைக் கொத்து, நவதந்திரக் கதைகள், சந்திரிகையின் கதை |
| Speech texts | Printed 1920 address summary |
| Life writing | கனவு and related pieces |

---

## Sources & credits

- **Texts:** Project Madurai electronic editions — keep their acknowledgement (`data/NOTICE.txt`).
- **என் ஈரோடு யாத்திரை:** Bharati’s *Swadesamitran* article, 4 August 1921.
- **Images:** Wikimedia Commons (public domain, GODL-India, CC BY-SA). Hero art: Dhayanithi, *Mahakavi Subramania Bharathiyar*, CC BY-SA 4.0 — see `web/public/assets/credits.json` / `docs/assets/credits.json`.
- **Films:** YouTube links only; this project does not host video files.

---

## License note

Bharati’s own writings are public domain. Project Madurai editions and third-party images keep their own terms — do not strip attributions.
