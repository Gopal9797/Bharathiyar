import { useState } from 'react'
import { PageMotion } from '../components/PageMotion'
import { FILMS } from '../data/media'

type Film = (typeof FILMS)[number]

export function Films() {
  const [active, setActive] = useState<Film>(FILMS[0])

  return (
    <PageMotion>
      <header className="page-head">
        <p className="eyebrow">Watch</p>
        <h1>Films</h1>
        <p>The 2000 biographical film, a television promo, and songs from the film.</p>
      </header>

      <label className="field">
        <span>Choose a film or song</span>
        <select
          value={active.id}
          onChange={(event) => {
            const next = FILMS.find((film) => film.id === event.target.value)
            if (next) setActive(next)
          }}
        >
          {FILMS.map((film) => (
            <option key={film.id} value={film.id}>
              {film.title}
            </option>
          ))}
        </select>
      </label>

      <p className="muted">{active.detail}</p>

      <div className="video-frame">
        <iframe
          title={active.title}
          src={`https://www.youtube-nocookie.com/embed/${active.id}`}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>

      <p>
        <a className="button ghost" href={active.url} target="_blank" rel="noreferrer">
          Open on YouTube
        </a>
      </p>
    </PageMotion>
  )
}
