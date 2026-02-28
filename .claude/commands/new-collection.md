Create a new life/travel collection entry for this Jekyll site.

Collections always require TWO files: one in `_collections/` (the written narrative) and one in
`_journeys/` (the photo/video gallery), plus a shared image directory under `images/mylife/`.

## Steps

1. Ask the user for:
   - **Title** — event title (e.g. "Running - Quảng Bình International Marathon 2024")
   - **Excerpt** — short description shown on archive cards (Vietnamese or English)
   - **Venue** — location and season (e.g. "Mùa hạ, Hà Nội")
   - **Tags** — comma-separated (common: Travel, Running, Trekking, Hiking)
   - **Date** — default to today's date (YYYY-MM-DD) if not provided

2. Derive:
   - `slug` — lowercase, spaces/special chars → hyphens
   - `topic_name` — snake_case (hyphens → underscores)
   - `year` — 4-digit year from date
   - `cover_file` — placeholder filename: `cover.jpg`

3. Create `_collections/<date>-<slug>.md`:
   ```yaml
   ---
   title: '<title>'
   excerpt: "<excerpt> <br/><img src='/images/mylife/<year>/<topic_name>/<cover_file>'>"
   collection: collections
   type: "collections"
   venue: "<venue>"
   date: <date>
   permalink: /collections/<date>-<slug>/
   tags:
   <tags as yaml list>
   ---
   ```
   Body starter:
   ```html
   <head>
       <style type="text/css">
           figure{text-align: center;}
       </style>
   </head>

   ```

4. Create `_journeys/<date>-<slug>.md` with identical front matter except:
   - `collection: journeys`
   - `type: "journeys"`
   - `permalink: /journeys/<date>-<slug>/`

5. Create image directory: `images/mylife/<year>/<topic_name>/`
   with a `.gitkeep` file inside.

6. Print a summary showing all three created paths.
