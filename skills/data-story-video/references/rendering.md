# Portable rendering workflow

Copy `assets/his01-starter/` to a new working folder; do not render into the installed skill. This starter includes a Motion Canvas chart and synthetic CSV, a Pillow layout, and an FFmpeg compositor. No API key is needed to run the demo. AI-assisted editing can use the user's existing coding agent.

## Requirements

Python 3.10+, Node.js 20+, npm, ffmpeg and ffprobe, and a Korean font. Python packages are in requirements.txt; JS dependencies and lockfile are under motion-canvas/. On Debian/Ubuntu install `ffmpeg fonts-noto-cjk`. macOS can use Apple SD Gothic Neo from the local OS (not redistributed). Set VIDEO_FONT_FILE to use another Korean TTF/OTF/TTC; VIDEO_FONT_INDEX and VIDEO_BOLD_FONT_INDEX select TTC faces.

From a **copy** of the starter:

```sh
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

The CI environment is pinned to Ubuntu 24.04, a supported browser target. On Linux without browser system libraries, use `npx playwright install --with-deps chromium` (may require administrator privileges). Newer distributions may require a supported container image or an updated Playwright version. On Windows use `.venv\Scripts\activate` instead of the POSIX activation command. Output: `output/DEMO.mp4` and `output/DEMO-validation.json`. Font/browser/package installation requires network access; the video pipeline itself runs locally.

## Inputs

- episode.json: id, track, title, question, ending, conclusion, related, chapters; optional `timing` {intro, example, chart, outro}, in seconds. Defaults: 3, 5, 12, 5.
- chapter: chart (unique filename-safe ID), two captions, example {title, term, caption}.
- chart-catalog.json: title and sourceFiles for each chart.
- motion-canvas/data/sample.csv: week, implementation, tests, docs. All shipped values are made up. Replace them and update all captions, units, calculations and synthetic markings when using genuine records.
- charts/<ID>.mp4: chart inputs. The example renderer creates DEMO.mp4; add scenes/projects and render targets to make other chart IDs.

## Geometry and time contract

Input charts must be 1080×1350 and at least 19.5 seconds long. Source 1.5–19.5 seconds is mapped to the configured chart duration. Crop x=0,y=114,w=1080,h=1140; resize to 972×1026; place at x=54,y=108. Lower explanation starts y=1163, at 34px and at most two lines. New charts must keep all axis labels/legends within this crop, or adjust the layout first. The compositor validates input dimensions, duration, captions, final frame count and audio absence.

The chart reveals weekly samples in order. Smooth geometric interpolation only transitions between samples; it must never be described as additional measured observations. For a comparison use consistent units and time windows. Code line totals are not productivity or quality; test line share is not coverage; token list-price estimates are not invoices.

## Evidence and export

Inspect the actual chart against the CSV. Check first/last and turning-point values, missing data treatment, denominator and date range. FFmpeg success alone does not prove data correctness. Extract opening/example/mid-chart/ending frames and inspect clipping, legends, text and reading time. The demo CLI decodes the entire finished file and writes a machine-readable media validation record.

For real work also deliver scene script, technical caption draft, source tables, calculation method, and a self-contained ID.md. The agent performs that evidence/narrative work; `render.py` only renders and verifies media. It does not automatically verify your historical claims or write the final technical article.
