import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { PageMotion } from '../components/PageMotion'
import { WorkTile } from '../components/WorkTile'
import { HERO_ART } from '../data/media'
import { useWorks } from '../hooks/useWorks'
import { KIND_ORDER, assetUrl, kindLabel } from '../lib/catalog'

const FEATURED = [
  'செந்தமிழ் நாடு',
  'அச்சமில்லை',
  'பாப்பாப் பாட்டு',
  'பாரத தேசம்',
  'காணி நிலம் வேண்டும்',
  'பெண் விடுதலை',
]

const LONGER = [
  'விநாயகர் நான்மணிமாலை',
  'என் ஈரோடு யாத்திரை',
]

const KEYWORDS = [
  ['விடுதலை', 'Freedom'],
  ['பெண்', 'Women'],
  ['தமிழ்', 'Tamil'],
  ['சாதி', 'Caste'],
  ['கல்வி', 'Learning'],
] as const

export function Home() {
  const { works, loading, error } = useWorks()
  const counts = Object.fromEntries(
    KIND_ORDER.map((kind) => [kind, works.filter((work) => work.kind === kind).length]),
  )
  const fearless = works.find((work) => work.title === 'அச்சமில்லை')
  const opening =
    fearless?.text
      .split('\n')
      .map((line) => line.trim())
      .find((line) => line && !line.startsWith('(')) ?? 'அச்சமில்லை அச்சமில்லை அச்சமென்ப தில்லையே'

  const featured = FEATURED.map((title) =>
    works.find((work) => work.title === title && work.kind === 'poem'),
  ).filter(Boolean)

  const longer = [
    ...LONGER.map((title) => works.find((work) => work.title === title)),
    ...['கண்ணன் பாட்டு', 'பாஞ்சாலி சபதம்', 'கதைக் கொத்து', 'பகவத் கீதை'].map((needle) =>
      works.find((work) => work.collection.includes(needle)),
    ),
  ].filter(Boolean)

  return (
    <PageMotion>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Mahakavi · 1882–1921</p>
          <motion.h1
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.5 }}
          >
            Bharathiyar
          </motion.h1>
          <motion.blockquote
            className="hero-quote"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.28, duration: 0.55 }}
          >
            {opening}
          </motion.blockquote>
          <p className="hero-sub">அச்சமில்லை · There is no fear</p>
          <div className="cta-row">
            <Link className="button primary" to="/explore">
              Open the shelf
            </Link>
            <Link className="button ghost" to="/search?q=%E0%AE%B5%E0%AE%BF%E0%AE%9F%E0%AF%81%E0%AE%A4%E0%AE%B2%E0%AF%88">
              Search விடுதலை
            </Link>
          </div>
        </div>
        <motion.div
          className="hero-art"
          initial={{ opacity: 0, scale: 1.04 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
        >
          <img
            src={assetUrl(HERO_ART.file)}
            alt={HERO_ART.alt}
            className="hero-image"
          />
          <p className="hero-credit">{HERO_ART.caption}</p>
        </motion.div>
      </section>

      {error ? <p className="error">{error}</p> : null}
      {loading ? <p className="muted">Loading the shelf…</p> : null}

      {!loading && !error ? (
        <>
          <section className="metrics">
            <div>
              <span className="metric-value">{works.length}</span>
              <span className="metric-label">Works</span>
            </div>
            {KIND_ORDER.filter((kind) => kind !== 'life').map((kind) => (
              <div key={kind}>
                <span className="metric-value">{counts[kind]}</span>
                <span className="metric-label">{kindLabel(kind)}</span>
              </div>
            ))}
          </section>

          <section className="section">
            <div className="section-head">
              <h2>Longer works</h2>
              <p>Poems, stories, and his own account of the last journey.</p>
            </div>
            <div className="tile-grid">
              {longer.map((work) => (
                <WorkTile key={work!.id} work={work!} />
              ))}
            </div>
          </section>

          <section className="section">
            <div className="section-head">
              <h2>Open a well-known poem</h2>
              <p>Six pieces people still sing and quote.</p>
            </div>
            <div className="tile-grid">
              {featured.map((work) => (
                <WorkTile key={work!.id} work={work!} />
              ))}
            </div>
          </section>

          <section className="section">
            <div className="section-head">
              <h2>Try a keyword</h2>
              <p>Jump straight into Search.</p>
            </div>
            <div className="chip-row">
              {KEYWORDS.map(([token, label]) => (
                <Link key={token} className="chip" to={`/search?q=${encodeURIComponent(token)}`}>
                  {label}
                </Link>
              ))}
            </div>
          </section>
        </>
      ) : null}
    </PageMotion>
  )
}
