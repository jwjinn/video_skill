import {defineConfig} from 'vite';
import {createRequire} from 'node:module';
// These packages publish CommonJS defaults; load them explicitly in ESM configs.
const require = createRequire(import.meta.url);
const motionCanvas = require('@motion-canvas/vite-plugin').default;
const ffmpeg = require('@motion-canvas/ffmpeg').default;

export default defineConfig({
  cacheDir: '.vite-cache',
  optimizeDeps: {include: ['@motion-canvas/2d/editor']},
  plugins: [motionCanvas({project: './src/project.ts', output: '../charts'}), ffmpeg()],
  server: {host: '127.0.0.1', port: 0},
});
