import os
import shutil
import subprocess
import sys
import webbrowser

from pathlib import Path


def open_url(url: str) -> bool:
    """Open a URL in the default browser."""
    return webbrowser.open(url)


def open_path(path: str | Path) -> None:
    """Open a file or directory using the system file manager."""
    target = Path(path).expanduser()

    if not target.exists():
        raise FileNotFoundError(f"Path does not exist: {target}")

    if sys.platform == "win32":
        os.startfile(str(target))

    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(target)])

    else:
        termux_open = shutil.which("termux-open")
        command = termux_open or shutil.which("xdg-open")

        if not command:
            raise RuntimeError("No system file opener found")

        subprocess.Popen([command, str(target)])
