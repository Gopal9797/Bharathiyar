import {
  THEME_LABELS,
  THEME_STEMS,
  themeLabels,
  type Hit,
  type Work,
} from './catalog'

function tokens(query: string): string[] {
  return query
    .trim()
    .split(/[\s,;|/]+/)
    .filter((part) => {
      if (!part) return false
      if (/^[\x00-\x7F]+$/.test(part) && part.length < 3) return false
      return true
    })
}

function expansions(token: string): readonly string[] {
  const folded = token.toLowerCase()
  for (const stems of Object.values(THEME_STEMS)) {
    if (stems.some((stem) => stem.toLowerCase() === folded)) return stems
  }
  return [token]
}

function isAscii(value: string): boolean {
  return /^[\x00-\x7F]*$/.test(value)
}

function contains(haystack: string, needle: string): boolean {
  if (!needle) return false
  if (isAscii(needle)) {
    const pattern = new RegExp(`(?<![A-Za-z0-9])${escapeRegExp(needle)}`, 'i')
    return pattern.test(haystack)
  }
  const pattern = new RegExp(`(?<![\\u0b80-\\u0bff])${escapeRegExp(needle)}`)
  return pattern.test(haystack)
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function emphasize(text: string, needle: string): string {
  const safe = text.replace(/[*_`]/g, '')
  if (isAscii(needle)) {
    return safe.replace(new RegExp(escapeRegExp(needle), 'i'), (match) => `**${match}**`)
  }
  if (safe.includes(needle)) return safe.replace(needle, `**${needle}**`)
  return safe
}

function snippet(work: Work, needles: string[]): string {
  const flat = work.text.replace(/\s+/g, ' ').trim()
  if (!flat) return work.english_title || work.collection
  const folded = flat.toLowerCase()
  let at = -1
  let found = ''
  for (const needle of needles) {
    if (!needle) continue
    const spot = isAscii(needle) ? folded.indexOf(needle.toLowerCase()) : flat.indexOf(needle)
    if (spot >= 0 && (at < 0 || spot < at)) {
      at = spot
      found = needle
    }
  }
  let window: string
  if (at < 0) {
    window = flat.slice(0, 220)
  } else {
    const start = Math.max(0, at - 70)
    const end = Math.min(flat.length, at + 150)
    window = flat.slice(start, end)
    if (start > 0) window = `…${window}`
    if (end < flat.length) window = `${window}…`
  }
  return found ? emphasize(window, found) : window
}

function bestNeedle(
  titleBlob: string,
  themeBlob: string,
  body: string,
  expansionList: readonly string[],
): [number, string | null] {
  for (const needle of expansionList) {
    if (contains(titleBlob, needle)) return [8, needle]
  }
  for (const needle of expansionList) {
    if (contains(themeBlob, needle)) return [3, needle]
  }
  for (const needle of expansionList) {
    if (contains(body, needle)) return [1, needle]
  }
  return [0, null]
}

export type SearchOptions = {
  match?: 'any' | 'all'
  kinds?: string[]
  themes?: string[]
  collection?: string | null
}

export function search(works: Work[], query = '', options: SearchOptions = {}): Hit[] {
  const selectedKinds = new Set(options.kinds ?? [])
  const selectedThemes = new Set(options.themes ?? [])
  const collection = options.collection ?? null
  const match = options.match ?? 'any'
  const queryTokens = tokens(query)
  const phrase = queryTokens.join(' ')
  const hits: Hit[] = []

  for (const work of works) {
    if (selectedKinds.size && !selectedKinds.has(work.kind)) continue
    if (collection && work.collection !== collection) continue
    if (selectedThemes.size && !work.themes.some((theme) => selectedThemes.has(theme))) {
      continue
    }

    const titleBlob = `${work.title}\n${work.english_title}`
    const themeBlob = [...themeLabels(work.themes), ...work.themes].join(' ')
    let score = 0
    const matchedNeedles: string[] = []
    let tokenHits = 0

    for (const token of queryTokens) {
      const [weight, needle] = bestNeedle(
        titleBlob,
        themeBlob,
        work.text,
        expansions(token),
      )
      if (weight) {
        tokenHits += 1
        score += weight
        if (needle) matchedNeedles.push(needle)
      }
    }

    if (queryTokens.length && match === 'all' && tokenHits < queryTokens.length) continue
    if (queryTokens.length && match !== 'all' && tokenHits === 0) continue
    if (
      phrase &&
      queryTokens.length > 1 &&
      contains(`${titleBlob}\n${work.text}`, phrase)
    ) {
      score += 3
    }
    if (
      !queryTokens.length &&
      !selectedKinds.size &&
      !selectedThemes.size &&
      !collection
    ) {
      continue
    }

    hits.push({
      work,
      score,
      snippet: snippet(work, matchedNeedles),
    })
  }

  const kindRank: Record<string, number> = {
    poem: 0,
    speech: 1,
    story: 2,
    life: 3,
    article: 4,
  }
  hits.sort(
    (a, b) =>
      b.score - a.score ||
      (kindRank[a.work.kind] ?? 9) - (kindRank[b.work.kind] ?? 9) ||
      a.work.title.localeCompare(b.work.title, 'ta'),
  )
  return hits
}

export function relatedWorks(works: Work[], work: Work, limit = 3): Work[] {
  const themes = new Set(work.themes)
  const ranked: Array<[number, string, Work]> = []
  for (const other of works) {
    if (other.id === work.id) continue
    const overlap = other.themes.filter((theme) => themes.has(theme)).length
    const sameKind = other.kind === work.kind ? 1 : 0
    if (overlap === 0 && other.collection !== work.collection) continue
    const sameCollection = other.collection === work.collection ? 3 : 0
    ranked.push([overlap * 2 + sameCollection + sameKind, other.title, other])
  }
  ranked.sort((a, b) => b[0] - a[0] || a[1].localeCompare(b[1], 'ta'))
  return ranked.slice(0, limit).map((item) => item[2])
}

export function relatedKeywords(
  hits: Hit[],
  query: string,
  limit = 8,
): Array<[string, string]> {
  const used = new Set(tokens(query).map((token) => token.toLowerCase()))
  const counts: Record<string, number> = {}
  for (const hit of hits) {
    for (const theme of hit.work.themes) {
      counts[theme] = (counts[theme] ?? 0) + 1
    }
  }
  const ranked = Object.keys(counts).sort(
    (a, b) => counts[b] - counts[a] || a.localeCompare(b),
  )
  const suggestions: Array<[string, string]> = []
  for (const theme of ranked) {
    const stems = THEME_STEMS[theme]
    if (!stems) continue
    const tamil = stems.find((stem) => !isAscii(stem)) ?? stems[0]
    if (used.has(tamil.toLowerCase()) || used.has(theme.toLowerCase())) continue
    if (stems.some((stem) => used.has(stem.toLowerCase()))) continue
    suggestions.push([THEME_LABELS[theme], tamil])
    if (suggestions.length >= limit) break
  }
  return suggestions
}

export function workById(works: Work[], id: string): Work | undefined {
  return works.find((work) => work.id === id)
}
