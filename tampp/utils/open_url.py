from __future__ import annotations

import os
import platform
import shutil
import subprocess
import webbrowser
from urllib.parse import urlparse


def open_url(url: str) -> bool:
    """Open a URL in the system's external browser."""

    url = url.strip()

    if not url:
        return False

    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    # Termux
    if os.environ.get("TERMUX_VERSION") or (
        "com.termux" in os.environ.get("PREFIX", "")
    ):
        opener = shutil.which("termux-open-url")

        if opener:
            try:
                subprocess.Popen([opener, url])
                return True
            except OSError:
                pass

    # Standard browser handler
    try:
        if webbrowser.open(url, new=2):
            return True
    except webbrowser.Error:
        pass

    # Native fallback
    system = platform.system()

    commands = {
        "Darwin": ["open", url],
        "Windows": ["cmd", "/c", "start", "", url],
        "Linux": ["xdg-open", url],
    }

    command = commands.get(system)

    if command and shutil.which(command[0]):
        try:
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except OSError:
            pass

    # Linux fallback
    if system == "Linux":
        gio = shutil.which("gio")

        if gio:
            try:
                subprocess.Popen(
                    [gio, "open", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return True
            except OSError:
                pass

    return False
