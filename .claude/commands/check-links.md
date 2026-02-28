Check all internal image and teaser references in content files for broken links
(i.e. the referenced file does not exist on disk).

## What to check

Scan every `.md` file in: `_posts/`, `_readings/`, `_learnings/`, `_collections/`, `_journeys/`

For each of the following, resolve the path against the repo root and verify the file exists:

1. **`header.teaser`** front matter field — e.g. `/images/posts/2024/bert/cover.png`
2. **`header.image`** front matter field
3. **`excerpt:` inline img src** — the image embedded in the excerpt string
4. **All `src=` attributes** in body HTML (`<img>`, `<video>`)
5. **All `![alt](path)` markdown images** in body content

## Output format

For each broken reference, print:
- Content file (relative to repo root)
- The broken path
- Type of reference (teaser / excerpt / body img / body video)

At the end, print a summary:
- Total files scanned
- Total broken references found

If all references resolve correctly, print a success message.

## Notes

- Ignore external URLs (starting with `http://` or `https://`)
- Ignore paths starting with `/images/cv/` and `/images/profile/` only if those
  directories actually exist (they are intentionally flat)
- Do not follow Jekyll permalink logic — only check whether the raw file path exists
  relative to the repo root
