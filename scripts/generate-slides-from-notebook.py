#!/usr/bin/env python3
"""
Generate and preview HTML/PDF slides for a single notebook, using Docker to
ensure a consistent environment (Linux, macOS, Windows).

Usage:

    python3 scripts/generate-slides-from-notebook.py <notebook>.ipynb

On Linux/macOS the script is also directly executable:

    ./scripts/generate-slides-from-notebook.py <notebook>.ipynb

Starts a watch process that regenerates the slides whenever the notebook is
saved. Press Ctrl+C to stop.
"""

import os
import subprocess
import sys
from pathlib import Path

IMAGE = "ercoppa/introcp"


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail(f"Usage: {sys.argv[0]} <notebook>.ipynb")

    notebook_arg = sys.argv[1]
    notebook_path = Path(notebook_arg)

    if notebook_path.suffix != ".ipynb":
        fail(f"File {notebook_arg} is not a .ipynb file")

    if not notebook_path.is_file():
        fail(f"File {notebook_arg} does not exist")

    repo_root = Path(__file__).resolve().parent.parent

    try:
        notebook_in_repo = notebook_path.resolve().relative_to(repo_root)
    except ValueError:
        fail(f"File {notebook_arg} must be inside the repository ({repo_root})")

    # Path as seen by the (always Linux) container, regardless of host OS.
    container_notebook_path = notebook_in_repo.as_posix()

    container_name = f"introcp-slide-{os.getpid()}"

    docker_cmd = ["docker", "run", "--rm", "-i"]

    # UID/GID mapping only makes sense on POSIX hosts (Linux/macOS); Docker
    # Desktop on Windows has no equivalent concept, so it's skipped there.
    if os.name == "posix":
        docker_cmd += ["-u", f"{os.getuid()}:{os.getgid()}"]

    docker_cmd += [
        "-v", f"{repo_root}:/home/user/introcp",
        "-w", "/home/user/introcp",
        "--ipc=host", "--cap-add=SYS_ADMIN", "--init",
        "--name", container_name,
        # Without a TTY (-t), Python's stdout is block-buffered by default, so
        # progress messages would only appear in bursts (or not until exit).
        # Force unbuffered output so hints show up immediately.
        "-e", "PYTHONUNBUFFERED=1",
        IMAGE,
        "scripts/convert-notebook-to-PDF-slides.py", "--watch", container_notebook_path,
    ]

    print("[INFO] Starting watch container. Press Ctrl+C to stop (press twice to force-kill).")
    # Use Popen (not subprocess.run) so that a KeyboardInterrupt here does not
    # SIGKILL the docker CLI immediately. On Ctrl+C, the terminal already sends
    # SIGINT to the whole foreground process group (including the docker CLI),
    # which forwards it into the container. The in-container script then needs
    # time to finish any in-progress conversion (headless-browser PDF rendering
    # can take well over a minute) and run its own cleanup logic (removing temp
    # files like *.slide.pdf.html and *_slides.pdf) before exiting. So we wait
    # indefinitely for a graceful exit, and only force-stop if the user presses
    # Ctrl+C a second time.
    proc = subprocess.Popen(docker_cmd)
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Waiting for the container to finish and stop gracefully... "
              "(press Ctrl+C again to force-kill; this may leave temp files behind)")
        try:
            proc.wait()
        except KeyboardInterrupt:
            print("\n[INFO] Forcing container to stop...")
    finally:
        # Best-effort cleanup: harmless if the container already stopped/removed itself (--rm).
        subprocess.run(
            ["docker", "stop", container_name],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )


if __name__ == "__main__":
    main()
