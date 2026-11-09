import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { ScrollToTop } from './ScrollToTop'

const LINKS = [
  { to: '/', label: 'Home', end: true },
  { to: '/explore', label: 'Explore' },
  { to: '/search', label: 'Search' },
  { to: '/visuals', label: 'Visuals' },
  { to: '/films', label: 'Films' },
  { to: '/books', label: 'Books' },
  { to: '/about', label: 'About' },
]

export function Layout() {
  const location = useLocation()

  return (
    <div className="shell">
      <ScrollToTop />
      <div className="atmosphere" aria-hidden="true" />
      <header className="topbar">
        <NavLink to="/" className="brand" end>
          <span className="brand-mark">B</span>
          <span className="brand-name">Bharathiyar</span>
        </NavLink>
        <nav className="nav" aria-label="Primary">
          {LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="main">
        <AnimatePresence mode="wait">
          <Outlet key={location.pathname} />
        </AnimatePresence>
      </main>
      <footer className="site-footer">
        <p>
          His writings are in the public domain. Project Madurai editions stay with
          their acknowledgement. English under titles are short glosses, not verse
          translations.
        </p>
      </footer>
    </div>
  )
}
