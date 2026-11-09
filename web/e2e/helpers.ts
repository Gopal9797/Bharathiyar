import { expect, type ConsoleMessage, type Page, type Response } from '@playwright/test'

export type CrawlIssue = {
  kind: 'console' | 'pageerror' | 'requestfailed' | 'badstatus' | 'empty' | 'scroll' | 'broken-image'
  message: string
  url?: string
}

export function attachIssueCollectors(page: Page) {
  const issues: CrawlIssue[] = []

  page.on('console', (msg: ConsoleMessage) => {
    if (msg.type() === 'error') {
      issues.push({
        kind: 'console',
        message: msg.text(),
        url: page.url(),
      })
    }
  })

  page.on('pageerror', (error) => {
    issues.push({
      kind: 'pageerror',
      message: error.message,
      url: page.url(),
    })
  })

  page.on('requestfailed', (request) => {
    const failure = request.failure()?.errorText ?? 'unknown'
    if (failure.includes('ERR_ABORTED')) return
    issues.push({
      kind: 'requestfailed',
      message: `${request.url()} :: ${failure}`,
      url: page.url(),
    })
  })

  page.on('response', (response: Response) => {
    const status = response.status()
    const url = response.url()
    // YouTube embed chrome often 403/404s in headless; ignore third-party noise.
    if (url.includes('youtube.com') || url.includes('googlevideo.com') || url.includes('google.com')) {
      return
    }
    if (status >= 400) {
      issues.push({
        kind: 'badstatus',
        message: `${status} ${url}`,
        url: page.url(),
      })
    }
  })

  return issues
}

export async function waitForShelf(page: Page) {
  await page.waitForLoadState('domcontentloaded')
  await expect(page.locator('.brand-name')).toHaveText('Bharathiyar', { timeout: 15_000 })
  const loading = page.getByText(/Loading( the shelf)?…/)
  if (await loading.count()) {
    await expect(loading).toHaveCount(0, { timeout: 30_000 })
  }
}

export async function assertNoBrokenImages(page: Page, issues: CrawlIssue[]) {
  const broken = await page.evaluate(() =>
    [...document.images]
      .filter((img) => !img.closest('iframe'))
      .filter((img) => img.complete && (img.naturalWidth === 0 || img.naturalHeight === 0))
      .map((img) => img.currentSrc || img.src || img.alt || 'unknown image'),
  )
  for (const src of broken) {
    issues.push({
      kind: 'broken-image',
      message: src,
      url: page.url(),
    })
  }
}

export async function assertScrolledToTop(page: Page, issues: CrawlIssue[]) {
  const y = await page.evaluate(() => window.scrollY || document.documentElement.scrollTop)
  if (y > 2) {
    issues.push({
      kind: 'scroll',
      message: `expected top, got scrollY=${y}`,
      url: page.url(),
    })
  }
}

export function formatIssues(issues: CrawlIssue[]): string {
  if (!issues.length) return 'no issues'
  return issues.map((issue) => `[${issue.kind}] ${issue.message} @ ${issue.url ?? ''}`).join('\n')
}

/** Relative to baseURL (.../Bharathiyar/). Do not prefix with '/'. */
export const STATIC_ROUTES = [
  './',
  'explore',
  'search',
  'search?q=%E0%AE%B5%E0%AE%BF%E0%AE%9F%E0%AF%81%E0%AE%A4%E0%AE%B2%E0%AF%88',
  'visuals',
  'films',
  'books',
  'about',
] as const
