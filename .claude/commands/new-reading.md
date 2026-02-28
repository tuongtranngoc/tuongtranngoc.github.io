Create a new reading note entry for this Jekyll site.

## Steps

1. Ask the user for:
   - **Title** — book or article title
   - **Type** — category string (e.g. "Deep Learning", "Running", "Self-help")
   - **Venue** — location/context (e.g. "Hà Nội", "Online")
   - **Tags** — comma-separated list
   - **Date** — default to today's date (YYYY-MM-DD) if not provided

2. Derive from the title:
   - `slug` — lowercase, spaces → hyphens, no special chars, strip Vietnamese diacritics if needed
   - `topic_name` — snake_case version (hyphens → underscores)
   - `year` — 4-digit year from the date

3. Create the file at `_readings/<date>-<slug>.md` with this front matter:
   ```yaml
   ---
   title: "<title>"
   colllection: readings
   type: "<type>"
   venue: "<venue>"
   date: <date>
   permalink: /readings/<year>/<slug>/
   tags:
   <tags as yaml list>
   header:
     teaser: /images/reading/<year>/<topic_name>/cover.png
   ---
   ```
   Note: `colllection` has three l's — this is intentional, matching the existing convention.

   Then add a starter body:
   ```html
   <head>
       <style type="text/css">
           figure{text-align: center;}
       </style>
   </head>

   ## Summary

   ```

4. Create the image directory: `images/reading/<year>/<topic_name>/`
   with a `.gitkeep` file inside.

5. Print a summary showing the new file path and image directory path.
