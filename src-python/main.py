import argparse
import os
import sys

import webview

from api import Api


def get_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_entry_url(args: argparse.Namespace) -> str:
    if "__compiled__" in globals():
        # Running as Nuitka bundle — dist/ is next to the executable
        base = __nuitka_binary_dir  # type: ignore[name-defined]  # noqa: F821
        return os.path.join(base, "dist", "index.html")
    elif args.prod:
        return os.path.join(get_project_root(), "dist", "index.html")
    else:
        return args.dev_url


def main() -> None:
    parser = argparse.ArgumentParser(description="pywebview + React app")
    parser.add_argument(
        "--prod",
        action="store_true",
        help="Load from built dist/ instead of dev server",
    )
    parser.add_argument(
        "--dev-url",
        default="http://localhost:5173",
        help="Dev server URL (default: http://localhost:5173)",
    )
    args = parser.parse_args()

    entry = get_entry_url(args)
    is_dev = not args.prod and "__compiled__" not in globals()

    # For local file:// URLs, pywebview needs http_server=True to load ES modules
    http_server = not is_dev and not entry.startswith("http")

    api = Api()
    webview.create_window(
        "pywebview + React",
        url=entry,
        js_api=api,
        width=900,
        height=680,
    )
    webview.start(debug=is_dev, http_server=http_server)


if __name__ == "__main__":
    main()
