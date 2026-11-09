import { useMemo, useState } from 'react'
import { PageMotion } from '../components/PageMotion'
import { WorkTile } from '../components/WorkTile'
import { useWorks } from '../hooks/useWorks'
import { KIND_ORDER, kindLabel } from '../lib/catalog'
import { search } from '../lib/search'

export function Explore() {
  const { works, loading, error } = useWorks()
  const [kinds, setKinds] = useState<string[]>([])
  const [collection, setCollection] = useState('')

  const collections = useMemo(() => {
    const names = new Set(works.map((work) => work.collection).filter(Boolean))
    return [...names].sort((a, b) => a.localeCompare(b, 'ta'))
  }, [works])

  const hits = useMemo(() => {
    if (!works.length) return []
    if (!kinds.length && !collection) {
      return works.slice(0, 48).map((work) => ({ work, score: 0, snippet: '' }))
    }
    return search(works, '', {
      kinds,
      collection: collection || null,
    })
  }, [works, kinds, collection])

  function toggleKind(kind: string) {
    setKinds((current) =>
      current.includes(kind) ? current.filter((item) => item !== kind) : [...current, kind],
    )
  }

  return (
    <PageMotion>
      <header className="page-head">
        <p className="eyebrow">Library</p>
        <h1>Explore</h1>
        <p>Browse the shelf by kind and collection.</p>
      </header>

      {error ? <p className="error">{error}</p> : null}
      {loading ? <p className="muted">Loading…</p> : null}

      {!loading && !error ? (
        <>
          <div className="filters">
            <div className="chip-row">
              {KIND_ORDER.map((kind) => (
                <button
                  key={kind}
                  type="button"
                  className={kinds.includes(kind) ? 'chip active' : 'chip'}
                  onClick={() => toggleKind(kind)}
                >
                  {kindLabel(kind)}
                </button>
              ))}
            </div>
            <label className="field">
              <span>Collection</span>
              <select value={collection} onChange={(event) => setCollection(event.target.value)}>
                <option value="">All collections</option>
                {collections.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <p className="muted">
            {kinds.length || collection
              ? `${hits.length} matches`
              : `Showing first ${hits.length} of ${works.length} works`}
          </p>

          {hits.length ? (
            <div className="tile-grid">
              {hits.map((hit) => (
                <WorkTile key={hit.work.id} work={hit.work} />
              ))}
            </div>
          ) : (
            <p className="muted">No works match these filters. Clear a kind or pick another collection.</p>
          )}
        </>
      ) : null}
    </PageMotion>
  )
}
