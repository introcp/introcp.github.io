all:
	@echo "Available targets: docker-build, docker-push, docker-run, docker-build-book, build-book, publish, clean-book"

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

build-book:
	# rm -rf _build/html || echo "nothing to clean"
	# embed slides/PDF/Colab/JupyterLite links into each notebook's frontmatter
	# (must run BEFORE slide generation: it rewrites notebook bytes, which
	# would otherwise invalidate the slide-generation hash cache every run)
	. ~/.venv/bin/activate; python3 scripts/inject-download-links.py
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