# AGENTS.md

Instructions for AI coding agents working in this repository. Read this whole file before writing or changing any code.

## 1. Project Overview

StockPredict is a Flask prototype for predicting LQ45 stock closing prices with a Bi-LSTM model.

- Backend: Flask (`app.py`, `routes/`, `services/`, `models/`). Python 3.12.
- Frontend: Jinja templates (`templates/`) and static assets served from `public/static/`.
- UI language: Indonesian. Keep all visible text in Indonesian. Code, identifiers, and this document are in English.

## 2. Hard Rules

1. Read the design system (Section 4) before writing any markup or CSS.
2. Do not replace the UI with Bootstrap, Tailwind, Material, Bulma, or any other UI framework or component library. The only UI system is Basecoat UI, self-hosted.
3. Do not load any CSS or JS from a CDN at runtime. Every asset must come from `public/static/`.
4. Do not add npm, a build step, React, Vue, or any package dependency.
5. Do not use Tailwind utility classes in markup (`flex`, `grid`, `gap-4`, `p-6`, `text-sm`, `bg-primary`, `hidden`, `md:`, and similar). Use Basecoat component classes and project CSS in `app.css`.
6. Do not modify `app.py`, `services/`, `models/`, or `tests/` unless the task explicitly requires it.
7. Do not delete files unless the task explicitly requires it. Ask first.
8. Do not leave comments in code. Write clean, self-explanatory code. No `#` comments in Python, no `//` or `/* */` comments in JS or CSS, no `<!-- -->` comments in templates.
9. Do not use `alert()` or leftover `console.log` in JavaScript.
10. Do not commit or push to `main` or `develop` directly. Follow Section 6.

## 3. Repository Layout

```
app.py                              Flask entry point (static_folder = "public/static")
routes/                             Blueprints: main_routes.py, prediction_routes.py
services/                           Prediction and upload logic (do not change for UI work)
models/                             Trained model files (do not change)
templates/
  base.html                         Base layout, stylesheet and script order
  index.html                        Home page (/)
  prediction.html                   Prediction form (/prediksi)
  about.html                        About page (/tentang)
  result.html                       Result page (/hasil)
  components/icon.html              Lucide icon macro
  components/macros.html            Jinja macros: badge, flash_messages, info_row
public/static/
  vendor/basecoat/basecoat.cdn.min.css   Basecoat CSS (do not edit)
  vendor/basecoat/js/all.min.js          Basecoat JS (do not edit)
  vendor/fonts/                          Self-hosted Plus Jakarta Sans (do not edit)
  css/theme.css                     Design tokens
  css/app.css                       Project layout and components
  js/main.js                        Form interactions (vanilla JS)
tests/                              unittest suite
change_log/                         Release notes, one file per version
```

Note: in Flask the static URL `/static/...` maps to `public/static/...` on disk. Use `url_for('static', filename='css/app.css')` in templates.

## 4. Design System

### 4.1 Stack

- Basecoat UI v1.1.0, self-hosted (`public/static/vendor/basecoat/`).
- Project design tokens in `public/static/css/theme.css`, following shadcn/ui naming.
- Project layout and components in `public/static/css/app.css`.
- Light mode only. Do not add dark mode, a theme switcher, or `.dark` styles.
- Primary color is sky.

### 4.2 Stylesheet and Script Order

