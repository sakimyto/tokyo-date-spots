// 画面のrange/base関数を参照しない、JSTの日付・行集合の期待値。
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.resolve(process.env.SPOTS_ROOT || path.join(__dirname, '../..'));
const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'spots.json'), 'utf8'));
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const updated = html.match(/最終更新\s+(\d{4}-\d{2}-\d{2})/);
const today = process.env.TEST_DATE || updated?.[1];
if (!today || !/^\d{4}-\d{2}-\d{2}$/.test(today)) throw new Error('最終更新日を取得できません');

function dateNumber(year, month, day) {
  const date = new Date(Date.UTC(year, month - 1, day));
  if (date.getUTCFullYear() !== year || date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) {
    throw new Error(`invalid date: ${year}-${month}-${day}`);
  }
  return year * 10000 + month * 100 + day;
}

function bounds(period = '') {
  const first = /(\d{4})年(\d+)月(\d+)日/.exec(period);
  if (!first) return null;
  const [year, month, day] = first.slice(1).map(Number);
  const tail = period.slice(first.index + first[0].length);
  const end = /^\s*[〜～・]\s*(?:(\d{4})年)?(?:(\d+)月)?(\d+)日/.exec(tail);
  if (!end && !/^[^〜～・]*?1日のみ/.test(tail)) return null;
  const start = dateNumber(year, month, day);
  if (!end) return [start, start];
  let endYear = end[1] ? Number(end[1]) : year;
  const endMonth = end[2] ? Number(end[2]) : month;
  const endDay = Number(end[3]);
  if (!end[1] && dateNumber(endYear, endMonth, endDay) < start) endYear++;
  return [start, dateNumber(endYear, endMonth, endDay)];
}

function phase(row, date) {
  const range = bounds(row.period);
  if (!range) return 'permanent';
  const now = Number(date.replaceAll('-', ''));
  return now < range[0] ? 'soon' : now > range[1] ? 'ended' : 'now';
}

function prefecture(area) {
  const match = /^(神奈川県|埼玉県|千葉県|栃木県|群馬県|茨城県|山梨県|静岡県|長野県)/.exec(area);
  return match ? match[0] : '東京都';
}

function select(rows, date, filters = {}) {
  // ハッシュに両方あれば「今やっている」を優先する仕様。
  const soon = filters.soon && !filters.now;
  return rows.map((row, id) => ({row, id})).filter(({row, id}) => {
    const state = phase(row, date);
    const query = (filters.q || '').trim().toLowerCase();
    const haystack = ['name', 'desc', 'area', 'period', 'venue', 'age', 'baby']
      .map(key => row[key] || '').join(' ').toLowerCase();
    return (!filters.g || filters.g === 'すべて' || row.genre === filters.g)
      && (!filters.a || prefecture(row.area) === filters.a)
      && (!query || haystack.includes(query))
      && (!filters.now || state === 'now') && (!soon || state === 'soon')
      && (filters.ended || state !== 'ended')
      && (!filters.rain || row.rain_ok) && (!filters.baby || row.baby_ok)
      && (!filters.fav || filters.fav.has(id));
  }).map(item => item.id);
}

function futureDate(date) {
  if (date < '2026-12-07') return '2026-12-07';
  const [year, month] = date.split('-').map(Number);
  const future = new Date(Date.UTC(year, month, 7));
  return future.toISOString().slice(0, 10);
}

module.exports = {ROOT, data, html, today, bounds, phase, prefecture, select, futureDate};
