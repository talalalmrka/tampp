import os

from dataclasses import dataclass, field
from pathlib import Path

from tampp.services.base import ServerService
from tampp.services.platform import find_php
from tampp.services.process import ProcessError, wait_for_port


@dataclass
class PhpServerConfig:
    document_root: Path
    host: str = "127.0.0.1"
    port: int = 8000
    executable: str | None = None
    router: Path | None = None
    ini_file: Path | None = None
    log_file: Path = Path("storage/logs/php.log")
    extra_args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.document_root = Path(self.document_root).expanduser()
        self.log_file = Path(self.log_file).expanduser()

        if self.router is not None:
            self.router = Path(self.router).expanduser()

        if self.ini_file is not None:
            self.ini_file = Path(self.ini_file).expanduser()

        if not 1 <= self.port <= 65535:
            raise ValueError("Invalid PHP server port.")


class PhpServer(ServerService):
    def __init__(self, config: PhpServerConfig):
        self.config = config
        super().__init__(config.log_file)

    def get_executable(self) -> str:
        executable = self.config.executable or find_php()

        if not executable:
            raise ProcessError(
                "PHP executable not found. Install PHP or configure its path."
            )

        return str(executable)

    def get_command(self) -> list[str]:
        config = self.config

        if not config.document_root.is_dir():
            raise FileNotFoundError(
                f"Document root does not exist: {config.document_root}"
            )

        command = [self.get_executable()]

        if config.ini_file is not None and config.ini_file.is_file():
            command.extend(["-c", str(config.ini_file.resolve())])

        command.extend(
            [
                "-S",
                f"{config.host}:{config.port}",
                "-t",
                str(config.document_root.resolve()),
            ]
        )

        if config.router is not None:
            if not config.router.is_file():
                raise FileNotFoundError(f"PHP router not found: {config.router}")

            command.append(str(config.router.resolve()))

        command.extend(config.extra_args)

        return command

    def start(self) -> None:
        if self.is_running():
            return

        env = os.environ.copy()
        env.update(self.config.env)

        self.process.start(
            self.get_command(),
            cwd=self.config.document_root,
            log_file=self.log_file,
            env=env,
        )

    def is_ready(self, timeout: float = 1) -> bool:
        if not self.is_running():
            return False

        return wait_for_port(
            self.config.host,
            self.config.port,
            timeout,
        )
