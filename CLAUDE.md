# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based personal blog and portfolio site hosted on GitHub Pages, built on a heavily customized Minimal Mistakes theme. Content is bilingual (English for technical posts, Vietnamese for personal content) and organized into five collection types.

## Build & Serve Commands

```bash
bundle install                                                   # Install Ruby dependencies
bundle exec jekyll serve                                         # Serve locally at localhost:4000
bundle exec jekyll serve --livereload                            # Serve with live reload (hawkins gem)
bundle exec jekyll serve --config _config.yml,_config.dev.yml   # Serve with dev overrides
bundle exec jekyll build                                         # Build static site to _site/
npm run build:js                                                 # Minify JS to assets/js/main.min.js
npm run watch:js                                                 # Watch and auto-rebuild JS
```

Use `_config.dev.yml` for local development — it disables analytics, uses `localhost:4000` as URL, and sets SASS to `expanded` output for easier debugging.

## Content Architecture

**Five collection types** (all use Markdown with YAML front matter):

| Directory | Purpose | Filename format |
|-----------|---------|-----------------|
| `_posts/` | Technical AI/ML blog posts | `YYYY-MM-DD-slug.md` |
| `_readings/` | Book and article reviews | `YYYY-MM-DD-slug.md` |
| `_learnings/` | Course certificates and summaries | `YYYYMMDDname.md` (no dashes) |
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

- `_layouts/` — `default.html` wraps everything; `single.html` for content pages; `archive.html` for list pages
- `_includes/` — Key reusable components: `blog-card.html`, `collection-card.html`, `author-profile.html`, `archive-single.html`
- `_data/navigation.yml` — Flat 5-item main nav: Blog Posts, Readings, Learnings, Collections, CV

## Styling

- `assets/css/main.scss` — Entry point that imports all `_sass/` partials
- Custom partials: `_dark-mode.scss`, `_blog.scss`, `_collections.scss`, `_sidebar.scss`, `_cv.scss`
- Dark mode uses a toggle with `localStorage` persistence

## JavaScript

- `assets/js/_main.js` — Source file; output is `assets/js/main.min.js`
- `npm run build:js` concatenates and minifies: jQuery 1.12.4 + plugins (fitvids, greedy-navigation, magnific-popup, smooth-scroll, stickyfill) + `_main.js`
- Blog archive has tag-based filtering via JS
- MathJax is loaded for math equation support in posts

## Key Config Notes

- Pagination: 5 posts per page (jekyll-paginate)
- `_pages/` is included via `include:` directive (not auto-discovered)
- The `_projects/` directory exists but is not a configured Jekyll collection
- Plugins: jekyll-paginate, jekyll-sitemap, jekyll-gist, jekyll-feed, jekyll-redirect-from (all via `github-pages` gem)
