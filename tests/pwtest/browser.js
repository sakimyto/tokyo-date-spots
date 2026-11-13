const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {chromium} = require('playwright-core');
const BASE = path.join(os.homedir(), '_pjsc/_work/ai-browser');

function executable() {
  if (process.env.CHROME_PATH) {
    const real = fs.realpathSync(process.env.CHROME_PATH);
    if (!real.startsWith(fs.realpathSync(BASE) + path.sep)
        || !real.endsWith('/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing')) {
      throw new Error('CHROME_PATHはAI専用Chrome for Testingを指定してください');
    }
    return real;
  }
  const browsers = path.join(BASE, 'browsers');
  for (const version of fs.readdirSync(browsers).filter(name => /^chromium-\d+$/.test(name)).sort().reverse()) {
    const candidate = path.join(browsers, version,
      'chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing');
    if (fs.existsSync(candidate)) return candidate;
  }
  throw new Error('AI専用Chrome for Testingがありません。PUBLISH.mdを参照してください');
}

async function withBrowser(run) {
  const scratch = path.join(BASE, 'tokyo-date-spots-tests');
  fs.mkdirSync(scratch, {recursive: true});
  const session = fs.mkdtempSync(path.join(scratch, 'run-'));
  // Playwrightが作る一時プロファイル・ログも/tmpへ置かない。
  const previousTemp = process.env.TMPDIR;
  process.env.TMPDIR = session;
  let browser;
  try {
    browser = await chromium.launch({executablePath: executable(), headless: true,
      env: {...process.env, TMPDIR: session}, artifactsDir: session});
    return await run(browser);
  } finally {
    try { if (browser) await browser.close(); }
    finally {
      if (previousTemp === undefined) delete process.env.TMPDIR;
      else process.env.TMPDIR = previousTemp;
      fs.rmSync(session, {recursive: true, force: true});
    }
  }
}

module.exports = {withBrowser};
