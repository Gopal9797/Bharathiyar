import { expect, test } from '@playwright/test'
import { waitForShelf } from './helpers'

test('search idle state invites a query instead of a false zero-match', async ({ page }) => {
  await page.goto('search', { waitUntil: 'networkidle' })
  await waitForShelf(page)
  await expect(page.getByText('Type a Tamil or English keyword to search the shelf.')).toBeVisible()
  await expect(page.getByText(/^0 matches/)).toHaveCount(0)
})

test('explore shows an empty-state when filters exclude everything', async ({ page }) => {
  await page.goto('explore', { waitUntil: 'networkidle' })
  await waitForShelf(page)
  await page.getByRole('button', { name: /Speech/ }).click()
  await page.locator('select').selectOption({ label: 'கண்ணன் பாட்டு' })
  await expect(page.getByText(/No works match these filters/)).toBeVisible()
})

test('books page lists every biography panel', async ({ page }) => {
  await page.goto('books', { waitUntil: 'networkidle' })
  await waitForShelf(page)
  await expect(page.locator('.panel')).toHaveCount(5)
  await expect(page.getByText('பாரதியார் சரித்திரம்')).toBeVisible()
})
