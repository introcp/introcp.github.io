"""
Patch each built page's `frontmatter.downloads` (MyST/Jupyter-Book-v2 site
data) with links to its generated slides, PDF, raw notebook and
Colab/JupyterLite launchers, published at their well-known site-relative
URLs.

This is a website-navigation concern, not lecture content, so it is patched
directly into mystmd's build output (docs/) rather than being written into
the notebooks under src/ (an earlier version of this script rewrote
src/*.ipynb before the build instead - that meant every build dirtied the
lecture source notebooks, which CI then committed back to git, and a
careless json.dump() in that rewrite is what caused the notebooks to fill
up with \\uXXXX escapes instead of literal unicode).

Must run AFTER `jupyter-book build --html`, once docs/ has been populated
from _build/html/ (see Makefile). mystmd emits each page's data twice: once
as docs/<slug>.json (fetched by the client-side router on navigation) and
once inlined verbatim inside docs/<slug>/index.html (the static,
pre-rendered snapshot used for the first paint / no-JS / search-engine
case). Both copies are patched in place, via targeted text surgery scoped to
the single `"frontmatter":{...}` object in each file, so nothing else in
either file is touched (no re-serialization, no reformatting, no risk of
mangling unicode elsewhere on the page).

Idempotent: safe to re-run, only rewrites the `downloads` array in place.
"""
import glob
import json
import os
import sys

SITE_ROOT = "https://introcp.github.io"
REPO = "introcp/introcp.github.io"
BRANCH = "2026"
JUPYTERLITE = "https://ercoppa.github.io/jupyterlite/lab/?fromURL="


def downloads_for(chapter, name):
    ipynb_url = f"{SITE_ROOT}/src/{chapter}/{name}.ipynb"
    # mystmd's book-theme only forces a blob download (onClick + fetch) for
    # downloads it recognizes as "local" exports; a plain user-supplied URL
    # like ipynb_url renders as a bare <a target="_blank"> link instead, so
    # the raw .ipynb JSON just opens as text in the browser. Route through
    # src/download.html, which fetches the file itself and forces the save
    # via a blob URL, regardless of how the theme renders the link.
    download_url = f"{SITE_ROOT}/src/download.html?file=src/{chapter}/{name}.ipynb"
    return [
        {"url": f"{SITE_ROOT}/src/{chapter}/{name}.slides.html", "title": "Slides (HTML)"},
        {"url": f"{SITE_ROOT}/src/{chapter}/{name}.pdf", "title": "Slides (PDF)"},
        {"url": download_url, "title": "Download notebook"},
        {"url": f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/src/{chapter}/{name}.ipynb",
         "title": "Open in Colab"},
        {"url": f"{JUPYTERLITE}{ipynb_url}", "title": "Open in JupyterLite"},
    ]


def find_pages_by_location(docs_dir):
    """Map a notebook's site-relative location (e.g. "/src/A00/A00-Introduction.ipynb")
    to its built docs/<slug>.json path and slug."""
    by_location = {}
    for path in glob.glob(os.path.join(docs_dir, "*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        location = data.get("location")
        if location:
            by_location[location] = (path, data.get("slug"))
    return by_location


def _bounded(text, start, open_ch, close_ch):
    depth = 0
    i = start
    while i < len(text):
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                return start, i
        i += 1
    raise ValueError(f"unbalanced {open_ch!r}/{close_ch!r} starting at {start}")


def patch_downloads(text, downloads):
    """Set frontmatter.downloads to `downloads` inside a mystmd page payload
    (a standalone docs/<slug>.json file, or the same payload inlined inside
    docs/<slug>/index.html). Confined to the single "frontmatter":{...}
    object in the text, so it can't collide with unrelated "downloads"-shaped
    text elsewhere on the page (e.g. inside a notebook's own displayed
    code/output)."""
    key = '"frontmatter":{'
    idx = text.find(key)
    if idx == -1:
        raise ValueError('no "frontmatter" object found')
    if text.find(key, idx + 1) != -1:
        raise ValueError('more than one "frontmatter" object found')

    obj_start = idx + len('"frontmatter":')
    start, end = _bounded(text, obj_start, "{", "}")
    body = text[start:end + 1]

    downloads_json = json.dumps(downloads, separators=(",", ":"))
    d_idx = body.find('"downloads":')
    if d_idx == -1:
        new_body = '{"downloads":' + downloads_json + ("," if len(body) > 2 else "") + body[1:]
    else:
        arr_start = body.find("[", d_idx)
        arr_start_i, arr_end_i = _bounded(body, arr_start, "[", "]")
        new_body = body[:arr_start_i] + downloads_json + body[arr_end_i + 1:]

    return text[:start] + new_body + text[end + 1:]


def patch_file(path, downloads):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = patch_downloads(text, downloads)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main(docs_dir="docs"):
    by_location = find_pages_by_location(docs_dir)

    for path in sorted(glob.glob("src/*/*.ipynb")):
        chapter = os.path.basename(os.path.dirname(path))
        name = os.path.splitext(os.path.basename(path))[0]
        location = f"/src/{chapter}/{name}.ipynb"

        match = by_location.get(location)
        if not match:
            print(f"Skipped (not a published page): {path}")
            continue
        json_path, slug = match

        downloads = downloads_for(chapter, name)
        patch_file(json_path, downloads)

        html_path = os.path.join(docs_dir, slug, "index.html")
        if os.path.exists(html_path):
            patch_file(html_path, downloads)
            print(f"Patched downloads: {json_path}, {html_path}")
        else:
            print(f"Patched downloads: {json_path} (no index.html for slug {slug!r})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs")
