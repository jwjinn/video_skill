# Data Story Video

A reusable agent skill and local rendering starter for **silent, evidence-based explainer videos**: one question, moving data, familiar examples, and short explanations beneath each chart.

[한국어](README.md) · [Skill](skills/data-story-video/SKILL.md) · [Rendering contract](skills/data-story-video/references/rendering.md)

![Synthetic chart demo](docs/demo.gif)

All shipped demo values are **synthetic**, not a real project's history or performance. [MP4](docs/demo.mp4) · [Self-contained script/evidence document (Korean)](docs/DEMO.md)

## Install as a Codex plugin

```sh
codex plugin marketplace add jwjinn/video_skill --ref master
codex plugin add data-story-video@video-skill
```

Start a new chat and select the packaged `data-story-video` skill. Example:

> Use $data-story-video to turn these records into a silent explainer. Connect related charts around one question, explain terms with familiar examples, and add scene-specific explanations underneath. Preserve technical details and original numbers. Deliver the source, script, evidence, validation and a self-contained Markdown document. Write the narration text in English.

Some clients show a plugin-qualified skill name. If `plugin add` is unavailable, add the marketplace and install from the desktop Plugins Directory. This is a GitHub marketplace package, **not a listing in the official public directory**. No MCP service, login or automatic hook is bundled.

## Install only the skill

Choose this instead of plugin installation. Do not overwrite an existing skill without reviewing it.

```sh
git clone https://github.com/jwjinn/video_skill.git
mkdir -p ~/.agents/skills
cp -R video_skill/skills/data-story-video ~/.agents/skills/data-story-video
```

Other Agent Skills hosts can copy this self-contained folder to their own skill location; their plugin installation mechanisms are not all tested.

## Render the demo locally

Requires Python 3.10+, Node.js 20+, npm, FFmpeg/ffprobe, and a Korean font. The default sample text is Korean; adapt it in episode.json and the Motion Canvas scene for another language. On Ubuntu/Debian, install `ffmpeg fonts-noto-cjk`. macOS can use its existing system font. Set VIDEO_FONT_FILE for another font. Font files are not bundled.

```sh
git clone https://github.com/jwjinn/video_skill.git
cd video_skill
cp -R skills/data-story-video/assets/his01-starter ./my-video
cd my-video
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
cd motion-canvas
npm ci
npx playwright install chromium
npm run check
npm run render
cd ..
python3 render.py --redraw
```

On Linux, missing browser system libraries may require `npx playwright install --with-deps chromium`. On Windows, activate with `.venv\Scripts\activate` instead. Output: `output/DEMO.mp4` and its validation JSON.

The pipeline uses Motion Canvas → Pillow text overlays → FFmpeg. Defaults: 1080×1350, 30fps, silent; one chapter takes 25 seconds, four take 76. Configure pacing through episode.json's `timing`. Dependencies are downloaded during setup; rendering runs locally and requires no API key.

Edit episode.json, chart-catalog.json, motion-canvas/data/sample.csv and motion-canvas/src/scene.ts to use your own material. See the rendering contract before cropping a new chart. The code verifies media properties and full decoding; it does **not** establish historical truth or automatically generate the final technical article. The skill guides an agent through that evidence and writing work.

This repository's code and documentation are MIT-licensed. Dependencies retain their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md). The plugin layout follows the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).
