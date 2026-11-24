from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from tampp.core import Collection


def php_version(php: str = "php") -> str:
    """Return the installed PHP version."""
    try:
        result = subprocess.run(
            [php, "-v"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )

        match = re.search(r"PHP\s+([\d.]+)", result.stdout)
        return match.group(1) if match else "Unknown"

    except FileNotFoundError:
        return "Not installed"
    except subprocess.TimeoutExpired:
        return "Timeout"
    except subprocess.CalledProcessError:
        return "Error"


def php_ini_path(php: str = "php") -> Path | None:
    try:
        result = subprocess.run(
            [php, "--ini"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )

        match = re.search(
            r"Loaded Configuration File:\s*(.+)",
            result.stdout,
        )

        if not match:
            return None

        path = match.group(1).strip()

        return None if path == "(none)" else Path(path)

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
    ):
        return None


def php_configs(php: str = "php") -> str:
    """Return PHP configuration file information."""
    try:
        result = subprocess.run(
            [php, "--ini"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )

        return result.stdout

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
    ):
        return ""


def php_ini_all(php: str = "php") -> Collection:
    """Return all loaded PHP INI directives."""
    script = "echo json_encode(ini_get_all(null, false));"

    try:
        result = subprocess.run(
            [php, "-r", script],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )

        return Collection(json.loads(result.stdout))

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
        json.JSONDecodeError,
    ):
        return Collection()


def php_ini_get(key: str, default=None, php: str = "php"):
    """Return a PHP INI directive value."""
    return php_ini_all(php).get(key, default)
