import re
import subprocess


def get_php_version() -> str:
    """Return the installed PHP version."""
    try:
        result = subprocess.run(
            ["php", "-v"],
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
