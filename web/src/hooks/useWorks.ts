import { useEffect, useState } from 'react'
import { dataUrl, type Work } from '../lib/catalog'

type WorksState = {
  works: Work[]
  loading: boolean
  error: string | null
}

let cached: Work[] | null = null
let pending: Promise<Work[]> | null = null

async function loadWorks(): Promise<Work[]> {
  if (cached) return cached
  if (!pending) {
    pending = fetch(dataUrl('works.json'))
      .then(async (response) => {
        if (!response.ok) throw new Error(`Could not load works (${response.status})`)
        const payload = (await response.json()) as Work[]
        cached = payload
        return payload
      })
      .finally(() => {
        pending = null
      })
  }
  return pending
}

export function useWorks(): WorksState {
  const [works, setWorks] = useState<Work[]>(cached ?? [])
  const [loading, setLoading] = useState(!cached)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let alive = true
    loadWorks()
      .then((payload) => {
        if (!alive) return
        setWorks(payload)
        setLoading(false)
      })
      .catch((err: unknown) => {
        if (!alive) return
        setError(err instanceof Error ? err.message : 'Could not load works')
        setLoading(false)
      })
    return () => {
      alive = false
    }
  }, [])

  return { works, loading, error }
}
