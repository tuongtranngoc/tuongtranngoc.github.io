Create a new technical blog post for this Jekyll site.

## Steps

1. Ask the user for:
   - **Title** — the post title (human-readable)
   - **Tags** — comma-separated list (e.g. "Machine Learning, Deep Learning")
   - **Date** — default to today's date (YYYY-MM-DD) if not provided
   - **TOC** — whether to include a table of contents (default: true)

2. Derive from the title:
   - `slug` — lowercase, spaces replaced with hyphens, no special chars
   - `topic_name` — lowercase snake_case version of the slug (hyphens → underscores)
   - `year` — 4-digit year from the date

3. Create the post file at `_posts/<date>-<slug>.md` with this front matter:
   ```yaml
   ---
   title: "<title>"
   date: <date>
   permalink: /posts/<year>/<slug>/
   tags:
   <tags as yaml list>
   toc: true
   header:
     teaser: /images/posts/<year>/<topic_name>/cover.png
   ---
   ```
   Then add a starter body:
   ```html
   <head>
       <style type="text/css">
           figure{text-align: center;}
           math{text-align: center;}
       </style>
   </head>

   ## Introduction

   ```

4. Create the image directory: `images/posts/<year>/<topic_name>/`
   (create a `.gitkeep` file inside so git tracks it)

5. Print a summary showing:
   - Path to the new post file
   - Path to the image directory
   - Reminder to rebuild JS if `_main.js` was touched
