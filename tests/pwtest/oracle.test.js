const {test} = require('node:test');
const assert = require('node:assert/strict');
const {bounds, phase, select} = require('./oracle');

test('会期の代表・境界・不正形式と年越し', () => {
  for (const text of ['', '未定', '11月13日〜14日', '2026年11月13日公開', '2026年11月13日開業']) {
    assert.equal(bounds(text), null, text);
  }
  assert.deepEqual(bounds('2026年11月13日(金) 1日のみ'), [20261113, 20261113]);
  assert.deepEqual(bounds('2026年11月13日〜15日'), [20261113, 20261115]);
  assert.deepEqual(bounds('2026年11月13日・14日'), [20261113, 20261114]);
  assert.deepEqual(bounds('2026年12月31日〜1月1日'), [20261231, 20270101]);
  assert.deepEqual(bounds('2026年12月31日〜2027年1月1日'), [20261231, 20270101]);
  assert.throws(() => bounds('2026年11月32日 1日のみ'), /invalid date/);
  const row = {period: '2026年11月13日〜14日'};
  assert.equal(phase(row, '2026-11-12'), 'soon');
  assert.equal(phase(row, '2026-11-13'), 'now');
  assert.equal(phase(row, '2026-11-14'), 'now');
  assert.equal(phase(row, '2026-11-15'), 'ended');
});

test('全64状態でフィルタの不変条件を列挙し、壊れた変種を検出', () => {
  const rows = ['permanent', 'soon', 'now', 'ended'].flatMap(state =>
    [false, true].flatMap(rain_ok => [false, true].map(baby_ok => ({
      genre: 'test', name: state, area: '神奈川県', desc: '', rain_ok, baby_ok,
      period: {permanent: '', soon: '2026年11月14日 1日のみ',
        now: '2026年11月13日 1日のみ', ended: '2026年11月12日 1日のみ'}[state],
    }))));
  for (let mask = 0; mask < 64; mask++) {
    const filters = Object.fromEntries(['rain', 'baby', 'now', 'soon', 'ended', 'fav']
      .map((name, bit) => [name, name === 'fav' && (mask & (1 << bit))
        ? new Set(rows.map((_, id) => id).filter(id => id % 2 === 0)) : Boolean(mask & (1 << bit))]));
    const got = select(rows, '2026-11-13', filters);
    const want = rows.map((row, id) => ({row, id})).filter(({row, id}) =>
      (!filters.rain || row.rain_ok) && (!filters.baby || row.baby_ok)
      && (filters.now ? row.name === 'now' : !filters.soon || row.name === 'soon')
      && (filters.ended || row.name !== 'ended')
      && (!filters.fav || filters.fav.has(id))).map(({id}) => id);
    assert.deepEqual(got, want, `mask=${mask}`);
  }
  const endedVisible = select(rows, '2026-11-13', {ended: true});
  assert.throws(() => assert.deepEqual(endedVisible, select(rows, '2026-11-13')), assert.AssertionError);
  assert.throws(() => assert.deepEqual(
    select(rows, '2026-11-13', {soon: true}),
    select(rows, '2026-11-13', {now: true, soon: true})), assert.AssertionError);
});
