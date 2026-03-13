# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based personal blog and portfolio site hosted on GitHub Pages, built on a heavily customized Minimal Mistakes theme. Content is bilingual (English for technical posts, Vietnamese for personal content) and organized into five collection types. Includes a Running stats page powered by automated Strava integration.

## Build & Serve Commands

### Common Tasks

Use the **Claude Code skills** for quick operations:
- `/serve` — Start local Jekyll dev server with live reload
- `/build-js` — Rebuild minified JavaScript bundle after editing `assets/js/_main.js`
- `/check-links` — Validate all internal image and teaser references
- `/check-images` — Audit image paths for compliance with naming conventions
- `/new-post` — Create a new technical blog post
- `/new-reading` — Create a new reading note entry
- `/new-collection` — Create a new life/travel collection entry

### Manual Commands

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

> After `npm install`, `npm run build:js` (alias: `npm run uglify`) works using the local `uglify-js` devDependency. Alternatively, use `npx uglify-js ...` without installing.

### Development Configuration

Use `_config.dev.yml` for local development. It overrides the production settings:
- **URL**: `http://localhost:4000` (instead of production domain)
- **Analytics**: Disabled (provider set to `false`)
- **Comments**: Uses dev Disqus shortname
- **SASS output**: `expanded` style (instead of `compressed`) for easier CSS debugging

Load it alongside the main config: `bundle exec jekyll serve --config _config.yml,_config.dev.yml`

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
  teaser: /images/posts/2024/topic_name/cover.png   # optional, used in card previews
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
excerpt: "<br/><img src='/images/mylife/2024/topic_name/cover.jpg'>"  # HTML image shown on archive cards
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
- Runs every hour at the top of the hour (via `cron: "0 * * * *"`) and can be triggered manually via `workflow_dispatch`
- Requires three repository secrets set in GitHub repo settings:
  - `STRAVA_CLIENT_ID` — Numeric app ID from Strava API settings page
  - `STRAVA_CLIENT_SECRET` — Secret from the same Strava API settings
  - `STRAVA_REFRESH_TOKEN` — Obtained via OAuth flow (see workflow file comments for one-time setup instructions)
- Auto-commits updates to `_data/strava.json` with `[skip ci]` to avoid infinite build loops
- Only commits if the file has changed (checks with `git diff --quiet`)

## Search

Client-side full-text search powered by Lunr.js — no server required (suitable for GitHub Pages).

- `search.json` — Jekyll-generated index at repo root; includes title, url, tags, content (truncated 500 chars) for all `_posts/`
- `_includes/masthead.html` — Search toggle button + fullscreen overlay HTML (backdrop, modal, input, results list, footer hints)
- `_sass/_search.scss` — All overlay styles: backdrop blur, spring animation, result cards with tag pills and animated arrow, keyboard hint footer
- `_includes/scripts.html` — Lunr.js loaded from CDN before `main.min.js`
- Search logic in `assets/js/_main.js`: opens on button click or `Cmd+K`, supports `↑↓` keyboard navigation through results, `Enter` to follow, `Escape` to close

## Image Path Conventions

All images must follow the canonical structure `/images/<tab>/<year>/<snake_case_topic>/<filename>`:

| Tab prefix | Used by |
|------------|---------|
| `/images/posts/` | `_posts/` |
| `/images/reading/` | `_readings/` |
| `/images/learning/` | `_learnings/` |
| `/images/mylife/` | `_collections/` and `_journeys/` |
| `/images/cv/` | CV page (flat structure, exempt from year/topic rules) |
| `/images/profile/` | Author profile (flat structure, exempt) |

Rules enforced by `/check-images`:
- Year segment must be 4 digits (2021–2030) immediately after the tab prefix
- Topic segment must be `snake_case` (underscores, not hyphens, no date prefixes)
- Each new content entry gets its own image directory with a `.gitkeep` to track it in git

Example: a post about BERT written in 2024 → `/images/posts/2024/bert/cover.png`

Collections always require **two paired files**: one in `_collections/` (narrative) and one in `_journeys/` (photo gallery), sharing the same `images/mylife/<year>/<topic>/` directory.

## Local Testing & Validation

**Always test locally before committing:**
1. Start the dev server with live reload: `bundle exec jekyll serve --config _config.yml,_config.dev.yml --livereload`
2. Visit http://localhost:4000 and verify your changes render correctly
3. Check browser console for JavaScript errors
4. If you modified `assets/js/_main.js`, rebuild the bundle: `npm run build:js`
5. Use `/check-links` and `/check-images` skills to validate references before pushing

**For new content:**
- Use the `/new-post`, `/new-reading`, or `/new-collection` skills to scaffold properly with correct front matter
- Always include a teaser image in the canonical path (e.g., `/images/posts/2024/topic_name/cover.png`)
- Test tag filtering on the archive page — click tags to ensure they filter correctly

**For Strava integration testing:**
- The workflow requires valid secrets to run — cannot be tested locally without credentials
- Commits to `_data/strava.json` happen hourly in production
- To test locally, you would need to copy a sample `_data/strava.json` and verify the `/running/` page renders correctly with the data

## Key Config Notes

- Pagination: 5 posts per page (jekyll-paginate)
- `_pages/` is included via `include:` directive (not auto-discovered)
- The `_projects/` directory exists but is not a configured Jekyll collection
- Plugins: jekyll-paginate, jekyll-sitemap, jekyll-gist, jekyll-feed, jekyll-redirect-from (all via `github-pages` gem)
- `_data/strava.json` is auto-generated — **do not manually edit** (updated hourly by GitHub Actions)
