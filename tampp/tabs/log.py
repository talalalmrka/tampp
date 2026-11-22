from datetime import datetime
from pathlib import Path

from textual.widgets import RichLog, TabPane


class LogTab(TabPane):
    def __init__(
        self,
        log_files: dict[str, Path],
        **kwargs,
    ):
        super().__init__("Log", **kwargs)

        self.log_files = {
            name: Path(path).expanduser() for name, path in log_files.items()
        }

        self.offsets: dict[str, int] = {}
        self.buffers: dict[str, str] = {}

    def compose(self):
        yield RichLog(
            id="server-log",
            wrap=True,
            highlight=False,
            markup=False,
            max_lines=2000,
        )

    def on_mount(self) -> None:
        self.write_event("SYSTEM", "Log viewer started")
        self.set_interval(0.5, self.read_logs)

    def write_event(
        self,
        service: str,
        message: str,
        level: str = "INFO",
    ) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.query_one(RichLog).write(
            f"[{timestamp}] [{level}] [{service.upper()}] {message}"
        )

    def read_logs(self) -> None:
        for service, path in self.log_files.items():
            if not path.is_file():
                continue

            try:
                size = path.stat().st_size
                offset = self.offsets.get(service, 0)

                if size < offset:
                    offset = 0
                    self.buffers[service] = ""

                if size == offset:
                    continue

                with path.open("rb") as file:
                    file.seek(offset)
                    content = file.read()
                    self.offsets[service] = file.tell()

                text = self.buffers.get(service, "")
                text += content.decode("utf-8", errors="replace")

                lines = text.split("\n")
                self.buffers[service] = lines.pop()

                for line in lines:
                    line = line.rstrip("\r")

                    if line:
                        self.write_event(service, line, "SERVER")

            except OSError as error:
                self.write_event(
                    service,
                    str(error),
                    "ERROR",
                )
