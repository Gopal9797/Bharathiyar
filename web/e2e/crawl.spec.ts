import { expect, test } from '@playwright/test'
import {
  STATIC_ROUTES,
  assertNoBrokenImages,
  assertScrolledToTop,
  attachIssueCollectors,
  formatIssues,
  waitForShelf,
} from './helpers'

test.describe('site crawl', () => {
  test('visits every primary route without runtime failures', async ({ page }) => {
    const issues = attachIssueCollectors(page)

    for (const route of STATIC_ROUTES) {
      await page.goto(route, { waitUntil: 'networkidle' })
      await waitForShelf(page)
      await expect(page.locator('main')).not.toBeEmpty()
      await assertNoBrokenImages(page, issues)
      await assertScrolledToTop(page, issues)
    }

    expect(issues, formatIssues(issues)).toEqual([])
  })

  test('nav links all resolve and keep brand chrome', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    await page.goto('./', { waitUntil: 'networkidle' })
    await waitForShelf(page)

    const labels = ['Home', 'Explore', 'Search', 'Visuals', 'Films', 'Books', 'About']
    for (const label of labels) {
      await page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: label }).click()
      await waitForShelf(page)
      await expect(page.locator('main h1')).toBeVisible()
      await assertScrolledToTop(page, issues)
    }

    expect(issues, formatIssues(issues)).toEqual([])
  })

  test('opens featured works and lands at the top of the reader', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    await page.goto('./', { waitUntil: 'networkidle' })
    await waitForShelf(page)

    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
    await expect.poll(async () => page.evaluate(() => window.scrollY)).toBeGreaterThan(100)

    const firstRead = page.locator('.tile-grid .work-tile a.text-link').first()
    await firstRead.click()
    await waitForShelf(page)
    await expect(page).toHaveURL(/\/read\//)
    await expect(page.locator('.reader')).toBeVisible()
    await assertScrolledToTop(page, issues)
    await assertNoBrokenImages(page, issues)

    expect(issues, formatIssues(issues)).toEqual([])
  })

  test('search returns matches and each result opens a readable work', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    const searchUrl = 'search?q=%E0%AE%85%E0%AE%9A%E0%AF%8D%E0%AE%9A%E0%AE%AE%E0%AF%8D'
    await page.goto(searchUrl, { waitUntil: 'networkidle' })
    await waitForShelf(page)
    await expect(page.getByText(/matches/)).toBeVisible()

    const resultLinks = page.locator('.tile-grid .work-tile h3 a')
    const count = await resultLinks.count()
    expect(count).toBeGreaterThan(0)

    const sample = Math.min(count, 5)
    for (let index = 0; index < sample; index += 1) {
      await page.goto(searchUrl, { waitUntil: 'networkidle' })
      await waitForShelf(page)
      const link = page.locator('.tile-grid .work-tile h3 a').nth(index)
      const title = (await link.innerText()).trim()
      await link.click()
      await waitForShelf(page)
      await expect(page).toHaveURL(/\/read\//)
      await expect(page.locator('main h1')).toContainText(title)
      await expect(page.locator('.reader')).toBeVisible()
      await assertScrolledToTop(page, issues)
    }

    expect(issues, formatIssues(issues)).toEqual([])
  })

  test('explore filters change the shelf without emptying chrome', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    await page.goto('explore', { waitUntil: 'networkidle' })
    await waitForShelf(page)

    await page.getByRole('button', { name: /Story/ }).click()
    await expect(page.getByText(/matches|works/)).toBeVisible()
    await expect(page.locator('.work-tile').first()).toBeVisible()

    const collection = page.locator('select')
    const optionCount = await collection.locator('option').count()
    expect(optionCount).toBeGreaterThan(1)
    await collection.selectOption({ index: 1 })
    await expect(page.locator('main')).toBeVisible()

    expect(issues, formatIssues(issues)).toEqual([])
  })

  test('films page embeds a player and keeps external youtube link', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    await page.goto('films', { waitUntil: 'networkidle' })
    await waitForShelf(page)
    await expect(page.locator('iframe')).toBeVisible()
    await expect(page.getByRole('link', { name: 'Open on YouTube' })).toHaveAttribute(
      'href',
      /youtube\.com/,
    )
    const serious = issues.filter((issue) => issue.kind === 'pageerror' || issue.kind === 'broken-image')
    expect(serious, formatIssues(serious)).toEqual([])
  })

  test('visuals show modern and archive art with valid images', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    await page.goto('visuals', { waitUntil: 'networkidle' })
    await waitForShelf(page)
    await expect(page.getByRole('heading', { name: 'Modern art' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Archive' })).toBeVisible()
    await expect(page.locator('.visual-frame img')).toHaveCount(7)
    await assertNoBrokenImages(page, issues)
    expect(issues, formatIssues(issues)).toEqual([])
  })

  test('about lists sources and speech deep links work', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    await page.goto('about', { waitUntil: 'networkidle' })
    await waitForShelf(page)
    await expect(page.getByRole('heading', { name: 'Speeches', exact: true })).toBeVisible()
    await expect(page.locator('.source-list li')).not.toHaveCount(0)

    await page.getByRole('link', { name: 'Erode account' }).click()
    await waitForShelf(page)
    await expect(page).toHaveURL(/erode-001/)
    await expect(page.locator('main h1')).toContainText('ஈரோடு')
    await assertScrolledToTop(page, issues)

    expect(issues, formatIssues(issues)).toEqual([])
  })

  test('crawls internal links discovered from the home page', async ({ page }) => {
    const issues = attachIssueCollectors(page)
    await page.goto('./', { waitUntil: 'networkidle' })
    await waitForShelf(page)

    const hrefs = await page.evaluate(() => {
      const origin = window.location.origin
      const prefix = `${origin}/Bharathiyar/`
      return [...document.querySelectorAll('a[href]')]
        .map((anchor) => (anchor as HTMLAnchorElement).href)
        .filter((href) => href.startsWith(prefix))
    })

    const unique = [...new Set(hrefs)].slice(0, 40)
    expect(unique.length).toBeGreaterThan(5)

    for (const href of unique) {
      const response = await page.goto(href, { waitUntil: 'domcontentloaded' })
      expect(response?.ok() ?? true, `failed ${href}`).toBeTruthy()
      await waitForShelf(page)
      await assertNoBrokenImages(page, issues)
    }

    const serious = issues.filter(
      (issue) =>
        issue.kind === 'pageerror' ||
        issue.kind === 'broken-image' ||
        issue.kind === 'badstatus' ||
        (issue.kind === 'console' && !/youtube|googlevideo|gtm|googleapis/i.test(issue.message)),
    )
    expect(serious, formatIssues(serious)).toEqual([])
  })
})
