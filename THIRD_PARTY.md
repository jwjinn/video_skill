# External components

The root MIT license covers this repository's original code, documentation and synthetic example data. It does not relicense dependencies or input/output assets supplied by a user.

|Component|License / notice|
|---|---|
|Motion Canvas packages|MIT; installed from npm, not vendored|
|Vite / TypeScript|MIT / Apache-2.0 respectively|
|Playwright|Apache-2.0; browser downloads have their own notices|
|Pillow|MIT-CMU / HPND, see installed package notices|
|Noto Sans KR via @fontsource|SIL Open Font License 1.1; npm includes font notices|
|FFmpeg|Build-dependent LGPL/GPL terms; installed separately|
|macOS / Windows system fonts|Referenced on the user's machine; no font files redistributed|

The starter pins exact JavaScript versions in package-lock.json. It uses Vite 6.4.5 with an explicit npm peer override: Motion Canvas 3.17.2 advertises Vite 4/5 support, but the older Vite line has published advisories. This package checks the adapter with Vite 6 via TypeScript and an actual chart-render smoke test. The override is not a claim of upstream Vite 6 support. Recheck compatibility when upgrading either package.

The repo ships no original company data, private historical logs, account settings, API credentials, or proprietary fonts. The synthetic dataset is intended to make the rendering workflow independently reproducible.
