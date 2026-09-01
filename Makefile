all:
	@echo "Available targets: docker-build, docker-push, docker-run, docker-build-book, docker-serve, build-book, serve, publish, clean-book"

docker-build:
	docker build -t ercoppa/introcp:v2 -t ercoppa/introcp:latest .

docker-push:
	docker push ercoppa/introcp:v2
	docker push ercoppa/introcp:latest

docker-run:
	docker run --rm -ti --pull always \
			-u `id -u`:`id -g` \
			-v $(PWD):/home/user/introcp \
			-w /home/user/introcp \
			--ipc=host --cap-add=SYS_ADMIN --init \
			--name introcp \
			ercoppa/introcp:v2 \
			bash

docker-build-book:
	docker run --rm -ti --pull always \
			-u `id -u`:`id -g` \
			-v $(PWD):/home/user/introcp \
			-w /home/user/introcp \
			--ipc=host --cap-add=SYS_ADMIN --init \
			--name introcp \
			ercoppa/introcp:v2 \
			bash -c "make build-book"

# live dev preview of src/ + myst.yml on http://localhost:3500, with
# file-watching and auto-rebuild/live-reload on every change (mystmd's own
# dev server, not the finalized docs/ output - no slides/PDF/download-link
# post-processing, see build-book).
docker-serve:
	docker run --rm -ti --pull always \
			-u `id -u`:`id -g` \
			-v $(PWD):/home/user/introcp \
			-w /home/user/introcp \
			--ipc=host --cap-add=SYS_ADMIN --init \
			-p 3500:3500 -p 3600:3600 \
			--name introcp \
			ercoppa/introcp:v2 \
			bash -c "make serve"

# --keep-host is required: mystmd's `start` otherwise forces HOST=localhost
# internally, which binds only inside the container's network namespace and
# is unreachable through Docker's -p port mapping from the host.
serve:
	. ~/.venv/bin/activate; HOST=0.0.0.0 PORT=3500 SERVER_PORT=3600 jupyter-book start --keep-host

build-book:
	# mystmd's content-hash cache in _build/html/build/ only ever adds new
	# hashed copies when a file's content changes - it never removes stale
	# ones. Since docs/ below is a wholesale copy of _build/html/, skipping
	# this clean means every past build's orphaned hash-named files ride
	# along into docs/ (and git) forever.
	rm -rf _build/html || echo "nothing to clean"
	# generate slides in HTML and PDF
	. ~/.venv/bin/activate; python3 scripts/convert-notebook-to-PDF-slides.py
	# generate website with jupyter-book (v2, myst.yml)
	# HOST=127.0.0.1 works around mystmd's static-export pre-render step
	# (it spins up a local server and self-crawls it to snapshot every page)
	# failing to bind when Node resolves the "localhost" hostname, seen
	# specifically when running inside the introcp container.
	. ~/.venv/bin/activate; HOST=127.0.0.1 jupyter-book build --html
	cp -r docs/.hashes . || true
	rm -rf docs ; mkdir docs && cp -r _build/html/* docs && mv .hashes docs || true
	. ~/.venv/bin/activate; python3 scripts/finalize-website.py docs
	# patch in slides/PDF/Colab/JupyterLite links: a website-navigation
	# concern, so it patches the built docs/ pages directly rather than
	# writing into src/*.ipynb (which CI would otherwise commit back to git
	# as a build byproduct on every run)
	. ~/.venv/bin/activate; python3 scripts/inject-download-links.py docs
	# mystmd emits a separate content-hashed copy of a notebook for every
	# path it discovers it through, even when nothing differs between them
	# (confirmed even on a from-scratch build) - collapse the duplicates.
	. ~/.venv/bin/activate; python3 scripts/dedupe-build-artifacts.py docs
	rm -rf docs/src/dist; cp -a src/dist docs/src/
	rm -rf docs/dist; cp -a src/dist docs/
	cp -a src/dist/plugin docs/src/
	cp _static/robots.txt docs/
	cp src/download.html docs/src/
	rm -rf docs/docs

publish:
	git add docs

clean-book:
	rm -rf _build || echo "nothing to clean"