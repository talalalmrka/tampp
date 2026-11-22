import os

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlunsplit
from helpers import get_php_version


@dataclass
class PhpConfig:
    root: Path
    host: str = "0.0.0.0"
    port: int = 8000

    dashboard_path: Path | None = None
    php_info_path: Path | None = None
    ini_path: Path | None = None
    router_path: Path | None = None
    temp_path: Path | None = None

    executable: str | None = None
    php_version: str | None = None

    def __post_init__(self):
        self.root = Path(self.root).expanduser()

        self.dashboard_path = (
            Path(self.dashboard_path).expanduser()
            if self.dashboard_path
            else self.root / "dashboard"
        )

        self.php_info_path = (
            Path(self.php_info_path).expanduser()
            if self.php_info_path
            else self.dashboard_path / "phpinfo.php"
        )

        self.ini_path = (
            Path(self.ini_path).expanduser()
            if self.ini_path
            else self.dashboard_path / "php.ini"
        )

        self.router_path = (
            Path(self.router_path).expanduser()
            if self.router_path
            else self.dashboard_path / "router.php"
        )

        self.temp_path = (
            Path(self.temp_path).expanduser()
            if self.temp_path
            else self.dashboard_path / "tmp"
        )
        if self.php_version is None:
            self.php_version = get_php_version()

    @property
    def pid_file(self) -> Path:
        return self.temp_path / "php-server.pid"

    @property
    def log_file(self) -> Path:
        return self.temp_path / "php_errors.log"

    @property
    def url(self) -> str:
        return f"http://localhost:{self.port}"

    @property
    def dashboard_url(self) -> str:
        return f"{self.url}/dashboard"

    @property
    def php_info_url(self) -> str:
        return f"{self.dashboard_url}/phpinfo.php"

    @property
    def phpmyadmin_url(self) -> str:
        return f"{self.url}/dashboard/phpmyadmin"


@dataclass
class MariaDBConfig:
    executable: str | None = None
    command: str | None = None

    pid_file: Path | None = None
    log_file: Path | None = None

    def __post_init__(self):
        temp_path = PROJECTS_PATH / "dashboard" / "tmp"

        if self.pid_file is None:
            self.pid_file = temp_path / "mariadb.pid"

        if self.log_file is None:
            self.log_file = temp_path / "mariadb.log"

        self.pid_file = Path(self.pid_file).expanduser()
        self.log_file = Path(self.log_file).expanduser()


@dataclass
class AppConfig:
    php: PhpConfig
    mariadb: MariaDBConfig


PROJECTS_PATH = Path(
    os.environ.get(
        "PROJECTS_PATH",
        str(Path.home() / "Desktop" / "laravel-projects"),
    )
).expanduser()


APP_CONFIG = AppConfig(
    php=PhpConfig(
        root=PROJECTS_PATH,
        host="0.0.0.0",
        port=8000,
    ),
    mariadb=MariaDBConfig(),
)
