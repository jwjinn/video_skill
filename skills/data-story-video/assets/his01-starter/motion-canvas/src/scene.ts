import {Line, Rect, Txt, makeScene2D} from '@motion-canvas/2d';
import {createSignal, linear} from '@motion-canvas/core';
import csv from '../data/sample.csv?raw';

const rows = csv.trim().split(/\r?\n/).map(line => line.split(','));
if (rows.shift()?.join(',') !== 'week,implementation,tests,docs' || rows.length < 2) {
  throw new Error('Expected at least two weekly samples with week,implementation,tests,docs');
}
const data = rows.map(([week, ...values]) => ({week, values: values.map(Number)}));
if (data.some(row => !/^\d{4}-\d{2}-\d{2}$/.test(row.week) || row.values.length !== 3 || row.values.some(v => !Number.isFinite(v) || v < 0))) {
  throw new Error('Expected dated samples and three non-negative line counts');
}
if (data.some((row, i) => i > 0 && row.week <= data[i - 1].week)) {
  throw new Error('Weeks must be unique and sorted');
}

export default makeScene2D(function* (view) {
  view.fill('#10181c');
  const time = createSignal(0);
  const progress = () => Math.min(1, Math.max(0, (time() - 2.4) / 15));
  const index = () => Math.min(data.length - 1, Math.floor(progress() * (data.length - 1)));
  const colors = ['#85b6e7', '#54bca8', '#fb744c'];
  const names = ['구현', '시험', '문서'];
  const totals = data.map(row => row.values.reduce((a, b) => a + b, 0));
  const maximum = Math.max(1000, Math.ceil(Math.max(...totals) / 1000) * 1000);
  function text(value: string | (() => string), x: number, y: number, size: number, color = '#f4f1e8') {
    const node = new Txt({text: value, x: x - 540, y: y - 675, offset: [-1, -1],
      fontFamily: 'Noto Sans KR', fontSize: size, fill: color, fontWeight: 700});
    view.add(node);
    return node;
  }
  text('합성 데이터 · 실제 개발 이력 아님', 80, 155, 25, '#fb744c');
  text('코드·시험·문서가', 80, 225, 60);
  text('쌓이는 순서', 80, 307, 64);
  text(() => totals[index()].toLocaleString('en-US') + ' 줄', 80, 430, 100);
  text(() => data[index()].week + ' 주 · 합성 예시', 80, 560, 28, '#97a6a9');
  const left = 160, right = 990, top = 680, base = 1045;
  for (const value of [0, maximum / 2, maximum]) {
    const y = base - value / maximum * (base - top);
    view.add(new Line({points: [[left - 540, y - 675], [right - 540, y - 675]], stroke: '#334248', lineWidth: 2}));
    text(value.toLocaleString('en-US'), 65, y - 15, 23, '#97a6a9');
  }
  const point = (week: number, category: number): [number, number] => [
    left + week / (data.length - 1) * (right - left) - 540,
    base - data[week].values.slice(0, category).reduce((a, b) => a + b, 0) / maximum * (base - top) - 675,
  ];
  for (let category = 0; category < 3; category++) {
    view.add(new Line({closed: true, fill: colors[category], points: () => {
      const position = progress() * (data.length - 1);
      const i = Math.min(data.length - 2, Math.floor(position)), blend = position - i;
      const edge = (level: number) => {
        const points = Array.from({length: i + 1}, (_, w) => point(w, level));
        const a = point(i, level), b = point(i + 1, level);
        points.push([a[0] + (b[0] - a[0]) * blend, a[1] + (b[1] - a[1]) * blend]);
        return points;
      };
      return [...edge(category + 1), ...edge(category).reverse()];
    }}));
  }
  // Bound labels to the chart area even with more than four source samples.
  const ticks = [...new Set([0, Math.floor((data.length - 1) / 3), Math.floor(2 * (data.length - 1) / 3), data.length - 1])];
  for (const i of ticks) text(data[i].week.slice(5), left + i / (data.length - 1) * (right - left) - 28, 1090, 23, '#97a6a9');
  names.forEach((name, i) => {
    view.add(new Rect({x: 100 + i * 300 - 540, y: 1172 - 675, width: 16, height: 16, fill: colors[i]}));
    text(name, 120 + i * 300, 1155, 28, '#97a6a9');
  });
  text('줄 수는 품질·생산성 점수가 아닙니다.', 80, 1210, 24, '#97a6a9');
  yield* time(20, 20, linear);
});