In `templates/base.html`, this order is required:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='vendor/basecoat/basecoat.cdn.min.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
{% block extra_css %}{% endblock %}
```

Scripts: `vendor/basecoat/js/all.min.js` first (deferred), then `js/main.js` (deferred), then `{% block extra_js %}`.

Do not add `@import` to any stylesheet. Do not duplicate Basecoat component styles in `app.css`.

### 4.3 Design Tokens (`theme.css`, light mode)

| Token | Value | Use |
|---|---|---|
| `--background` | `oklch(1 0 0)` | Page background |
| `--foreground` | `oklch(0.208 0.042 265.755)` slate-900 | Main text |
| `--card` / `--popover` | `oklch(1 0 0)` | Card and popover surface |
| `--primary` | `oklch(0.5 0.134 242.749)` sky-700 | Primary buttons, active links, chart accents |
| `--primary-foreground` | `oklch(0.985 0.006 236.62)` | Text on primary |
| `--secondary` | `oklch(0.968 0.007 247.896)` slate-100 | Secondary buttons, neutral chips |
| `--muted` | `oklch(0.984 0.003 247.858)` slate-50 | Panels, footer background |
| `--muted-foreground` | `oklch(0.554 0.046 257.417)` slate-500 | Supporting text |
| `--accent` | `oklch(0.977 0.013 236.62)` sky-50 | Hover, badges, highlights |
| `--accent-foreground` | `oklch(0.5 0.134 242.749)` sky-700 | Text on accent |
| `--destructive` | `oklch(0.577 0.245 27.325)` red-600 | Errors, price drops, delete actions |
| `--border` / `--input` | `oklch(0.929 0.013 255.508)` slate-200 | Borders |
| `--ring` | `oklch(0.685 0.169 237.323)` sky-500 | Focus ring |
| `--radius` | `0.65rem` | Base radius |
| `--positive` | `oklch(0.596 0.145 163.225)` emerald-600 | Price up, success status |
| `--warning` | `oklch(0.666 0.179 58.318)` amber-500 | Disclaimers, data warnings |
| `--font-sans` | Plus Jakarta Sans, then system sans-serif fallbacks | All text |

### 4.4 Color Rules

| Role | Color | Use |
|---|---|---|
| Primary | sky-700 | Main buttons, active links, chart accents |
| Secondary | slate-100 | Secondary buttons, neutral chips |
| Tertiary / accent | sky-50 with sky-700 text | Badges, highlights, info panels |
| Positive | emerald-600 | Price up, success |
| Destructive | red-600 | Errors, price down, delete |
| Warning | amber-500 | Disclaimers, data warnings |

`--primary` must stay at sky-700 so white text on buttons meets WCAG AA (4.5:1). Do not lighten it to sky-500 for button backgrounds.

### 4.5 Components

Use Basecoat classes and attributes:

- Buttons: `<button class="btn">`. Variants: `data-variant="outline"`, `data-variant="secondary"`, `data-variant="ghost"`. Sizes: `data-size="lg"`, `data-size="sm"`.
- Cards: `<div class="card">` with optional `<header>`, `<section>`, `<footer>`. Small cards: `data-size="sm"`.
- Badges: `<span class="badge">`, with `data-variant="secondary"` where needed.
- Alerts: `<div class="alert">`. Errors: `<div class="alert" data-variant="destructive">`.
- Form fields: wrap each control in `<div class="field">`. Selects: `<select class="select">`. Invalid state: `data-invalid` on the `.field` wrapper and `aria-invalid="true"` on the control.
- Tables: `<div class="table-container"><table class="table">`.

Layout, spacing, grid, typography, and responsive rules are written by hand in `app.css` with plain CSS and the tokens above.

### 4.6 Icons

Use inline Lucide SVG through the macro in `templates/components/icon.html`:

```jinja
{% from "components/icon.html" import icon %}
{{ icon('arrow-right', 18) }}
```

Available names: `chart-line`, `upload`, `database`, `cpu`, `shield-check`, `arrow-right`, `download`, `info`, `triangle-alert`, `circle-check`, `circle-alert`, `loader-circle`, `file-spreadsheet`, `github`. To add an icon, add its SVG paths to the dictionary in that macro. Do not install an icon package.

### 4.7 Jinja Blocks

Keep these block names unchanged because all templates depend on them: `title`, `extra_css`, `content`, `extra_js`.

### 4.8 Responsive and Accessibility

- Breakpoints: `1024px` (two columns become one) and `640px` (container padding 16px, smaller headings, full-width buttons).
- Navigation must work at 375px width without horizontal scrolling. Tables scroll inside `.table-container`.
- Focus must be visible: `:focus-visible` uses `outline: 2px solid var(--ring)` with `outline-offset: 2px`.
- Every `input` and `select` needs a matching `<label for="...">`.
- Respect `prefers-reduced-motion`.

### 4.9 Prediction Form Behavior (`templates/prediction.html`, `public/static/js/main.js`)

- The form uses `novalidate`. Validation is done in `main.js`, and the server must still validate everything.
- Required fields: stock (`#stock`), CSV file (`#csv_file`), horizon (`#horizon`). An empty required field gets `data-invalid`, a red error message, and receives focus on submit.
- Errors are red. Do not use sky for error states.
- File rules: extension must be `.csv`; size must be at most 5 MB. Errors show in `#csv-error`.
- After a valid file is chosen, `main.js` reads the file and counts data rows (skip an optional `sep=` line and the header). Rows must be at least 30.
- If rows are fewer than 30, submit is blocked and a `<dialog id="csv-row-dialog">` popup shows the detected row count. The request must not reach `/proses-prediksi`.
- While the file is being read, the submit button is disabled with label "Memeriksa file…".
- After a valid submit, the button is disabled with label "Memproses…" and the spinner (`[data-spinner]`) is shown.

