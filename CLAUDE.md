# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based personal blog and portfolio site hosted on GitHub Pages, built on a heavily customized Minimal Mistakes theme. The site serves as a blog for an AI engineer, with content organized into posts, readings, collections (life experiences), and journeys.

## Build & Serve Commands

```bash
bundle install                                          # Install Ruby dependencies
bundle exec jekyll serve                                # Serve locally at localhost:4000
bundle exec jekyll serve --config _config.yml,_config.dev.yml  # Serve with dev overrides
bundle exec jekyll build                                # Build static site to _site/
npm run build:js                                        # Minify JS to assets/js/main.min.js
```

Use `_config.dev.yml` for local development (disables analytics, uses localhost URL, expanded SASS output).

## Architecture

**Content types** (all use Markdown with YAML front matter):
- `_posts/` — Blog posts (filename format: `YYYY-MM-DD-slug.md`)
- `_collections/` — Life experiences (travel, trekking, sports)
- `_reading/` — Book/article reviews
- `_journeys/` — Trip documentation

**Templating**:
- `_layouts/` — Liquid templates (`default.html` → `single.html` for content pages, `archive.html` for lists)
- `_includes/` — Reusable components (masthead, author-profile, blog-card, collection-card, pagination, comments)
- `_data/navigation.yml` — Site navigation menu structure

**Styling**:
- `assets/css/main.scss` — Entry point, imports all partials from `_sass/`
- `_sass/` — SCSS partials; key custom files: `_dark-mode.scss`, `_blog.scss`, `_collections.scss`, `_sidebar.scss`, `_cv.scss`
- Dark mode toggle with localStorage persistence

**JavaScript**:
- `assets/js/_main.js` — Source JS; minified output at `assets/js/main.min.js`
- Blog archive has tag-based filtering via JS

**Key integrations**: MathJax (math equations), Font Awesome icons, Academic Icons, jQuery, MagnificPopup.

## Post Front Matter

Posts typically include: `title`, `date`, `permalink`, `tags`, `toc` (optional), `header.teaser` (for card images).

## Config

`_config.yml` controls: site metadata, collections, pagination (5 per page), defaults for layouts/author, plugin list (jekyll-paginate, jekyll-sitemap, jekyll-gist, jekyll-feed, jekyll-redirect-from).
