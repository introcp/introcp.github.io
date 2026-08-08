"""
One-time content migration: replace the absolute
`https://introcp.github.io/dist/img/logo2.png` reference (used at the top of
every notebook's title cell) with a relative path to the copy already vendored
at src/dist/img/logo2.png.

Under Jupyter Book v1 (Sphinx), this string was never touched. Under v2
(mystmd), any absolute image URL is fetched over the network at build time to
be locally hashed/optimized - and ~80 near-simultaneous requests for the exact
same URL reliably trip failures (site rate limiting / connection exhaustion),
leaving a broken `src="/build/undefined"` image. Pointing at the local file
removes the network round-trip entirely.

Safe to run once; re-running is a no-op.
"""
import glob
import json

REMOTE_URL = "https://introcp.github.io/dist/img/logo2.png"


def main():
    changed = 0

    for path in sorted(glob.glob("src/*/*.ipynb")):
        with open(path) as f:
            text = f.read()
        new_text = text.replace(REMOTE_URL, "../dist/img/logo2.png")
        if new_text != text:
            with open(path, "w") as f:
                f.write(new_text)
            print("Localized:", path)
            changed += 1

    for path in ["src/index.md"]:
        with open(path) as f:
            text = f.read()
        new_text = text.replace(REMOTE_URL, "dist/img/logo2.png")
        if new_text != text:
            with open(path, "w") as f:
                f.write(new_text)
            print("Localized:", path)
            changed += 1

    print(f"\n{changed} file(s) migrated.")


if __name__ == "__main__":
    main()
