const assert = require('node:assert/strict');
const {withBrowser} = require('./browser');
const {data, today, select} = require('./oracle');

withBrowser(async browser => {
  const context = await browser.newContext({timezoneId: 'Asia/Tokyo'});
  const response = await context.request.get('https://sakimyto.github.io/tokyo-date-spots/spots.json');
  assert.equal(response.status(), 200, '公開JSON HTTP 200');
  assert.deepEqual(await response.json(), data, '公開JSONとローカルの全行一致');
  const page = await context.newPage();
  const errors = [], external = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => {if (message.type() === 'error') errors.push(message.text());});
  page.on('request', request => {
    if (!request.isNavigationRequest()) external.push(request.url());
  });
  await page.clock.setFixedTime(new Date(today + 'T12:00:00+09:00'));
  const html = await page.goto('https://sakimyto.github.io/tokyo-date-spots/#g='+encodeURIComponent('すべて'));
  assert.equal(html.status(), 200, '公開ページ HTTP 200');
  assert.equal(await page.locator('article').count(), select(data, today).length);
  await page.click('#fRain');
  assert.equal(await page.locator('article').count(), select(data, today, {rain: true}).length);
  assert.deepEqual(errors, []);
  assert.deepEqual(external, []);
  await context.close();
  console.log(JSON.stringify({http: 200, rows: data.length, exactMatch: true, errors: 0, external: 0}));
}).catch(error => {console.error(error); process.exitCode = 1;});
