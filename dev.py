"""Dev runner: starts Vite + pywebview in one command, like `tauri dev`."""

import subprocess
import sys
import time
import urllib.request


def wait_for_vite(url: str, timeout: int = 30) -> bool:
    """Poll until Vite dev server is responding."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def main() -> None:
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pm",
        default=os.environ.get("npm_execpath", "npm").split("\\")[-1].split("/")[-1].replace(".js", "").replace(".cmd", "") or "npm",
        help="Package manager to use: npm, bun, yarn, pnpm (default: npm)",
    )
    parser.add_argument("--dev-url", default="http://localhost:5173")
    args = parser.parse_args()

    dev_url = args.dev_url
    pm = args.pm

    # 1. Start Vite in the background
    vite = subprocess.Popen(
        [pm, "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=(sys.platform == "win32"),
    )

    try:
        # 2. Wait for Vite to be ready
        print(f"Waiting for Vite on {dev_url}...")
        if not wait_for_vite(dev_url):
            print("Vite failed to start.", file=sys.stderr)
            vite.terminate()
            sys.exit(1)
        print("Vite is ready.")

        # 3. Launch pywebview (blocks until window is closed)
        result = subprocess.run(
            [sys.executable, "src-python/main.py", "--dev-url", dev_url],
        )
        sys.exit(result.returncode)
    finally:
        # 4. Kill Vite when pywebview exits
        vite.terminate()
        vite.wait()


if __name__ == "__main__":
    main()
