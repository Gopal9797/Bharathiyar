import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { kindLabel, preview, type Work } from '../lib/catalog'

type Props = {
  work: Work
  snippet?: string
}

export function WorkTile({ work, snippet }: Props) {
  return (
    <motion.article
      className="work-tile"
      whileHover={{ y: -4 }}
      transition={{ type: 'spring', stiffness: 360, damping: 24 }}
    >
      <p className="eyebrow">{kindLabel(work.kind)}</p>
      <h3>
        <Link to={`/read/${work.id}`}>{work.title}</Link>
      </h3>
      {work.english_title ? <p className="gloss">{work.english_title}</p> : null}
      {work.collection ? <p className="collection">{work.collection}</p> : null}
      <p className="snippet">{snippet ?? preview(work.text, 140)}</p>
      <Link className="text-link" to={`/read/${work.id}`}>
        Read
      </Link>
    </motion.article>
  )
}

export function renderMarked(snippet: string) {
  const parts = snippet.split(/(\*\*[^*]+\*\*)/g)
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index}>{part.slice(2, -2)}</strong>
    }
    return <span key={index}>{part}</span>
  })
}
