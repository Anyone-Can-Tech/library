::: {.callout-important}
## Draft
This appendix is an outline. Fittingly, you could help write it. It's shared by every Anyone Can book, so one fix improves them all.
:::

## Goal

Turn readers into contributors. Fix something in this book and see your name on the chapter page.

## The big idea

Version control and open source collaboration: git, GitHub, forks, branches and pull requests.

## Outline

- What git is: a time machine and a paper trail for files
- Why this book lives in git, and how the chapter credits work
- Making a GitHub account
- The easy path: the **Edit this page** link on every page of this site
- The real path: fork, clone, branch, edit, commit, push
- Opening a pull request and what happens during review
- Finding something to fix: typos, outdated versions, a lab that no longer works
- Seeing your name on the chapter welcome page after the next build

## How chapter credits work

Every chapter opens with the names of the people who wrote and edited it. Those credits are built automatically from the book's git history each time the site is published:

- The first person to commit to a chapter is credited as **Written by**
- Everyone after that is credited as **Edited by**
- `Co-authored-by:` lines in commit messages count too
- Help that doesn't show up in commits, like testing a lab or drawing a diagram, is listed in `contributors.json`
- Want your name to appear differently? Add yourself to the `.mailmap` file at the root of the repo
