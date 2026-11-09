import { Link, useParams } from 'react-router-dom'
import { PageMotion } from '../components/PageMotion'
import { WorkTile } from '../components/WorkTile'
import { useWorks } from '../hooks/useWorks'
import { kindLabel } from '../lib/catalog'
import { relatedWorks, workById } from '../lib/search'

export function Read() {
  const { id = '' } = useParams()
  const { works, loading, error } = useWorks()
  const work = workById(works, id)
  const related = work ? relatedWorks(works, work) : []

  return (
    <PageMotion>
      {loading ? <p className="muted">Loading…</p> : null}
      {error ? <p className="error">{error}</p> : null}
      {!loading && !work ? (
        <header className="page-head">
          <h1>Work not found</h1>
          <p>
            <Link to="/explore">Back to Explore</Link>
          </p>
        </header>
      ) : null}
      {work ? (
        <>
          <header className="page-head read-head">
            <p className="eyebrow">{kindLabel(work.kind)}</p>
            <h1>{work.title}</h1>
            {work.english_title ? <p className="gloss">{work.english_title}</p> : null}
            {work.collection ? <p className="collection">{work.collection}</p> : null}
            {work.note ? <p className="note">{work.note}</p> : null}
          </header>
          <article className="reader">
            {work.text.split(/\n{2,}/).map((block, index) => (
              <p key={index}>{block}</p>
            ))}
          </article>
          <p className="source-line">
            {work.source}
            {work.source_url ? (
              <>
                {' · '}
                <a href={work.source_url} target="_blank" rel="noreferrer">
                  Source
                </a>
              </>
            ) : null}
          </p>
          {related.length ? (
            <section className="section">
              <div className="section-head">
                <h2>Related</h2>
              </div>
              <div className="tile-grid">
                {related.map((item) => (
                  <WorkTile key={item.id} work={item} />
                ))}
              </div>
            </section>
          ) : null}
        </>
      ) : null}
    </PageMotion>
  )
}
