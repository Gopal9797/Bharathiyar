import { motion } from 'framer-motion'
import { PageMotion } from '../components/PageMotion'
import { PICTURES } from '../data/media'
import { assetUrl } from '../lib/catalog'

export function Visuals() {
  const modern = PICTURES.filter((picture) => picture.modern)
  const archive = PICTURES.filter((picture) => !picture.modern)

  return (
    <PageMotion>
      <header className="page-head">
        <p className="eyebrow">Look</p>
        <h1>Visuals</h1>
        <p>Modern licensed art beside the historical portraits and stamp.</p>
      </header>

      <section className="section">
        <div className="section-head">
          <h2>Modern art</h2>
          <p>Verified Wikimedia files with Creative Commons or public-domain licenses.</p>
        </div>
        <div className="visual-grid">
          {modern.map((picture, index) => (
            <motion.figure
              key={picture.file}
              className="visual-frame"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ delay: index * 0.08 }}
            >
              <img src={assetUrl(picture.file)} alt={picture.alt} />
              <figcaption>{picture.caption}</figcaption>
            </motion.figure>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2>Archive</h2>
          <p>Portraits, the 1921 photograph, the 1960 stamp, and his signature.</p>
        </div>
        <div className="visual-grid">
          {archive.map((picture) => (
            <figure key={picture.file} className="visual-frame">
              <img src={assetUrl(picture.file)} alt={picture.alt} />
              <figcaption>{picture.caption}</figcaption>
            </figure>
          ))}
        </div>
      </section>
    </PageMotion>
  )
}
