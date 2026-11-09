# Bharathiyar

A public archive of **Subramania Bharati (Bharathiyar)** — poems, essays, stories, speeches in print, and life writing — with Tamil keyword search and a GenZ-facing web experience.

Live site:  
**https://Gopal9797.github.io/Bharathiyar/**

Use that URL (no `/web/` at the end). `/web/` is only the source folder and will show a blank page.

**GitHub Pages setting:** Settings → Pages → Deploy from branch → Branch `main` → folder **`/docs`**.  
(Or switch the source to **GitHub Actions** and use the workflow in `.github/workflows/deploy-pages.yml`.)

His own writings (d. 1921) are in the public domain (nationalised 1949). English under titles are **short glosses only**, not full verse translations.

---

## What’s on the shelf

| Kind | Examples |
|------|----------|
| Poems | தேசிய கீதங்கள், கண்ணன் பாட்டு, பாஞ்சாலி சபதம், விநாயகர் நான்மணிமாலை |
| Articles | கட்டுரைகள், பகவத் கீதை commentary, என் ஈரோடு யாத்திரை |
| Stories | கதைக் கொத்து, நவதந்திரக் கதைகள், சந்திரிகையின் கதை |
| Speech texts | Printed 1920 address summary |
| Life writing | கனவு and related pieces |

Also: historical & modern licensed art, film/YouTube links, published biographies (titles + notes only), and a life / speeches timeline.

---

## Tech stack

### Public site (`web/`)

| Layer | Choice |
|-------|--------|
| UI | React 19 + TypeScript |
| Build | Vite |
| Routing | React Router |
| Motion | Framer Motion |
| Hosting | GitHub Pages (static) |
| CI deploy | GitHub Actions → `actions/deploy-pages` |
| Unit tests | Vitest (search / catalog smoke) |
| E2E | Playwright (full-site crawl) |

Search mirrors the Python shelf: Tamil word-start matching (e.g. பெண் → பெண்கள்), English theme aliases (`freedom` → விடுதலை / சுதந்திர), title / theme / body scoring.

### Catalog & local shelf (repo root)

| Layer | Choice |
|-------|--------|
| Catalog builder | Python (`scripts/build_catalog.py`) |
| Source texts | Project Madurai Unicode HTML editions |
| Data | `data/works.json` (synced into `web/public/data/`) |
| Local explorer | Streamlit ≥ 1.67 (`streamlit_app.py`) |

---

## Project layout

```
Bharathiyar/
├── web/                 # GenZ React app (GitHub Pages)
│   ├── e2e/             # Playwright crawl + smoke tests
│   ├── src/             # pages, search, media, life data
│   └── public/          # works.json + images
├── bharathi/            # Python catalog + search (Streamlit)
├── app_pages/           # Streamlit pages
├── scripts/             # build_catalog.py
├── data/                # works.json, NOTICE, sources (local)
├── assets/              # historical portraits (also copied to web)
└── .github/workflows/   # Pages deploy
```

---

## Run locally

### Web app

```bash
cd web
npm install
npm run sync-data
npm run dev
```

Open `http://127.0.0.1:5173/Bharathiyar/` (production base path is `/Bharathiyar/`).

```bash
npm test          # Vitest
npm run test:e2e  # Playwright (builds + previews, or reuses :4173)
npm run build && npm run preview
```

### Streamlit shelf

```bash
.\.venv\Scripts\streamlit.exe run streamlit_app.py --server.headless=true --server.address=127.0.0.1 --server.port=8765
```

### Rebuild the catalog from Project Madurai HTML

```bash
.\.venv\Scripts\python.exe .\scripts\build_catalog.py
cd web && npm run sync-data
```

---

## Sources & credits

- **Texts:** Project Madurai electronic editions — keep their acknowledgement when redistributing (`data/NOTICE.txt`).
- **என் ஈரோடு யாத்திரை:** Bharati’s *Swadesamitran* article, 4 August 1921.
- **Images:** Wikimedia Commons (public domain, GODL-India, CC BY-SA). Modern hero art: Dhayanithi, *Mahakavi Subramania Bharathiyar*, CC BY-SA 4.0. See `web/public/assets/credits.json`.
- **Films:** YouTube links only; this project does not host video files.

---

## License note

Bharati’s own writings are public domain. Project Madurai editions and third-party images carry their own terms — do not strip attributions.
