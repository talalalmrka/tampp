import os
import signal

from dataclasses import dataclass, field
from pathlib import Path

from tampp.services.base import ServerService
from tampp.services.platform import (
    find_mariadb,
    find_mariadb_installer,
    get_default_data_dir,
)
from tampp.services.process import (
    ManagedProcess,
    ProcessError,
    wait_for_port,
)


@dataclass
class MariaDBConfig:
    data_dir: Path | None = None

    host: str = "127.0.0.1"
    port: int = 3306

    executable: str | None = None
    installer: str | None = None

    socket: Path | None = None
    pid_file: Path | None = None
    log_file: Path = Path("storage/logs/mariadb.log")

    extra_args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)

    startup_timeout: float = 30

    def __post_init__(self):
        if self.data_dir is None:
            self.data_dir = get_default_data_dir()

        if self.data_dir is not None:
            self.data_dir = Path(self.data_dir).expanduser()

        if self.socket is not None:
            self.socket = Path(self.socket).expanduser()

        if self.pid_file is not None:
            self.pid_file = Path(self.pid_file).expanduser()

        self.log_file = Path(self.log_file).expanduser()

        if not 1 <= self.port <= 65535:
            raise ValueError("Invalid MariaDB port.")


class MariaDBServer(ServerService):
    def __init__(self, config: MariaDBConfig):
        self.config = config

        super().__init__(config.log_file)

    def get_executable(self) -> str:
        executable = self.config.executable or find_mariadb()

        if not executable:
            raise ProcessError(
                "MariaDB executable not found. Install MariaDB or configure its path."
            )

        return executable

    def get_installer(self) -> str:
        installer = self.config.installer or find_mariadb_installer()

        if not installer:
            raise ProcessError(
                "MariaDB installer not found. Configure mariadb-install-db manually."
            )

        return installer

    def get_command(self) -> list[str]:
        config = self.config

        if config.data_dir is None:
            raise ValueError("MariaDB data directory is not configured.")

        if not config.data_dir.is_dir():
            raise FileNotFoundError(
                f"MariaDB data directory does not exist: {config.data_dir}"
            )

        command = [
            self.get_executable(),
            f"--datadir={config.data_dir.resolve()}",
            f"--bind-address={config.host}",
            f"--port={config.port}",
        ]

        if config.socket:
            command.append(f"--socket={config.socket.expanduser()}")

        if config.pid_file:
            command.append(f"--pid-file={config.pid_file.expanduser()}")

        if os.name == "nt":
            command.append("--console")

        command.extend(config.extra_args)

        return command

    def start(self) -> None:
        if self.is_running():
            return

        if self.config.data_dir is None:
            raise ValueError("Configure the MariaDB data directory first.")

        env = os.environ.copy()
        env.update(self.config.env)

        self.process.start(
            self.get_command(),
            cwd=self.config.data_dir,
            log_file=self.log_file,
            env=env,
        )

    def stop(self) -> None:
        self.process.stop()

    def initialize(self) -> None:
        config = self.config

        if config.data_dir is None:
            raise ValueError("Configure the MariaDB data directory first.")

        if self.is_running():
            raise ProcessError("Cannot initialize while MariaDB is running.")

        if (config.data_dir / "mysql").is_dir():
            raise ProcessError("MariaDB data directory is already initialized.")

        config.data_dir.mkdir(parents=True, exist_ok=True)

        command = [
            self.get_installer(),
            f"--datadir={config.data_dir.resolve()}",
        ]

        import subprocess

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env={**os.environ, **config.env},
            check=False,
        )

        if result.returncode != 0:
            raise ProcessError(
                f"MariaDB initialization failed:\n{result.stderr or result.stdout}"
            )

    def is_ready(self, timeout: float = 1) -> bool:
        if not self.is_running():
            return False

        return wait_for_port(
            self.config.host,
            self.config.port,
            timeout,
        )
