import { PageMotion } from '../components/PageMotion'
import { BOOKS } from '../data/life'

export function Books() {
  return (
    <PageMotion>
      <header className="page-head">
        <p className="eyebrow">Lives of Bharati</p>
        <h1>Books</h1>
        <p>
          Published biographies by his wife, a friend, and later scholars. They do not
          reprint here; the titles and short notes stay.
        </p>
      </header>

      <div className="stack">
        {BOOKS.map((book) => (
          <article key={book.title} className="panel">
            <h2>{book.title}</h2>
            <p className="gloss">{book.english}</p>
            <p className="collection">{book.author}</p>
            <p>{book.about}</p>
          </article>
        ))}
      </div>
    </PageMotion>
  )
}
