import { expect, test } from '@playwright/test'
import { waitForShelf } from './helpers'

test('home metrics load from the catalog', async ({ page }) => {
  await page.goto('./', { waitUntil: 'networkidle' })
  await waitForShelf(page)
  await expect(page.getByRole('heading', { name: 'Bharathiyar' })).toBeVisible()
  const worksMetric = page.locator('.metrics .metric-value').first()
  await expect(worksMetric).toHaveText(/^\d{3,}$/)
  const count = Number(await worksMetric.innerText())
  expect(count).toBeGreaterThan(200)
})

test('unknown read id shows not-found state', async ({ page }) => {
  await page.goto('read/does-not-exist', { waitUntil: 'networkidle' })
  await waitForShelf(page)
  await expect(page.getByRole('heading', { name: 'Work not found' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Back to Explore' })).toBeVisible()
})
