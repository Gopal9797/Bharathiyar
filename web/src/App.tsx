import { Navigate, Route, Routes } from 'react-router-dom'
import { Layout } from './components/Layout'
import { About } from './pages/About'
import { Books } from './pages/Books'
import { Explore } from './pages/Explore'
import { Films } from './pages/Films'
import { Home } from './pages/Home'
import { Read } from './pages/Read'
import { SearchPage } from './pages/SearchPage'
import { Visuals } from './pages/Visuals'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="explore" element={<Explore />} />
        <Route path="search" element={<SearchPage />} />
        <Route path="read/:id" element={<Read />} />
        <Route path="visuals" element={<Visuals />} />
        <Route path="films" element={<Films />} />
        <Route path="books" element={<Books />} />
        <Route path="about" element={<About />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
