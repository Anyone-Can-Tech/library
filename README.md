# Anyone Can Tech Library

Free, open books that teach technical literacy by building real things.

| Book | Status | Read it |
|---|---|---|
| **Anyone Can Homelab** | Outline, chapter 6 lab tested | [anyonecanhomelab.com](https://anyonecanhomelab.com) |
| **Anyone Can Code** | Outline, chapter 1 drafted | |
| **Anyone Can Linux** | Outline, chapter 1 drafted | |
| **Anyone Can Network** | Outline, chapter 1 drafted | |
| **Anyone Can Protect** | Outline, chapter 1 drafted | |

## What's in this repo

```
books/
  code/ linux/ network/ protect/   The other books, same layout as homelab
  homelab/            Anyone Can Homelab
    _quarto.yml       Book config and chapter order
    index.qmd         Welcome page
    chapters/         One file per chapter
    appendices/
    labs/             Docker Compose labs, one folder per chapter, tested in CI
    contributors.json Credit for help that isn't a commit (testing, art, reviews)
    CHANGELOG.md
shared/               Used by every book in the series
  scripts/credits.py  Builds chapter credits from git history
  shortcodes/         {{< credits >}} shortcode for chapter credits
  filters/            Pulls lab files into code blocks
  modules/            Lessons shared by several books, like Your First Contribution
  partials/           Reusable snippets, like the sponsor note
  styles/             Series look and feel
```

The books are written in Markdown and built with [Quarto](https://quarto.org), which turns the same files into a website, a PDF and an EPUB.

## Build a book locally

1. [Install Quarto](https://quarto.org/docs/get-started/) (1.11 or newer) and Python 3.
2. From the book's folder, start a live preview:

   ```sh
   cd books/homelab
   quarto preview
   ```

3. To build every format (website, PDF and EPUB) into `_book/`:

   ```sh
   quarto render
   ```

## Run a lab

Each lab is a self-contained Docker Compose project:

```sh
cd books/homelab/labs/06-ad-blocking
cp .env.example .env    # then edit .env
docker compose up -d
```

## Contributing

Typo fixes count, and every contributor gets credited by name on the chapters they touch. Start with [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The book text is [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) and the lab code and build tooling are [MIT](LICENSES/MIT.txt). See [LICENSE.md](LICENSE.md) for details.

## Support

The books are free and will stay that way. If they help you, you can [sponsor the project](https://github.com/sponsors/Anyone-Can-Tech).
