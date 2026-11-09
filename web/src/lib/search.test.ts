import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import type { Work } from './catalog'
import { search } from './search'

const works = JSON.parse(
  readFileSync(resolve(process.cwd(), 'public/data/works.json'), 'utf8'),
) as Work[]

describe('search archive', () => {
  it('loads more than 200 works', () => {
    expect(works.length).toBeGreaterThan(200)
  })

  it('finds செந்தமிழ் நாடு', () => {
    const hits = search(works, 'செந்தமிழ்')
    expect(hits.some((hit) => hit.work.title === 'செந்தமிழ் நாடு')).toBe(true)
  })

  it('keeps exactly one Islam speech summary', () => {
    const speeches = works.filter(
      (work) => work.kind === 'speech' && work.title.includes('இஸ்லாம்'),
    )
    expect(speeches).toHaveLength(1)
  })

  it('expands freedom to Tamil stems', () => {
    const hits = search(works, 'freedom')
    expect(hits.length).toBeGreaterThan(0)
  })

  it('matches பெண் at word start', () => {
    const hits = search(works, 'பெண்')
    expect(hits.length).toBeGreaterThan(0)
    expect(hits.some((hit) => /(?<![\u0b80-\u0bff])பெண்/.test(hit.work.text + hit.work.title))).toBe(
      true,
    )
  })
})
