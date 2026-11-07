import project from './project?project';
import {Renderer, RendererResult, Vector2} from '@motion-canvas/core';

const button = document.querySelector<HTMLButtonElement>('#render')!;
const status = document.querySelector<HTMLElement>('#status')!;
for (const weight of [400, 700]) await document.fonts.load(`${weight} 42px "Noto Sans KR"`, '구현 시험 문서 합성 데이터 쌓이는 순서');
await document.fonts.ready;
button.disabled = false;
status.textContent = 'READY';
button.addEventListener('click', async () => {
  button.disabled = true;
  const renderer = new Renderer(project);
  const errors: string[] = [];
  const unsubscribe = project.logger.onLogged.subscribe(entry => {
    if (entry.level === 'error') errors.push(entry.message);
  });
  let result: RendererResult | undefined;
  renderer.onFinished.subscribe(value => result = value);
  renderer.onFrameChanged.subscribe(frame => status.textContent = `FRAME ${frame}/600`);
  document.querySelector('#stage')!.replaceChildren(renderer.stage.finalBuffer);
  try {
    await renderer.render({...project.meta.getFullRenderingSettings(), name: 'DEMO', size: new Vector2(1080, 1350),
      fps: 30, resolutionScale: 1, range: [0, 20 - 1 / 30],
      exporter: {name: '@motion-canvas/ffmpeg', options: {fastStart: true, includeAudio: false}}});
    if (result !== RendererResult.Success || errors.length) throw new Error(errors.join('\n') || String(result));
    status.textContent = 'COMPLETE';
  } catch (error) {
    status.textContent = `FAILED ${String(error)}`;
  } finally {
    unsubscribe();
    button.disabled = false;
  }
});
