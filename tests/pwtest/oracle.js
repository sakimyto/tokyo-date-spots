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

function intervals(period = '', note = '') {
  let year;
  const result = [];
  for (const part of period.split('、')) {
    const tokens = [...part.replace('1日のみ', '').matchAll(/(?:(\d{4})年)?(?:(\d+)月)?(\d+)日/g)].slice(0, 2);
    const first = tokens[0];
    if (!first || !first[2] || (!first[1] && !year) || part.slice(0, first.index).trim()) return null;
    year = Number(first[1] || year);
    const start = dateNumber(year, Number(first[2]), Number(first[3]));
    if (tokens.length === 1) {
      if (!(part + note).includes('1日のみ') && !part.endsWith('のみ')) return null;
      result.push([start, start]);
    } else if (tokens.length === 2) {
      const last = tokens[1];
      const between = part.slice(first.index + first[0].length, last.index).trim();
      if (!['〜','～','~','・'].includes(between)) return null;
      let endYear = Number(last[1] || year);
      const endMonth = Number(last[2] || first[2]);
      let end = dateNumber(endYear, endMonth, Number(last[3]));
      if (!last[1] && end < start) end = dateNumber(++endYear, endMonth, Number(last[3]));
      if (end < start) return null;
      result.push(...(between === '・' ? [[start,start],[end,end]] : [[start,end]]));
    } else return null;
  }
  return result;
}

function bounds(period = '', note = '') {
  const ranges = intervals(period, note);
  return ranges ? [Math.min(...ranges.map(r=>r[0])), Math.max(...ranges.map(r=>r[1]))] : null;
}

function phase(row, date) {
  const ranges = intervals(row.period, row.period_note);
  if (!ranges) return 'permanent';
  const now = Number(date.replaceAll('-', ''));
  if (ranges.some(([s,e])=>s<=now&&now<=e)) return 'now';
  return now > Math.max(...ranges.map(r=>r[1])) ? 'ended' : 'soon';
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
