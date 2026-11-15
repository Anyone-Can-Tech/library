#!/usr/bin/env python3
"""Generate per-chapter contributor credits from git history.

Runs as a Quarto pre-render step from inside a book folder (for example
books/homelab). For every chapter and appendix it reads the commit history of
the chapter file plus its matching labs/ folder, then writes a small Markdown
snippet to _credits/<chapter>.md that the chapter includes on its welcome page.

Credit rules:
  - The first person to commit to a chapter is credited as "Written by".
  - Everyone after that is "Edited by", in order of their first contribution.
  - Co-authored-by trailers count as contributions.
  - Edits to shared modules a chapter includes count for that chapter.
  - Bots (Renovate, Dependabot, GitHub Actions) are skipped.
  - Names are resolved through the repo's .mailmap, so contributors can choose
    how their name appears.
  - Non-commit help (testing, reviews, art) comes from contributors.json.
  - The chapter's last-verified and tested-with front matter is shown too.

The script only uses the Python standard library so it runs anywhere Quarto does.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

BOOK_DIR = Path.cwd()
OUT_DIR = BOOK_DIR / "_credits"
CONTENT_DIRS = ("chapters", "appendices")
LABS_DIR = BOOK_DIR / "labs"
EXTRA_FILE = BOOK_DIR / "contributors.json"

BOT_PATTERN = re.compile(r"\[bot\]|renovate|dependabot|github-actions", re.IGNORECASE)
NOREPLY_PATTERN = re.compile(r"^(?:\d+\+)?([A-Za-z0-9-]+)@users\.noreply\.github\.com$", re.IGNORECASE)
TRAILER_PATTERN = re.compile(r"^\s*(.+?)\s*<([^>]+)>\s*$")

FIELD_SEP = "\x1f"
RECORD_SEP = "\x1e"


@dataclass
class Person:
    name: str
    email: str = ""
    github: str | None = None

    @property
    def key(self) -> str:
        return (self.github or self.email or self.name).lower()


@dataclass
class Credits:
    written_by: list[Person] = field(default_factory=list)
    edited_by: list[Person] = field(default_factory=list)
    helped_by: list[tuple[Person, str]] = field(default_factory=list)


def git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=BOOK_DIR, capture_output=True, text=True, check=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def github_handle(email: str) -> str | None:
    match = NOREPLY_PATTERN.match(email.strip())
    return match.group(1) if match else None


def people_from_history(paths: list[Path]) -> list[Person]:
    """Return everyone who touched these paths, oldest contribution first."""
    rel = [os.path.relpath(p, BOOK_DIR) for p in paths if p.exists()]
    if not rel:
        return []
    fmt = FIELD_SEP.join(["%aN", "%aE", "%(trailers:key=Co-authored-by,valueonly,separator=%x1d)"])
    log = git("log", "--reverse", "--use-mailmap", f"--format={fmt}{RECORD_SEP}", "--", *rel)

    seen: dict[str, Person] = {}
    order: list[Person] = []

    def add(name: str, email: str) -> None:
        name, email = name.strip(), email.strip()
        if not name or BOT_PATTERN.search(name) or BOT_PATTERN.search(email):
            return
        person = Person(name=name, email=email, github=github_handle(email))
        if person.key not in seen:
            seen[person.key] = person
            order.append(person)

    for record in log.split(RECORD_SEP):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split(FIELD_SEP)
        if len(parts) < 2:
            continue
        add(parts[0], parts[1])
        if len(parts) > 2:
            for trailer in parts[2].split("\x1d"):
                match = TRAILER_PATTERN.match(trailer)
                if match:
                    add(match.group(1), match.group(2))
    return order


def load_extra() -> dict:
    if not EXTRA_FILE.exists():
        return {}
    try:
        return json.loads(EXTRA_FILE.read_text(encoding="utf-8")).get("chapters", {})
    except json.JSONDecodeError as err:
        print(f"credits: could not parse {EXTRA_FILE.name}: {err}", file=sys.stderr)
        return {}


def link(person: Person) -> str:
    if person.github:
        return f"[{person.name}](https://github.com/{person.github})"
    return person.name


def avatars(people: list[Person]) -> str:
    imgs = [
        f"[![{p.name}](https://github.com/{p.github}.png?size=64){{.credit-avatar}}](https://github.com/{p.github})"
        for p in people
        if p.github
    ]
    return " ".join(imgs)


INCLUDE_PATTERN = re.compile(r"\{\{<\s*include\s+(\S*shared/modules/\S+)\s*>\}\}")


def shared_modules(chapter: Path) -> list[Path]:
    """Shared modules a chapter includes, so their contributors get credit too."""
    text = chapter.read_text(encoding="utf-8")
    return [(chapter.parent / m).resolve() for m in INCLUDE_PATTERN.findall(text)]


FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def verification(chapter: Path) -> str:
    """Read last-verified and tested-with from the chapter's front matter."""
    match = FRONT_MATTER.match(chapter.read_text(encoding="utf-8"))
    if not match:
        return ""
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"\'')
    parts = []
    if fields.get("last-verified"):
        parts.append(f"Last verified: {fields['last-verified']}")
    if fields.get("tested-with"):
        parts.append(f"Tested with: {fields['tested-with']}")
    return " · ".join(parts)


def render(credits: Credits, verified: str = "") -> str:
    meta = f"\n[{verified}]{{.chapter-meta}}\n" if verified else ""
    if not (credits.written_by or credits.edited_by or credits.helped_by):
        return (
            "::: {.chapter-credits}\n"
            "This chapter is waiting for its first contributor. "
            "See [Your First Contribution](/appendices/a-your-first-contribution.qmd) "
            "to put your name here.\n"
            + meta
            + ":::\n"
        )

    lines = ["::: {.chapter-credits}"]
    everyone = credits.written_by + credits.edited_by + [p for p, _ in credits.helped_by]
    face_row = avatars(everyone)
    if face_row:
        lines += ["::: {.content-visible when-format=\"html\"}", face_row, ":::", ""]
    if credits.written_by:
        lines.append("**Written by** " + ", ".join(link(p) for p in credits.written_by) + "  ")
    if credits.edited_by:
        lines.append("**Edited by** " + ", ".join(link(p) for p in credits.edited_by) + "  ")
    if credits.helped_by:
        helped = ", ".join(f"{link(p)} ({role})" for p, role in credits.helped_by)
        lines.append("**With help from** " + helped + "  ")
    if meta:
        lines.append(meta)
    lines.append(":::")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    extra = load_extra()

    chapter_files = sorted(
        f for d in CONTENT_DIRS for f in (BOOK_DIR / d).glob("*.qmd") if (BOOK_DIR / d).exists()
    )
    for chapter in chapter_files:
        stem = chapter.stem
        history = people_from_history([chapter, LABS_DIR / stem, *shared_modules(chapter)])

        credits = Credits()
        if history:
            credits.written_by = history[:1]
            credits.edited_by = history[1:]

        listed = {p.key for p in history}
        for entry in extra.get(stem, []):
            person = Person(name=entry.get("name", ""), github=entry.get("github"))
            if person.name and person.key not in listed:
                credits.helped_by.append((person, entry.get("role", "contributor")))

        (OUT_DIR / f"{stem}.md").write_text(render(credits, verification(chapter)), encoding="utf-8")

    print(f"credits: wrote {len(chapter_files)} credit blocks to {OUT_DIR.name}/")


if __name__ == "__main__":
    main()