### 4.10 Page Content Rules

- Keep existing Indonesian text unless the task says to change it.
- Do not invent sample numbers. Empty states must not show example data.
- Result page (`/hasil`): if no result data exists, show an empty state with a `chart-line` icon, the title "Belum ada hasil prediksi", and a button to `/prediksi`.
- Disclaimer on results: "Seluruh angka merupakan estimasi model, bukan rekomendasi investasi."

## 5. Coding Standards

- Keep code short and clean. No comments of any kind (see Hard Rule 8).
- Do not add features, abstractions, or error handling beyond what the task needs.
- Prefer editing existing files over creating new ones.
- Do not add dependencies.
- Write vanilla JavaScript with no libraries.
- Keep JS under about 100 lines in `main.js`.

## 6. Git and Branching Workflow

The release is done by the repository owner, not by the agent.

1. Start from `develop`. Run `git checkout develop` and `git pull` before making changes.
2. Create a feature branch from `develop`: `git checkout -b feature/<short-kebab-name>` (or `fix/...`, `refactor/...`).
3. Make the changes on that branch. Commit with clear messages.
4. Run the checks in Section 7 before merging.
5. Merge the branch into `develop`: `git checkout develop`, `git merge --no-ff feature/<name>`.
6. Do not merge into `main`. Do not create release tags. Do not run release commands. The owner releases.
7. Do not push unless the owner asks. When asked, push `develop` and the feature branch only.
8. Never use `git push --force`, `git reset --hard`, or `git checkout --` on work you did not create without asking first.
9. Check `git status` before any command that could discard uncommitted changes. Stash or commit them first.

## 7. Verification

Before reporting a task as done:

1. Run the tests: `python -m unittest discover -s tests -v`. All tests must pass.
2. Run the app: `python app.py` (or `flask run`), then confirm these routes return HTTP 200: `/`, `/prediksi`, `/tentang`, `/hasil`.
3. For UI changes, open the page in a browser and check the golden path and edge cases: empty fields, wrong file type, file over 5 MB, CSV with fewer than 30 rows, and a valid CSV.
4. If you cannot test the UI in a browser, say so explicitly in your report instead of claiming success.

Definition of done for UI work:

- No Bootstrap references: `grep -ri "bootstrap" templates/ public/static/` returns nothing.
- No CDN references: `grep -rn "cdn.jsdelivr.net\|unpkg\|cdnjs" templates/` returns nothing.
- No Tailwind utility classes in markup.
- No code comments added.
- Keyboard focus is visible on buttons, links, inputs, and selects.
- Text contrast is at least 4.5:1.
- The page works at 375px width without horizontal scrolling.

## 8. Changelog

Release notes are stored in `change_log/v<major>/v<version>.md`, for example `change_log/v1/v1.0.0.md`. Start from `change_log/TEMPLATE.md` and follow this format:

```md
# vX.Y.Z

Ringkasan singkat rilis.

**Tanggal Rilis:** DD Bulan YYYY

## Fitur

-

## Perbaikan

-

## Teknis

-

## Catatan

-
```

Rules:

1. Write the changelog in Indonesian.
2. Group entries under the four headings; do not list commits, branches, or internal ticket names.
3. Include only user-visible changes and meaningful technical changes. Keep it short.
4. Create a new file for each release. Do not rewrite a published release note.
5. Keep `change_log/TEMPLATE.md` as the source for new release files.
