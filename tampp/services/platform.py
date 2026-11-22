import platform as system_platform
import shutil
from pathlib import Path


def get_os() -> str:
    system = system_platform.system().lower()

    if system == "darwin":
        return "macos"

    if system == "windows":
        return "windows"

    if system == "linux":
        return "linux"

    return "unknown"


def get_architecture() -> str:
    return system_platform.machine().lower()


def find_executable(*names: str) -> str | None:
    for name in names:
        executable = shutil.which(name)

        if executable:
            return executable

    return None


def find_php() -> str | None:
    return find_executable("php", "php.exe")


def find_mariadb() -> str | None:
    executable = find_executable(
        "mariadbd",
        "mariadbd.exe",
        "mysqld",
        "mysqld.exe",
    )

    if executable:
        return executable

    return None


def find_mariadb_installer() -> str | None:
    return find_executable(
        "mariadb-install-db",
        "mariadb-install-db.exe",
        "mysql_install_db",
        "mysql_install_db.exe",
    )


def get_default_data_dir() -> Path | None:
    os_name = get_os()

    if os_name == "macos":
        candidates = [
            Path("/opt/homebrew/var/mysql"),
            Path("/usr/local/var/mysql"),
        ]

    elif os_name == "linux":
        candidates = [
            Path("/var/lib/mysql"),
            Path("/var/lib/mariadb"),
        ]

    elif os_name == "windows":
        candidates = [
            Path("C:/Program Files/MariaDB/data"),
        ]

    else:
        candidates = []

    for path in candidates:
        if path.is_dir():
            return path

    return None
