# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based personal blog and portfolio site hosted on GitHub Pages, built on a heavily customized Minimal Mistakes theme. Content is bilingual (English for technical posts, Vietnamese for personal content) and organized into five collection types. Includes a Running stats page powered by automated Strava integration.

## Build & Serve Commands

```bash
bundle install                                                   # Install Ruby dependencies
bundle exec jekyll serve                                         # Serve locally at localhost:4000
bundle exec jekyll serve --livereload                            # Serve with live reload (hawkins gem)
bundle exec jekyll serve --config _config.yml,_config.dev.yml   # Serve with dev overrides
bundle exec jekyll build                                         # Build static site to _site/
npx uglify-js assets/js/vendor/jquery/jquery-1.12.4.min.js \
  assets/js/plugins/jquery.fitvids.js \
  assets/js/plugins/jquery.greedy-navigation.js \
  assets/js/plugins/jquery.magnific-popup.js \
  assets/js/plugins/jquery.smooth-scroll.min.js \
  assets/js/plugins/stickyfill.min.js \
  assets/js/_main.js -c -m -o assets/js/main.min.js            # Rebuild minified JS bundle
npm run watch:js                                                 # Watch and auto-rebuild JS
```

> `npm run build:js` requires `uglifyjs` to be globally installed; use `npx uglify-js ...` (command above) instead.

Use `_config.dev.yml` for local development — it disables analytics, uses `localhost:4000` as URL, and sets SASS to `expanded` output for easier debugging.

## Content Architecture

**Five collection types** (all use Markdown with YAML front matter):

| Directory | Purpose | Filename format |
|-----------|---------|-----------------|
| `_posts/` | Technical AI/ML blog posts | `YYYY-MM-DD-slug.md` |
| `_readings/` | Book and article reviews | `YYYY-MM-DD-slug.md` |
| `_learnings/` | Course certificates and summaries | `YYYYMMDDname.md` or `YYYYMMDD-name.md` |
| `_collections/` | Personal life experiences (travel, sports) | `YYYY-MM-DD-slug.md` |
| `_journeys/` | Trip photo/video galleries | `YYYY-MM-DD-slug.md` |

All collections use `permalink: /:collection/:path/` and the `single` layout by default (configured in `_config.yml` defaults).

## Front Matter Patterns

**Posts** (`_posts/`):
```yaml
---
title: "Post Title"
date: 2024-05-17
permalink: /posts/2024/slug
tags:
  - Mathematics
  - Machine Learning
toc: true          # optional, shows table of contents
header:
  teaser: /images/path/image.png   # optional, used in card previews
---
```

**Readings** (`_readings/`) and **Learnings** (`_learnings/`):
```yaml
---
title: "Title"
colllection: readings    # NOTE: intentional 3-l typo ("colllection") used in existing files
type: "Deep Learning"
venue: "Ha Noi"
date: 2024-02-07
permalink: /readings/2024/slug/
tags:
  - Deep Learning
---
```

**Collections** (`_collections/`) and **Journeys** (`_journeys/`):
```yaml
---
title: 'Event Title'
excerpt: "<br/><img src='/images/path/cover.jpg'>"  # HTML image shown on archive cards
collection: collections
type: "collections"
venue: "Mùa hạ, Hà Nội"
date: 2024-07-30
tags:
  - Travel
---
```
These are media-heavy: body content uses inline HTML `<img>` tags and `<video controls>` elements for galleries.

## Templating

- `_layouts/` — `default.html` wraps everything; `single.html` for content pages; `archive.html` for list pages; also `splash.html`, `talk.html`, `archive-taxonomy.html`
- `_includes/` — Key reusable components: `blog-card.html`, `reading-card.html`, `collection-card.html`, `author-profile.html`, `archive-single.html`, `paginator.html`
- `_data/navigation.yml` — 6-item main nav: Blog Posts, Readings, Learnings, Collections, Running, CV

## Styling

- `assets/css/main.scss` — Entry point that imports all `_sass/` partials
- Custom partials: `_dark-mode.scss`, `_blog.scss`, `_collections.scss`, `_sidebar.scss`, `_cv.scss`, `_running.scss`, `_archive.scss`, `_footer.scss`, `_masthead.scss`, `_navigation.scss`, `_page.scss`, `_search.scss`
- Dark mode uses a toggle with `localStorage` persistence (`data-theme` attribute on `<html>`)

## JavaScript

- `assets/js/_main.js` — Source file; output is `assets/js/main.min.js`. **Always rebuild the bundle after editing `_main.js`.**
- Bundle concatenation order: jQuery 1.12.4 → fitvids → greedy-navigation → magnific-popup → smooth-scroll → stickyfill → `_main.js`
- Blog archive has tag-based filtering via JS
- MathJax is loaded for math equation support in posts
- Running page uses Leaflet.js (via unpkg CDN) for activity maps
- Search overlay uses Lunr.js (unpkg CDN) with a client-side index built from `search.json`

## Strava Integration

A running stats page at `/running/` displays activity data fetched from Strava automatically.

- `scripts/fetch_strava.py` — Fetches last 16 weeks of Strava activities, processes GPS polylines, and generates aggregated stats
- `_data/strava.json` — Auto-generated data file (288KB+), committed daily by CI; **do not edit manually**
- `_pages/running.html` — Page layout that reads `strava.json` and renders charts/maps
- `_sass/_running.scss` — Styles for the running page

**GitHub Actions** (`.github/workflows/sync-strava.yml`):
- Runs daily at 05:00 UTC (or manually via `workflow_dispatch`)
- Requires three repository secrets: `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, `STRAVA_REFRESH_TOKEN`
- Auto-commits updates to `_data/strava.json` with `[skip ci]` to avoid build loops

## Search

Client-side full-text search powered by Lunr.js — no server required (suitable for GitHub Pages).

- `search.json` — Jekyll-generated index at repo root; includes title, url, tags, content (truncated 500 chars) for all `_posts/`
- `_includes/masthead.html` — Search toggle button + fullscreen overlay HTML (backdrop, modal, input, results list, footer hints)
- `_sass/_search.scss` — All overlay styles: backdrop blur, spring animation, result cards with tag pills and animated arrow, keyboard hint footer
- `_includes/scripts.html` — Lunr.js loaded from CDN before `main.min.js`
- Search logic in `assets/js/_main.js`: opens on button click or `Cmd+K`, supports `↑↓` keyboard navigation through results, `Enter` to follow, `Escape` to close

## Key Config Notes

- Pagination: 5 posts per page (jekyll-paginate)
- `_pages/` is included via `include:` directive (not auto-discovered)
- The `_projects/` directory exists but is not a configured Jekyll collection
- Plugins: jekyll-paginate, jekyll-sitemap, jekyll-gist, jekyll-feed, jekyll-redirect-from (all via `github-pages` gem)
- `_data/strava.json` is auto-generated — do not manually edit
