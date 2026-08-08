"""
One-time content migration: rewrite hardcoded cross-reference links between
notebooks (e.g. "find more exercises here: <link>") that point at the old
Jupyter Book v1 (Sphinx) page URL scheme - https://introcp.github.io/src/
<chapter>/<name>.html - to the v2 (mystmd) scheme, where every page is served
at a flat slug derived from its filename: https://introcp.github.io/<slug>.

Does NOT touch links to .ipynb/.pdf/.slides.html (those still live at the
old /src/<chapter>/<name> path on purpose - see finalize-website.py).

Safe to run once; re-running is a no-op.
"""
import glob
import json
import os
import re

OLD_LINK = re.compile(
    r'https://introcp\.github\.io/src/[A-Za-z0-9]+/([A-Za-z0-9._-]+)\.html\b'
)


def slug_for(filename_no_ext):
    return filename_no_ext.lower()


def rewrite(text):
    def repl(m):
        name = m.group(1)
        if name.endswith(".slides"):
            return m.group(0)  # leave slide deck links alone
        return f"https://introcp.github.io/{slug_for(name)}"
    return OLD_LINK.sub(repl, text)


def main():
    changed = 0

    for path in sorted(glob.glob("src/*/*.ipynb")):
        with open(path) as f:
            nb = json.load(f)

        touched = False
        for cell in nb["cells"]:
            if cell.get("cell_type") != "markdown":
                continue
            new_source = [rewrite(line) for line in cell["source"]]
            if new_source != cell["source"]:
                cell["source"] = new_source
                touched = True

        if touched:
            with open(path, "w") as f:
                json.dump(nb, f, indent=1)
                f.write("\n")
            print("Fixed links in:", path)
            changed += 1

    for path in sorted(glob.glob("src/*.md")):
        with open(path) as f:
            text = f.read()
        new_text = rewrite(text)
        if new_text != text:
            with open(path, "w") as f:
                f.write(new_text)
            print("Fixed links in:", path)
            changed += 1

    print(f"\n{changed} file(s) migrated.")


if __name__ == "__main__":
    main()
