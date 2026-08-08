import sys
import glob
import os
import shutil

# Publish each chapter dir (notebook, img/, slides.html, pdf) verbatim under
# docs/, so slides/PDF/notebook all live at stable, predictable URLs that
# scripts/inject-download-links.py points the "downloads" button at. This
# also preserves the slide deck's own relative asset links (../dist/..., img/...).
for filename in glob.glob('src/*/*slides.html'):
    print("Processing", filename)
    d = os.path.dirname(filename)
    dest = os.path.join(sys.argv[1], d)
    print("Copying", d, "->", dest)
    shutil.copytree(d, dest, dirs_exist_ok=True)

# Rewrite relative img/ and ../dist/ references to absolute URLs in the
# published notebook copy, since Colab/JupyterLite/a plain local download
# fetch just the single .ipynb file (no sibling img/ or dist/ folder) when
# opened via a raw URL.
for filename in glob.glob('docs/src/*/*.ipynb'):
    print("Processing", filename)
    data = open(filename).read()
    d = os.path.basename(os.path.dirname(filename))
    data = data.replace('(img/', '(https://introcp.github.io/src/' + d + '/img/')
    data = data.replace('"img/', '"https://introcp.github.io/src/' + d + '/img/')
    data = data.replace('(../dist/', '(https://introcp.github.io/dist/')
    data = data.replace('"../dist/', '"https://introcp.github.io/dist/')
    open(filename, 'w').write(data)
