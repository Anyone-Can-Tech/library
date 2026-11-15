# Shared

Tooling and content used by every book in the series.

- `scripts/credits.py` runs before each build and writes the contributor credits for every chapter, using git history plus the book's `contributors.json`.
- `shortcodes/credits.lua` provides `{{< credits chapter-file-name >}}`, which places those credits at the top of a chapter.
- `filters/include-code.lua` fills a code block from a file, for example `{.yaml include="labs/06-ad-blocking/compose.yaml"}`.
- `partials/` holds snippets included in many chapters, like the sponsor note.
- `styles/series.scss` is the shared look for all the books.

Shared lessons that appear in more than one book (the terminal, git, config files) will also live here, so they're written once and stay in sync.
