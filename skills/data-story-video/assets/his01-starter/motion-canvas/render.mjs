import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createServer} from 'vite';
import {chromium} from 'playwright';

const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
const server = await createServer({configFile: path.join(root, 'vite.config.ts')});
let browser;
try {
  await server.listen();
  const port = server.httpServer.address().port;
  browser = await chromium.launch({headless: true});
  const page = await browser.newPage();
  page.on('pageerror', error => console.error(error.message));
  await page.goto(`http://127.0.0.1:${port}/render.html`);
  await page.locator('#render').waitFor();
  await page.waitForFunction(() => document.querySelector('#status')?.textContent === 'READY', null, {timeout: 120000});
  await page.locator('#render').click();
  await page.waitForFunction(() => /^(COMPLETE|FAILED)/.test(document.querySelector('#status')?.textContent ?? ''), null, {timeout: 300000});
  const result = await page.locator('#status').textContent();
  if (result !== 'COMPLETE') throw new Error(result);
  console.log('Chart rendered: ../charts/DEMO.mp4');
} finally {
  await browser?.close();
  await server.close();
}
