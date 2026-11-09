export type Work = {
  id: string
  title: string
  english_title: string
  kind: string
  collection: string
  themes: string[]
  text: string
  note: string
  source: string
  source_url: string
}

export type Hit = {
  work: Work
  score: number
  snippet: string
}

export const KIND_LABELS: Record<string, string> = {
  poem: 'Poem · பாடல்',
  article: 'Article · கட்டுரை',
  story: 'Story · கதை',
  speech: 'Speech · உரை',
  life: 'Life · சுயசரிதை',
}

export const KIND_ORDER = ['poem', 'article', 'story', 'speech', 'life'] as const

export const THEME_LABELS: Record<string, string> = {
  freedom: 'Freedom · விடுதலை',
  tamil: 'Tamil · தமிழ்',
  nation: 'Nation · பாரதம்',
  women: 'Women · பெண்',
  courage: 'Courage · வீரம்',
  devotion: 'Devotion · பக்தி',
  education: 'Learning · கல்வி',
  caste: 'Caste · சாதி',
  labor: 'Labor · உழைப்பு',
  leaders: 'Leaders · தலைவர்கள்',
}

export const THEME_STEMS: Record<string, readonly string[]> = {
  freedom: ['சுதந்திர', 'விடுதலை', 'freedom', 'liberty'],
  tamil: ['தமிழ்', 'செந்தமிழ்', 'tamil'],
  nation: ['பாரத', 'தேசிய', 'சுதேச', 'nation', 'india'],
  women: ['பெண்', 'மாதர்', 'விதவை', 'ஸ்திரீ', 'women', 'woman'],
  courage: ['அச்சமில்லை', 'அச்சம்', 'வீரம்', 'தைரியம்', 'courage', 'fearless'],
  devotion: [
    'பக்தி',
    'பராசக்தி',
    'காளி',
    'கண்ணன்',
    'நந்தலாலா',
    'முருகன்',
    'devotion',
    'krishna',
  ],
  education: ['கல்வி', 'பள்ளி', 'சாத்திர', 'education', 'learning'],
  caste: ['சாதி', 'ஜாதி', 'caste'],
  labor: ['உழைப்பு', 'தொழில்', 'வறுமை', 'labor', 'labour', 'poverty'],
  leaders: [
    'திலகர்',
    'காந்தி',
    'லாஜபதி',
    'சிவாஜி',
    'நௌரோஜி',
    'leader',
    'gandhi',
    'tilak',
  ],
}

export function kindLabel(kind: string): string {
  return KIND_LABELS[kind] ?? kind
}

export function themeLabels(themes: string[]): string[] {
  return themes.map((theme) => THEME_LABELS[theme]).filter(Boolean)
}

export function preview(text: string, limit = 180): string {
  const flat = text.replace(/\s+/g, ' ').trim()
  if (flat.length <= limit) return flat
  return `${flat.slice(0, limit - 1).replace(/\s+\S*$/, '')}…`
}

export function assetUrl(file: string): string {
  const base = import.meta.env.BASE_URL
  return `${base}assets/${file}`
}

export function dataUrl(file: string): string {
  const base = import.meta.env.BASE_URL
  return `${base}data/${file}`
}
