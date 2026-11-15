# Contributing

Thanks for helping. These books exist to make technology less intimidating, and that applies to contributing too. If this is your first pull request ever, you're in the right place.

## The quick way: edit in your browser

Every page on the book's website has an **Edit this page** link. It opens the file on GitHub, where you can make a change and propose it in a few clicks. Great for typos and small fixes.

## The full way: work locally

1. Fork this repo and clone your fork.
2. Create a branch: `git switch -c fix-chapter-6-typo`
3. Preview the book while you edit: `cd books/homelab && quarto preview`
4. Commit with a short, clear message, then push and open a pull request.

## How you get credited

Each chapter opens with the names of the people who wrote and edited it. The list is built from git history every time the book is published, so you show up automatically once your pull request is merged.

- The first person to commit to a chapter is listed as **Written by**. Everyone after is **Edited by**.
- Pairing with someone? Add a `Co-authored-by: Name <email>` line to your commit message and they get credit too.
- Commit with your GitHub noreply email (`12345+you@users.noreply.github.com`) and your avatar shows up next to your name.
- Want your name shown differently? Add a line to [.mailmap](.mailmap).
- Helped without committing (tested a lab, reviewed a chapter, drew a diagram)? A maintainer will add you to that book's `contributors.json`.

## Writing style

- Write for someone who has never opened a terminal. Define every term the first time it shows up.
- Use short sentences and plain words. Talk to the reader as "you".
- No em dashes. Use a period, a comma or parentheses instead.
- Every chapter teaches one big idea. Keep detours in callout boxes.

### Personal stories

Each book has a foreword written by the series creator. Everywhere else, the book speaks with one shared voice, so anyone can edit any chapter.

Have a story that would help a reader? Add it as a **Field note**, credited to you:

```markdown
::: {.callout-note}
## Field note from Your Name
The time my router's DNS settings took down the whole house...
:::
```

Keep field notes short, true and useful. Other contributors can tighten the wording, but the story stays yours.

### Callout boxes

| Box | Use it for | Markdown |
|---|---|---|
| Concept box | Connecting the project to everyday tech | `::: {.callout-note}` with a `## Concept box: ...` title |
| Break it on purpose | A safe way to break and fix what was just built | `::: {.callout-warning}` |
| Level up | End-of-part checkpoint | `::: {.callout-tip}` |

## Labs

- Every lab lives in `books/<book>/labs/<chapter-file-name>/` and must include `compose.yaml`.
- Pin image versions (`pihole/pihole:2026.11.0`, never `latest`). Renovate opens a pull request when a new version ships.
- Put settings readers must change in `.env.example`, and never commit a real `.env`.
- Add a `test.sh` smoke test so CI can boot the lab and check it works. If a port conflicts with the CI runner, add a `compose.ci.yaml` override.
- Show lab files in the chapter with an include, so the book always matches the tested file:

  ````markdown
  ```{.yaml include="labs/06-ad-blocking/compose.yaml" filename="compose.yaml"}
  ```
  ````

- When you change a lab, run it yourself and update the chapter's `last-verified` date.
