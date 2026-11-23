import shutil

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import TabPane

from tampp.config import APP_CONFIG
from tampp.screens import CodeEditorScreen
from tampp.widgets import ListGroup, ListGroupItem


class MariaDBConfigItem(ListGroupItem):
    """A list item that opens the shared code editor."""

    def _open_file(self) -> None:
        if not self.path:
            return

        self.app.push_screen(
            CodeEditorScreen(self.path),
            callback=self.on_editor_closed,
        )

    def on_editor_closed(self, saved: bool | None) -> None:
        if not saved:
            return

        self.notify(
            "MariaDB configuration saved. Restart MariaDB to apply changes.",
            title="Configuration saved",
            severity="information",
        )

        log_event = getattr(self.app, "log_event", None)

        if callable(log_event):
            log_event("mariadb", "MariaDB configuration updated")


class MariadbTab(TabPane):
    """MariaDB server information and configuration."""

    def __init__(self, **kwargs):
        super().__init__("MariaDB", **kwargs)

        self.config = APP_CONFIG.mariadb

        self.executable = (
            getattr(self.config, "executable", None) or self.find_server_executable()
        )

        self.client_executable = shutil.which("mariadb") or shutil.which("mysql")

        self.command = getattr(self.config, "command", None)

        self.host = getattr(self.config, "host", None)
        self.port = getattr(self.config, "port", None)

        self.pid_path = self.get_optional_path("pid_file")
        self.log_path = self.get_optional_path("log_file")
        self.config_path = self.get_optional_path("config_file")
        self.data_path = self.get_optional_path("data_dir")

    @staticmethod
    def find_server_executable() -> str | None:
        """Find the MariaDB server executable."""

        for name in (
            "mariadbd-safe",
            "mysqld_safe",
            "mariadbd",
            "mysqld",
        ):
            executable = shutil.which(name)

            if executable:
                return executable

        return None

    def get_optional_path(self, name: str) -> Path | None:
        """Get an optional filesystem path from configuration."""

        value = getattr(self.config, name, None)

        if not value:
            return None

        return Path(value).expanduser()

    def get_groups(self) -> list[ListGroup]:
        return [
            ListGroup(
                title="Info",
                items=[
                    ListGroupItem(
                        title="Server Executable",
                        subtitle=self.executable or "Not found",
                    ),
                    ListGroupItem(
                        title="Client Executable",
                        subtitle=self.client_executable or "Not found",
                    ),
                    ListGroupItem(
                        title="Startup Command",
                        subtitle=self.command or "Automatic detection",
                    ),
                ],
            ),
            ListGroup(
                title="Connection",
                items=[
                    ListGroupItem(
                        title="Host",
                        subtitle=self.host or "Managed by MariaDB configuration",
                    ),
                    ListGroupItem(
                        title="Port",
                        subtitle=(
                            str(self.port)
                            if self.port
                            else "Managed by MariaDB configuration"
                        ),
                    ),
                ],
            ),
            ListGroup(
                title="Paths",
                items=[
                    ListGroupItem(
                        title="Data Directory",
                        path=self.data_path,
                    )
                    if self.data_path
                    else ListGroupItem(
                        title="Data Directory",
                        subtitle="Managed by my.cnf",
                    ),
                ],
            ),
            ListGroup(
                title="Files",
                items=[
                    MariaDBConfigItem(
                        title="Configuration",
                        subtitle=str(self.config_path),
                        path=self.config_path,
                    )
                    if self.config_path
                    else ListGroupItem(
                        title="Configuration",
                        subtitle="Using MariaDB defaults",
                    ),
                    ListGroupItem(
                        title="PID File",
                        path=self.pid_path,
                    )
                    if self.pid_path
                    else ListGroupItem(
                        title="PID File",
                        subtitle="Not configured",
                    ),
                    ListGroupItem(
                        title="Log File",
                        path=self.log_path,
                    )
                    if self.log_path
                    else ListGroupItem(
                        title="Log File",
                        subtitle="Not configured",
                    ),
                ],
            ),
        ]

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="mariadb-settings"):
            yield from self.get_groups()
