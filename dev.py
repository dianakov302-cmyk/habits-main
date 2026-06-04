from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_APP = "backend.main:app"
FRONTEND_DIR = PROJECT_ROOT / "frontend" / "site"


def ensure_img_link() -> None:
    """Ensure frontend/site/img/ exists pointing to frontend/img/.

    Uses a directory junction on Windows (no admin rights required) and a
    symlink on macOS/Linux.  Safe to call repeatedly — exits early when the
    link/directory already exists.
    """
    img_src = str(PROJECT_ROOT / "frontend" / "img")
    img_dst = str(PROJECT_ROOT / "frontend" / "site" / "img")

    if os.path.exists(img_dst):
        return  # already set up

    if not os.path.isdir(img_src):
        return  # no img dir to link — skip silently

    if sys.platform == "win32":
        # mklink /J creates a directory junction; no elevation needed
        subprocess.run(["mklink", "/J", img_dst, img_src], shell=True, check=True)
    else:
        os.symlink(img_src, img_dst)

    print(f"  Linked frontend/site/img -> frontend/img")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the backend API and the static frontend together.",
    )
    parser.add_argument(
        "--backend-port",
        type=int,
        default=8080,
        help="Port for the FastAPI backend (default: 8080).",
    )
    parser.add_argument(
        "--frontend-port",
        type=int,
        default=3000,
        help="Port for the frontend static server (default: 3000).",
    )
    return parser.parse_args()


def start_processes(backend_port: int, frontend_port: int) -> list[subprocess.Popen[str]]:
    backend_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        BACKEND_APP,
        "--reload",
        "--host",
        "127.0.0.1",
        "--port",
        str(backend_port),
    ]
    frontend_cmd = [
        sys.executable,
        "-m",
        "http.server",
        str(frontend_port),
        "--bind",
        "127.0.0.1",
        "--directory",
        str(FRONTEND_DIR),
    ]

    backend = subprocess.Popen(backend_cmd, cwd=PROJECT_ROOT)
    frontend = subprocess.Popen(frontend_cmd, cwd=PROJECT_ROOT)
    return [backend, frontend]


def stop_processes(processes: list[subprocess.Popen[str]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()

    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> int:
    ensure_img_link()
    args = parse_args()
    processes = start_processes(args.backend_port, args.frontend_port)

    print(f"Backend:  http://127.0.0.1:{args.backend_port}")
    print(f"Frontend: http://127.0.0.1:{args.frontend_port}")
    print("Press Ctrl+C to stop both processes.")

    def handle_signal(_signum: int, _frame) -> None:
        stop_processes(processes)
        raise SystemExit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while True:
            backend_exit = processes[0].poll()
            frontend_exit = processes[1].poll()
            if backend_exit is not None or frontend_exit is not None:
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_processes(processes)

    backend_exit = processes[0].returncode
    frontend_exit = processes[1].returncode

    if backend_exit not in (0, None):
        return backend_exit
    if frontend_exit not in (0, None):
        return frontend_exit
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
