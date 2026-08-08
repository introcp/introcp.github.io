"""
One-time content migration: strip the inline-HTML title/subtitle wrappers
(`# <b style="font-family: 'LUISS', 'Lato'">Text</b>`, `<h2 style="...">Text</h2>`,
`<h3 style="...">Text</h3>`) used across chapter title cells and replace them
with plain Markdown headings.

Under Jupyter Book v1 (Sphinx), raw HTML in a heading rendered fine. Under
Jupyter Book v2 (mystmd), the first heading's raw source text is lifted
verbatim into the page's `title` frontmatter (a plain string), so the HTML
tags show up literally instead of being rendered - hence this cleanup.
The LUISS/Lato font previously applied per-heading via inline `style=` is now
applied site-wide in _static/custom.css instead.

Safe to run once; re-running is a no-op since the patterns it looks for
won't be present anymore after the first pass.
"""
import glob
import json
import re

PATTERNS = [
    (re.compile(r'^(#+)\s*<b style="font-family: \'LUISS\', \'Lato\'">(.*?)</b>\s*\n?$'), r'\1 \2\n'),
    (re.compile(r'^<h2 style="font-family: \'LUISS\', \'Lato\'">(.*?)</h2>\s*\n?$'), r'## \1\n'),
    (re.compile(r'^<h3 style="font-family: \'LUISS\', \'Lato\'">(.*?)</h3>\s*\n?$'), r'### \1\n'),
]


def clean_line(line):
    for pattern, repl in PATTERNS:
        m = pattern.match(line)
        if m:
            return pattern.sub(repl, line)
    return line


def migrate_notebook(path):
    with open(path) as f:
        nb = json.load(f)

    touched = False
    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        new_source = [clean_line(line) for line in cell["source"]]
        if new_source != cell["source"]:
            cell["source"] = new_source
            touched = True

    if touched:
        with open(path, "w") as f:
            json.dump(nb, f, indent=1)
            f.write("\n")
    return touched


def migrate_markdown(path):
    with open(path) as f:
        lines = f.readlines()

    new_lines = [clean_line(line) for line in lines]
    if new_lines == lines:
        return False

    with open(path, "w") as f:
        f.writelines(new_lines)
    return True


def main():
    changed = 0
    for path in sorted(glob.glob("src/*/*.ipynb")):
        if migrate_notebook(path):
            print("Migrated:", path)
            changed += 1

    for path in sorted(glob.glob("src/*.md")) + sorted(glob.glob("src/*/*.md")):
        if migrate_markdown(path):
            print("Migrated:", path)
            changed += 1

    print(f"\n{changed} file(s) migrated.")


if __name__ == "__main__":
    main()
