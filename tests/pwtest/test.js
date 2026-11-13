const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {withBrowser} = require('./browser');
const {ROOT, data, today, phase, select, futureDate} = require('./oracle');

let checks = 0;
function ok(condition, message) {
  assert.ok(condition, message);
  checks++;
  console.log('ok -', message);
}
function equal(got, want, message) {
  assert.deepEqual(got, want, message);
  checks++;
  console.log('ok -', message);
}

async function run(browser) {
  const errors = [], external = [];
  const file = pathToFileURL(path.join(ROOT, 'index.html')).href;
  const ctx = await browser.newContext({viewport: {width: 390, height: 844},
    deviceScaleFactor: 2, isMobile: true, hasTouch: true, timezoneId: 'Asia/Tokyo'});
  ctx.on('page', page => {
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  });
  ctx.on('request', request => { if (!request.url().startsWith('file:')) external.push(request.url()); });
  // 外部通信が混ざった場合は到達前に拒否し、最後にテストを失敗させる。
  await ctx.route(/^https?:/, route => route.abort());
  async function pageAt(date, hash = '') {
    const page = await ctx.newPage();
    await page.clock.setFixedTime(new Date(date + 'T12:00:00+09:00'));
    await page.goto(file + hash);
    return page;
  }
  const page = await pageAt(today);
  async function tab(genre) {
    await page.locator(`#tabs button[data-g=${JSON.stringify(genre)}]`).click();
  }
  async function matches(target, date, filters, label) {
    const got = await target.locator('article').evaluateAll(articles => articles.map(article => Number(article.dataset.id)));
    const want = select(data, date, filters);
    equal(got, want, label + ` (${want.length}件)`);
    equal(await target.textContent('#cnt'), `${want.length}件 / 全${data.length}件`, label + 'の件数表示');
  }
  await matches(page, today, {g: '話題'}, '初期表示は話題');
  const genres = [...new Set(data.map(row => row.genre))];
  equal(await page.locator('#tabs button').count(), genres.length + 1, '全ジャンルのタブ');
  for (const genre of ['すべて', ...genres]) {
    await tab(genre);
    await matches(page, today, {g: genre}, 'タブ切替 ' + genre);
  }
  await tab('すべて');
  const visible = select(data, today);
  ok(visible.length >= 2, 'お気に入りを検査できる可視行がある');
  await page.click('#fSoon');
  await matches(page, today, {soon: true}, 'これから');
  ok((await page.evaluate(() => location.hash)).includes('soon=1'), 'これからの共有ハッシュ');
  await page.click('#fNow');
  await matches(page, today, {now: true}, '今やっている');
  equal(await page.getAttribute('#fSoon', 'aria-pressed'), 'false', '今やっているはこれからと排他');
  ok(!(await page.evaluate(() => location.hash)).includes('soon=1'), '排他時にsoonハッシュを除く');
  await page.click('#fSoon');
  equal(await page.getAttribute('#fNow', 'aria-pressed'), 'false', 'これからも今やっていると排他');
  await page.click('#fSoon');
  equal(await page.getAttribute('#fRain', 'aria-pressed'), 'false', '雨の日OKは初期OFF');
  await page.click('#fRain');
  await matches(page, today, {rain: true}, '雨の日OK');
  equal(await page.locator('article .rb').count(), select(data, today, {rain: true}).length, '雨の日OKの全カードにバッジ');
  await page.click('#fBaby');
  await matches(page, today, {rain: true, baby: true}, '雨と赤ちゃんOKの併用');
  equal(await page.getAttribute('#fRain', 'aria-pressed'), 'true', '雨の日OKのaria状態');
  equal(await page.locator('article .bb').count(), select(data, today, {rain: true, baby: true}).length, '親子の全カードにバッジ');
  await page.reload();
  await matches(page, today, {rain: true, baby: true}, 'リロード後も雨と親子を復元');
  await page.click('#fBaby');
  await page.click('#fRain');
  await matches(page, today, {}, '雨と親子を解除');
  equal(await page.locator('article .rb').count(), select(data, today, {rain: true}).length, 'OFFでも雨バッジを表示');

  const sample = data[visible[0]];
  const query = sample.name.slice(0, 4);
  await page.fill('#q', query);
  await matches(page, today, {q: query}, '検索');
  await page.fill('#q', '__該当なし_検索__');
  await matches(page, today, {q: '__該当なし_検索__'}, '検索0件');
  equal(await page.locator('.empty').count(), 1, '0件の案内');
  await page.fill('#q', '');
  const area = await page.locator('#ar option').nth(1).getAttribute('value')
    || await page.locator('#ar option').nth(1).textContent();
  await page.selectOption('#ar', area);
  await matches(page, today, {a: area}, 'エリア');
  await page.fill('#q', query);
  await matches(page, today, {a: area, q: query}, 'エリアと検索の併用');
  await page.fill('#q', '');
  await page.selectOption('#ar', '');
  const mapLinks = await page.locator('article').evaluateAll(articles => articles.map(article => ({
    id: Number(article.dataset.id), map: [...article.querySelectorAll('a')].find(a => a.textContent.includes('Googleマップ'))?.href,
    official: [...article.querySelectorAll('a')].find(a => a.textContent.includes('公式サイト'))?.href,
  })));
  for (const item of mapLinks) {
    const row = data[item.id];
    const map = new URL(item.map);
    assert.equal(map.origin + map.pathname, 'https://www.google.com/maps/search/');
    assert.equal(map.searchParams.get('api'), '1');
    assert.equal(map.searchParams.get('query'), row.name + ' ' + row.area);
    if (row.url) assert.equal(item.official, new URL(row.url).href);
  }
  ok(true, '全可視行の地図リンク形式・検索語と公式リンク');

  const favoriteIds = [visible[0], visible[1]];
  for (const id of favoriteIds) await page.locator(`article[data-id="${id}"] .star`).click();
  const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('dateSpotsFav_v1')));
  equal(Object.keys(saved).sort(), favoriteIds.map(id => data[id].genre + '|' + data[id].name).sort(), 'localStorageに安定した名前キーで保存');
  await page.click('#fFav');
  await matches(page, today, {fav: new Set(favoriteIds)}, 'お気に入り');
  await page.reload();
  await matches(page, today, {fav: new Set(favoriteIds)}, 'お気に入りをリロードで復元');
  await page.locator('article .star').first().click();
  await matches(page, today, {fav: new Set([favoriteIds[1]])}, 'お気に入り表示中の解除');
  await page.click('#fFav');
  // 6つのフラグの全64状態を、実データの全行と画面で照合する。
  for (let mask = 0; mask < 64; mask++) {
    const filters = {g: 'すべて'};
    const params = new URLSearchParams({g: 'すべて'});
    for (const [bit, key] of ['rain', 'baby', 'now', 'soon', 'ended', 'fav'].entries()) {
      if (mask & (1 << bit)) {
        params.set(key, '1');
        filters[key] = key === 'fav' ? new Set([favoriteIds[1]]) : true;
      }
    }
    await page.goto(file + '#' + params);
    await matches(page, today, filters, 'フィルタ全列挙 mask=' + mask);
  }
  await page.goto(file + '#g=' + encodeURIComponent('すべて'));
  await page.click('#rand');
  equal(await page.locator('article.hl').count(), 1, 'ランダムで1件を強調');
  ok(visible.includes(Number(await page.locator('article.hl').getAttribute('data-id'))), 'ランダムの選択は現在の候補内');

  const sharedSample = data[select(data, today, {rain: true, baby: true})[0]];
  ok(Boolean(sharedSample), '共有復元に使う雨・親子の該当行がある');
  const sharedQuery = sharedSample.name;
  const hash = '#'+new URLSearchParams({g: sharedSample.genre, q: sharedQuery, rain: '1', baby: '1'});
  const shared = await pageAt(today, hash);
  await matches(shared, today, {g: sharedSample.genre, q: sharedQuery, rain: true, baby: true}, '共有ハッシュの復元');
  await shared.close();
  const conflicting = await pageAt(today, '#g='+encodeURIComponent('すべて')+'&now=1&soon=1');
  await matches(conflicting, today, {now: true, soon: true}, '競合ハッシュでは今やっているを優先');
  equal(await conflicting.getAttribute('#fSoon', 'aria-pressed'), 'false', '競合ハッシュの排他');
  await conflicting.close();

  const future = futureDate(today);
  const later = await pageAt(future, '#g='+encodeURIComponent('すべて'));
  await matches(later, future, {}, '未来の日付で終了を自動非表示 ' + future);
  equal(await later.locator('article.ended').count(), 0, '終了カードが初期表示に混ざらない');
  await later.click('#fEnd');
  await matches(later, future, {ended: true}, '終了も表示');
  const expiredCount = data.filter(row => phase(row, future) === 'ended').length;
  equal(await later.locator('article.ended .end').count(), expiredCount, '終了バッジ');
  await later.click('#fRain');
  await matches(later, future, {ended: true, rain: true}, '未来の雨と終了表示');
  await later.click('#fEnd');
  await matches(later, future, {rain: true}, '未来の雨でも終了を除く');
  await later.close();

  // Expected dates/states come from the official calendar, not the oracle parser.
  for (const [name, cases] of [
    ['HIBIYA CHRISTMAS MARKET', [['2026-12-18','soon'],['2026-12-19','now'],
      ['2026-12-21','now'],['2026-12-22','soon'],['2026-12-23','now'],
      ['2026-12-24','now'],['2026-12-25','now'],['2026-12-26','ended']]],
    ['初日の出特別営業', [['2026-12-31','soon'],['2027-01-01','now'],['2027-01-02','ended']]],
  ]) {
    for (const [day, state] of cases) {
      const target = await pageAt(day, '#'+new URLSearchParams({g:'すべて',q:name}));
      try {
        equal(await target.locator('article').count(), state==='ended'?0:1, name+' '+day+' initial');
        if (state==='ended') await target.click('#fEnd');
        equal(await target.locator('article .'+{soon:'soon',now:'now',ended:'end'}[state]).count(),1,name+' '+day+' badge');
        if (day==='2026-12-22') equal(await target.locator('.soon').textContent(),'これから(あと1日)','休催日の次回開始日');
      } finally {await target.close();}
    }
  }

  await tab('すべて');
  ok(await page.evaluate(() => {
    const tabs = document.getElementById('tabs');
    return tabs.scrollWidth > tabs.clientWidth && getComputedStyle(tabs).overflowX === 'auto';
  }), 'モバイルのタブ横スクロール');
  await page.evaluate(() => window.scrollTo(0, 2000));
  equal(await page.locator('header').evaluate(header => header.getBoundingClientRect().top), 0, 'ヘッダー固定');
  const desktop = await ctx.newPage();
  await desktop.setViewportSize({width: 1366, height: 900});
  await desktop.clock.setFixedTime(new Date(today + 'T12:00:00+09:00'));
  await desktop.goto(file);
  await matches(desktop, today, {g: '話題'}, 'デスクトップの初期表示');
  ok((await desktop.locator('meta[name="description"]').getAttribute('content')).includes(`${data.length}件`), 'メタ情報はJSON件数と一致');
  await desktop.close();
  await ctx.close();
  equal(errors, [], '全ページでJSエラーなし');
  equal(external, [], '全ページで外部リクエストなし');
  console.log(JSON.stringify({checks, rows: data.length, today, future, errors: 0, external: 0}));
}

withBrowser(run).catch(error => {console.error(error); process.exitCode = 1;});
