const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {withBrowser} = require('./browser');
const {data, html, today, select, futureDate} = require('./oracle');

withBrowser(async browser => {
  const base = path.join(os.homedir(), '_pjsc/_work/date-spots-migrate-1113');
  fs.mkdirSync(base, {recursive: true});
  const scratch = fs.mkdtempSync(path.join(base, 'ui-mutations-'));
  const detected = [];
  const cases = [
    {name: 'NO_EXPIRED', before: '(st.ended||!isEnded(d,t))', after: 'true',
      date: futureDate(today), filters: {}},
    {name: 'EXCLUSIVE', before: 'if(st.now)st.soon=false;', after: '',
      date: today, filters: {now: true}, click: true},
  ];
  try {
    for (const variant of cases) {
      assert.ok(html.includes(variant.before), '変種の対象が実装に存在する');
      const file = path.join(scratch, variant.name + '.html');
      fs.writeFileSync(file, html.replace(variant.before, variant.after));
      const context = await browser.newContext({timezoneId: 'Asia/Tokyo'});
      try {
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        await page.clock.setFixedTime(new Date(variant.date + 'T12:00:00+09:00'));
        await page.goto(pathToFileURL(file).href + '#g=' + encodeURIComponent('すべて'));
        if (variant.click) {await page.click('#fSoon'); await page.click('#fNow');}
        const actual = await page.locator('article').evaluateAll(items => items.map(item => Number(item.dataset.id)));
        const expected = select(data, variant.date, variant.filters);
        assert.deepEqual(errors, [], '構文・起動エラーではない');
        assert.throws(() => assert.deepEqual(actual, expected), assert.AssertionError,
          variant.name + 'が行集合の不一致として検出される');
        detected.push(variant.name);
      } finally {await context.close();}
    }
    console.log(JSON.stringify({brokenVariantsDetected: detected}));
  } finally {fs.rmSync(scratch, {recursive: true, force: true});}
}).catch(error => {console.error(error); process.exitCode = 1;});
