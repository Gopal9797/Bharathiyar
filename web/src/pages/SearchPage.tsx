import { useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { PageMotion } from '../components/PageMotion'
import { WorkTile } from '../components/WorkTile'
import { useWorks } from '../hooks/useWorks'
import { KIND_ORDER, THEME_LABELS, kindLabel } from '../lib/catalog'
import { relatedKeywords, search } from '../lib/search'

export function SearchPage() {
  const { works, loading, error } = useWorks()
  const [params, setParams] = useSearchParams()
  const query = params.get('q') ?? ''
  const match = (params.get('match') as 'any' | 'all') || 'any'
  const kinds = params.getAll('kind')
  const themes = params.getAll('theme')

  const hits = useMemo(
    () =>
      search(works, query, {
        match,
        kinds,
        themes,
      }),
    [works, query, match, kinds, themes],
  )

  const suggestions = useMemo(
    () => relatedKeywords(hits, query),
    [hits, query],
  )

  function update(next: URLSearchParams) {
    setParams(next, { replace: true })
  }

  function setQuery(value: string) {
    const next = new URLSearchParams(params)
    if (value) next.set('q', value)
    else next.delete('q')
    update(next)
  }

  function toggle(key: 'kind' | 'theme', value: string) {
    const next = new URLSearchParams(params)
    const current = next.getAll(key)
    next.delete(key)
    const selected = current.includes(value)
      ? current.filter((item) => item !== value)
      : [...current, value]
    for (const item of selected) next.append(key, item)
    update(next)
  }

  return (
    <PageMotion>
      <header className="page-head">
        <p className="eyebrow">Find a line</p>
        <h1>Search</h1>
        <p>Tamil stems and English theme words both work.</p>
      </header>

      <div className="search-panel">
        <label className="field grow">
          <span>Keywords</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="விடுதலை, freedom, பெண்…"
            autoFocus
          />
        </label>
        <label className="field">
          <span>Match</span>
          <select
            value={match}
            onChange={(event) => {
              const next = new URLSearchParams(params)
              next.set('match', event.target.value)
              update(next)
            }}
          >
            <option value="any">Any keyword</option>
            <option value="all">All keywords</option>
          </select>
        </label>
      </div>

      <div className="filters">
        <div className="chip-row">
          {KIND_ORDER.map((kind) => (
            <button
              key={kind}
              type="button"
              className={kinds.includes(kind) ? 'chip active' : 'chip'}
              onClick={() => toggle('kind', kind)}
            >
              {kindLabel(kind)}
            </button>
          ))}
        </div>
        <div className="chip-row">
          {Object.entries(THEME_LABELS).map(([theme, label]) => (
            <button
              key={theme}
              type="button"
              className={themes.includes(theme) ? 'chip active' : 'chip'}
              onClick={() => toggle('theme', theme)}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {error ? <p className="error">{error}</p> : null}
      {loading ? <p className="muted">Loading…</p> : null}

      {!loading && !error ? (
        <>
          {query || kinds.length || themes.length ? (
            <p className="muted">
              {hits.length} matches · {match === 'all' ? 'all keywords' : 'any keyword'}
            </p>
          ) : (
            <p className="muted">Type a Tamil or English keyword to search the shelf.</p>
          )}
          {suggestions.length ? (
            <div className="chip-row">
              {suggestions.map(([label, token]) => (
                <Link
                  key={token}
                  className="chip"
                  to={`/search?q=${encodeURIComponent(`${query} ${token}`.trim())}`}
                >
                  {label}
                </Link>
              ))}
            </div>
          ) : null}
          {hits.length ? (
            <div className="tile-grid">
              {hits.map((hit) => (
                <WorkTile
                  key={hit.work.id}
                  work={hit.work}
                  snippet={hit.snippet.replace(/\*\*/g, '')}
                />
              ))}
            </div>
          ) : query || kinds.length || themes.length ? (
            <p className="muted">Try a shorter Tamil stem, switch to Any keyword, or clear a theme.</p>
          ) : (
            <div className="chip-row">
              {['விடுதலை', 'பெண்', 'தமிழ்', 'அச்சமில்லை'].map((token) => (
                <Link key={token} className="chip" to={`/search?q=${encodeURIComponent(token)}`}>
                  {token}
                </Link>
              ))}
            </div>
          )}
        </>
      ) : null}
    </PageMotion>
  )
}
