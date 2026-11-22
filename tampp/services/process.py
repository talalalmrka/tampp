import os
import signal
import subprocess
import time

from pathlib import Path
from typing import Sequence


class ProcessError(RuntimeError):
    pass


class ManagedProcess:
    def __init__(self):
        self.process: subprocess.Popen | None = None

    @property
    def pid(self) -> int | None:
        if self.process is None:
            return None

        return self.process.pid

    def is_running(self) -> bool:
        if self.process is None:
            return False

        return self.process.poll() is None

    def start(
        self,
        command: Sequence[str],
        *,
        cwd: Path | None = None,
        log_file: Path | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.Popen:
        if self.is_running():
            raise ProcessError("Process is already running.")

        if log_file:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            output = log_file.open("ab")
        else:
            output = subprocess.DEVNULL

        try:
            creation_flags = 0

            if os.name == "nt":
                creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP

            self.process = subprocess.Popen(
                list(command),
                cwd=str(cwd) if cwd else None,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=output,
                stderr=subprocess.STDOUT,
                shell=False,
                creationflags=creation_flags,
            )

        except OSError as error:
            raise ProcessError(f"Unable to start process: {error}") from error

        finally:
            if log_file:
                output.close()

        return self.process

    def stop(self, timeout: float = 10) -> None:
        if not self.is_running():
            self.process = None
            return

        process = self.process

        if process is None:
            return

        self._request_stop(process)

        try:
            process.wait(timeout=timeout)

        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        finally:
            self.process = None

    @staticmethod
    def _request_stop(process: subprocess.Popen) -> None:
        process.terminate()

    def wait(self, timeout: float | None = None) -> int | None:
        if self.process is None:
            return None

        return self.process.wait(timeout=timeout)


def wait_for_port(
    host: str,
    port: int,
    timeout: float = 30,
) -> bool:
    import socket

    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        try:
            with socket.create_connection(
                (host, port),
                timeout=1,
            ):
                return True

        except OSError:
            time.sleep(0.25)

    return False
