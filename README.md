# Bharathiyar

Public-domain poems, essays, stories, and life writing of Subramania Bharati (Bharathiyar), with Tamil keyword search.

## Public site (GitHub Pages)

The GenZ web app lives in [`web/`](web/). After you push `main` and enable Pages (GitHub Actions), it serves at:

`https://<your-user>.github.io/Bharathiyar/`

```bash
cd web
npm install
npm run sync-data
npm run dev
```

## Local Streamlit shelf

```bash
.\.venv\Scripts\streamlit.exe run streamlit_app.py --server.headless=true --server.address=127.0.0.1 --server.port=8765
```

Catalog rebuild:

```bash
.\.venv\Scripts\python.exe .\scripts\build_catalog.py
```

English under titles are short glosses only, not full verse translations.
