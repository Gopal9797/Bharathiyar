import { Link } from 'react-router-dom'
import { PageMotion } from '../components/PageMotion'
import { BOOKS, EVENTS, SPEECHES } from '../data/life'
import { useWorks } from '../hooks/useWorks'
import { KIND_ORDER } from '../lib/catalog'

export function About() {
  const { works, loading } = useWorks()
  const counts = Object.fromEntries(
    KIND_ORDER.map((kind) => [kind, works.filter((work) => work.kind === kind).length]),
  )
  const sources = new Map<string, string>()
  for (const work of works) {
    if (work.source_url && !sources.has(work.source_url)) {
      sources.set(work.source_url, work.source)
    }
  }

  return (
    <PageMotion>
      <header className="page-head">
        <p className="eyebrow">Context</p>
        <h1>About</h1>
        <p>
          Subramania Bharati (1882–1921), known in Tamil as Bharathiyar, wrote poems,
          songs, essays, and stories for the freedom movement, for women&apos;s
          emancipation, against caste, and in devotion. The Madras government
          nationalised his writings in 1949. They are in the public domain.
        </p>
      </header>

      <section className="section">
        <div className="section-head">
          <h2>Life</h2>
        </div>
        <ol className="timeline">
          {EVENTS.map(([year, detail]) => (
            <li key={year}>
              <strong>{year}.</strong> {detail}
            </li>
          ))}
        </ol>
        <p>
          <Link className="text-link" to="/read/songs-037">
            Read his own account, கனவு
          </Link>
        </p>
      </section>

      <section className="section">
        <div className="section-head">
          <h2>Speeches</h2>
          <p>
            This shelf prints one speech summary from 1920 and his own Erode account
            from Swadesamitran, 4 August 1921.
          </p>
        </div>
        <div className="stack">
          {SPEECHES.map((speech) => (
            <article key={speech.title} className="panel">
              <h3>{speech.title}</h3>
              <p className="collection">{speech.when}</p>
              <p>{speech.about}</p>
            </article>
          ))}
        </div>
        <div className="cta-row">
          <Link className="button ghost" to="/read/essays-049">
            Printed speech summary
          </Link>
          <Link className="button ghost" to="/read/erode-001">
            Erode account
          </Link>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2>What is on this shelf</h2>
        </div>
        {loading ? (
          <p className="muted">Counting…</p>
        ) : (
          <p>
            This shelf holds {works.length} pieces. {counts.poem} are poems,{' '}
            {counts.article} are articles, {counts.story} are stories, {counts.speech}{' '}
            is the printed speech summary, and {counts.life} are pieces of life writing.
            English lines under a title are short glosses, not verse translations. The{' '}
            {BOOKS.length} biographies on Books stay as names and notes only.
          </p>
        )}
      </section>

      <section className="section">
        <div className="section-head">
          <h2>Sources</h2>
          <p>
            Project Madurai Unicode editions may be shared when their acknowledgement
            stays with them.
          </p>
        </div>
        <ul className="source-list">
          {[...sources.entries()].map(([url, label]) => (
            <li key={url}>
              <a href={url} target="_blank" rel="noreferrer">
                {label}
              </a>
            </li>
          ))}
        </ul>
      </section>
    </PageMotion>
  )
}
