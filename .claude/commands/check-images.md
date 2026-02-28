Audit all image path references in content files and report any that don't follow the
canonical structure: `/images/<tab>/<year>/<snake_case_topic>/<filename>`.

## What to check

Scan every `.md` file in: `_posts/`, `_readings/`, `_learnings/`, `_collections/`, `_journeys/`

For each `src=` attribute and `![...]()` markdown image, extract the path and check it against
these rules:

1. **Correct tab prefix** — path must start with one of:
   - `/images/posts/`
   - `/images/reading/`
   - `/images/learning/`
   - `/images/mylife/`
   - `/images/cv/` (exempt — flat structure is intentional)
   - `/images/profile/` (exempt — flat structure is intentional)

2. **Year segment present** — the segment after the tab prefix must be a 4-digit year
   (2021–2030). Flag paths like `/images/posts/ssd/` or `/images/posts/20231127_crnn/`
   that skip the year.

3. **Snake_case topic** — the topic segment must use underscores, not hyphens or
   date prefixes. Flag `/images/mylife/running-cat-ba-2024/` or `/images/posts/20240121_BERT/`.

4. **File actually exists** on disk — check that the referenced file path resolves under
   the repo root. Flag any reference where the file is missing.

## Output format

Group findings by content file. For each violation print:
- The content file path (relative to repo root)
- The offending image path
- The rule it violates
- A suggested corrected path where possible

At the end, print a summary:
- Total files scanned
- Total violations found
- Total missing files found

If everything is clean, print a success message.
