from abc import ABC, abstractmethod
from pathlib import Path

from tampp.models.server_status import ServerStatus
from tampp.services.process import ManagedProcess


class ServerService(ABC):
    def __init__(self, log_file: Path | None = None):
        self.process = ManagedProcess()
        self.log_file = Path(log_file) if log_file else None

    @abstractmethod
    def start(self) -> None: ...

    def stop(self) -> None:
        self.process.stop()

    def restart(self) -> None:
        self.stop()
        self.start()

    def is_running(self) -> bool:
        return self.process.is_running()

    def get_status(self) -> ServerStatus:
        if self.is_running():
            return ServerStatus.ON

        return ServerStatus.OFF

    @property
    def pid(self) -> int | None:
        return self.process.pid

    def get_log_file(self) -> Path | None:
        return self.log_file
