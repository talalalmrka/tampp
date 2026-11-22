from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


def open_dir(path: str | Path) -> bool:
    """Open a directory in the system's default file manager."""

    directory = Path(path).expanduser().resolve()

    if not directory.exists() or not directory.is_dir():
        return False

    system = platform.system()

    # Windows
    if system == "Windows":
        try:
            os.startfile(directory)
            return True
        except OSError:
            return False

    # macOS
    if system == "Darwin":
        opener = shutil.which("open")

        if opener:
            try:
                subprocess.Popen([opener, str(directory)])
                return True
            except OSError:
                pass

        return False

    # Termux / Android
    termux_opener = shutil.which("termux-open")

    if termux_opener:
        try:
            subprocess.Popen([termux_opener, str(directory)])
            return True
        except OSError:
            pass

    # Linux / Debian / proot
    for command in ("xdg-open", "gio"):
        opener = shutil.which(command)

        if not opener:
            continue

        args = (
            [opener, str(directory)]
            if command == "xdg-open"
            else [opener, "open", str(directory)]
        )

        try:
            subprocess.Popen(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except OSError:
            continue

    return False
