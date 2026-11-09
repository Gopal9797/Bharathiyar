import { copyFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const dest = resolve(root, 'web/public/data/works.json')
mkdirSync(dirname(dest), { recursive: true })
copyFileSync(resolve(root, 'data/works.json'), dest)
console.log('synced data/works.json -> web/public/data/works.json')
