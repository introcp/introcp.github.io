#!/usr/bin/env python3
"""
mystmd's static export emits a separate content-hashed copy of a notebook
for every path it discovers it through (page render, raw-download link,
self-crawl snapshot, etc.), even when nothing differs. Confirmed on a fully
clean `jupyter-book build --html`: many notebooks end up with several
byte-for-byte-identical copies under different hashes (e.g. P12/P13/P14 each
5x). Not a correctness bug - just wasted files riding into docs/ and git.

This collapses each group of structurally-identical docs/build/*.ipynb files
down to one canonical copy, then rewrites every reference to a removed
filename (across all text assets in docs/) to point at the survivor.

Must run AFTER finalize-website.py, since that step is what populates docs/.
"""
import glob
import json
import os
import sys

TEXT_EXTENSIONS = {".json", ".html", ".js", ".css", ".xml", ".txt"}


def main(docs_dir):
    build_dir = os.path.join(docs_dir, "build")
    groups = {}
    for path in glob.glob(os.path.join(build_dir, "*.ipynb")):
        prefix = path.rsplit("-", 1)[0]
        groups.setdefault(prefix, []).append(path)

    renames = {}  # old basename -> canonical basename
    removed = 0
    for prefix, paths in groups.items():
        if len(paths) < 2:
            continue
        by_content = {}
        for path in sorted(paths):
            with open(path) as f:
                key = json.dumps(json.load(f), sort_keys=True)
            by_content.setdefault(key, []).append(path)
        for content_paths in by_content.values():
            if len(content_paths) < 2:
                continue
            canonical = content_paths[0]
            for dup in content_paths[1:]:
                renames[os.path.basename(dup)] = os.path.basename(canonical)
                os.remove(dup)
                removed += 1

    if not renames:
        print("dedupe-build-artifacts: no duplicate .ipynb content found")
        return

    rewritten = 0
    for path in glob.glob(os.path.join(docs_dir, "**", "*"), recursive=True):
        if not os.path.isfile(path):
            continue
        if os.path.splitext(path)[1].lower() not in TEXT_EXTENSIONS:
            continue
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        original = text
        for old_name, new_name in renames.items():
            if old_name in text:
                text = text.replace(old_name, new_name)
        if text != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            rewritten += 1

    print(f"dedupe-build-artifacts: removed {removed} duplicate .ipynb files "
          f"({len(renames)} distinct renames), rewrote references in {rewritten} files")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs")
