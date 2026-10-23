"""
launch.py -- starts the Digital Twin backend AND serves its frontend, in
one command. Two separate concerns this solves at once:

1. api.py's internal path routing (`project_root = current_dir.parent.parent`)
   assumes a specific nested folder layout to find the `modules/` package.
   This launcher is self-locating instead of assuming: it searches for
   api.py near itself, adds whatever paths it actually needs, and only
   then imports it -- works whether your layout is flat or nested.

2. Opening the frontend HTML files directly (file://...) breaks icon
   loading and any fetch() call under Chrome's CORS rules for local files
   (confirmed earlier -- every icon request came back net::ERR_FAILED).
   This starts a plain static file server for the frontend folder so it's
   served over http://, which fixes that outright.

Usage:
    python launch.py
    python launch.py --api-port 8001 --frontend-port 5500
    python launch.py --backend-dir path/to/digital_twin --frontend-dir path/to/ui

Ctrl+C stops both.
"""

import argparse
import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path


def find_file(start_dir: Path, filename: str, max_depth: int = 3) -> Path | None:
    """Searches start_dir and its subdirectories (up to max_depth) for a
    file. Used to locate api.py / a frontend HTML file without assuming a
    fixed folder layout."""
    if (start_dir / filename).exists():
        return start_dir / filename

    if max_depth <= 0:
        return None

    for child in start_dir.iterdir():
        if child.is_dir() and not child.name.startswith((".", "__")):
            found = find_file(child, filename, max_depth - 1)
            if found:
                return found
    return None


def resolve_backend_dir(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).resolve()
        if not (path / "api.py").exists():
            print(f"[launch.py] ERROR: no api.py found in {path}")
            sys.exit(1)
        return path

    here = Path(__file__).resolve().parent
    api_path = find_file(here, "api.py")
    if api_path is None:
        print("[launch.py] ERROR: could not find api.py anywhere under this script's "
              "directory. Pass --backend-dir explicitly.")
        sys.exit(1)
    return api_path.parent


def resolve_frontend_dir(explicit: str | None, backend_dir: Path) -> Path | None:
    if explicit:
        path = Path(explicit).resolve()
        if not (path / "home.html").exists():
            print(f"[launch.py] WARNING: no home.html found in {path} -- frontend server "
                  f"will still start, but may serve the wrong folder.")
        return path

    here = Path(__file__).resolve().parent
    html_path = find_file(here, "home.html") or find_file(backend_dir, "home.html")
    return html_path.parent if html_path else None


def start_backend(backend_dir: Path, port: int):
    """Imports and runs api.py's FastAPI app with uvicorn, from wherever it
    actually lives -- mirrors exactly what `python api.py` does, just
    without requiring you to `cd` there first."""
    sys.path.insert(0, str(backend_dir))
    # api.py's own path routing (project_root = parent.parent of its own
    # location) still runs when it's imported -- this just makes sure
    # backend_dir itself is importable regardless of where launch.py sits.

    import uvicorn
    import api  

    print(f"[launch.py] Digital Twin API starting on http://127.0.0.1:{port}")
    uvicorn.run(api.app, host="127.0.0.1", port=port, log_level="info")


def start_frontend(frontend_dir: Path, port: int):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(frontend_dir))
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"[launch.py] Frontend serving http://127.0.0.1:{port}/home.html")
        httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Launch the Digital Twin API + its frontend together.")
    parser.add_argument("--backend-dir", default=None, help="Folder containing api.py (auto-detected if omitted)")
    parser.add_argument("--frontend-dir", default=None, help="Folder containing home.html (auto-detected if omitted)")
    parser.add_argument("--api-port", type=int, default=8001)
    parser.add_argument("--frontend-port", type=int, default=5500)
    parser.add_argument("--no-frontend", action="store_true", help="Only start the API, skip the static file server")
    args = parser.parse_args()

    backend_dir = resolve_backend_dir(args.backend_dir)
    print(f"[launch.py] Digital Twin backend found at: {backend_dir}")

    frontend_dir = None
    if not args.no_frontend:
        frontend_dir = resolve_frontend_dir(args.frontend_dir, backend_dir)
        if frontend_dir is None:
            print("[launch.py] No frontend (home.html) found -- starting API only. "
                  "Pass --frontend-dir if it's somewhere this couldn't find.")

    if frontend_dir:
        frontend_thread = threading.Thread(
            target=start_frontend, args=(frontend_dir, args.frontend_port), daemon=True
        )
        frontend_thread.start()

    try:
        # Backend runs on the main thread -- uvicorn.run() blocks, and its
        # own Ctrl+C handling is what should own the process's lifetime.
        start_backend(backend_dir, args.api_port)
    except KeyboardInterrupt:
        print("\n[launch.py] Shutting down.")


if __name__ == "__main__":
    main()

    # To Open the Digital Twin Dashboard, use http://localhost:5500/home.html
