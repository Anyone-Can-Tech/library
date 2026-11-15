# Contributing

Thanks for helping. These books exist to make technology less intimidating, and that applies to contributing too. If this is your first pull request ever, you're in the right place.

Every change comes in as a pull request from a fork. Issues are turned off, so if you spot a problem, the way to report it is to fix it. Not sure how? Open a draft pull request with what you have and say what's wrong. We'll help from there.

## The quick way: edit in your browser

Every page on the book's website has an **Edit this page** link. It opens the file on GitHub, which forks the repo and opens a pull request for you in a few clicks. Great for typos and small fixes.

## The full way: fork, branch, pull request

1. Fork this repo on GitHub and clone your fork.
2. Create a branch for your change: `git switch -c fix-chapter-6-typo`. One topic per branch, and never work on `main`.
3. Preview the book while you edit: `cd books/homelab && quarto preview`
4. Commit with a short, clear message and push the branch to your fork.
5. Open a pull request from your branch to `main` on this repo and fill in the template.
6. Answer review comments by pushing more commits to the same branch.

If `main` moves while you work, sync your fork's `main` on GitHub and rebase your branch onto it.

## Using AI tools

AI assistants and agents are welcome here. Use whatever helps you write, edit or test. The rule is simple: **the human who opens the pull request is responsible for it**, no matter how it was made.

That means before you open a pull request you have:

- Read every line of the change and can explain why it's there.
- Checked every fact, command, version number and link yourself. AI tools make up plausible commands and options. In a book for beginners, one wrong command can break a reader's computer.
- Run any lab you changed, on a real machine.
- Made sure it follows the [writing style](#writing-style) below and sounds like the rest of the book.
- Stayed around to answer review comments yourself. An agent can push fixes, but a person has to be accountable for them.

We will close pull requests that are low effort, unhelpful or make the books worse. That includes bulk rewrites nobody asked for, generic filler, made-up facts and changes the author clearly didn't review. How it was made doesn't matter. What it does to the book does.

- **First time:** we close the pull request and leave a warning explaining why.
- **After that:** we block the account from contributing.

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
