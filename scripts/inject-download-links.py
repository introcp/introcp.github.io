"""
Populate each notebook's `metadata.downloads` (MyST/Jupyter-Book-v2 frontmatter)
with links to its generated slides, PDF, raw notebook and Colab/JupyterLite
launchers, published at their well-known site-relative URLs.

Must run BEFORE `jupyter-book build`, so the theme picks it up as frontmatter.
Idempotent: safe to re-run, only rewrites the `downloads` key.
"""
import glob
import json
import os

SITE_ROOT = "https://introcp.github.io"
REPO = "introcp/introcp.github.io"
BRANCH = "2026"
JUPYTERLITE = "https://ercoppa.github.io/jupyterlite/lab/?fromURL="


def downloads_for(chapter, name):
    ipynb_url = f"{SITE_ROOT}/src/{chapter}/{name}.ipynb"
    return [
        {"url": f"{SITE_ROOT}/src/{chapter}/{name}.slides.html", "title": "Slides (HTML)"},
        {"url": f"{SITE_ROOT}/src/{chapter}/{name}.pdf", "title": "Slides (PDF)"},
        {"url": ipynb_url, "title": "Download notebook"},
        {"url": f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/src/{chapter}/{name}.ipynb",
         "title": "Open in Colab"},
        {"url": f"{JUPYTERLITE}{ipynb_url}", "title": "Open in JupyterLite"},
    ]


def main():
    for path in sorted(glob.glob("src/*/*.ipynb")):
        chapter = os.path.basename(os.path.dirname(path))
        name = os.path.splitext(os.path.basename(path))[0]

        with open(path) as f:
            nb = json.load(f)

        nb["metadata"]["downloads"] = downloads_for(chapter, name)

        with open(path, "w") as f:
            json.dump(nb, f, indent=1)
            f.write("\n")

        print("Updated downloads metadata:", path)


if __name__ == "__main__":
    main()
