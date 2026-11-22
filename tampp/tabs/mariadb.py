import shutil
import webbrowser

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static, TabPane, TextArea

from tampp.config import APP_CONFIG


class MariaDBConfigEditor(ModalScreen):
    def __init__(self, config_path: Path):
        super().__init__()

        self.config_path = Path(config_path).expanduser()

        try:
            self.initial_content = (
                self.config_path.read_text(encoding="utf-8")
                if self.config_path.is_file()
                else ""
            )
        except OSError:
            self.initial_content = ""

    def compose(self) -> ComposeResult:
        with Vertical(id="mariadb-editor-dialog"):
            yield Label(
                f"Editing: {self.config_path}",
                id="mariadb-editor-title",
            )

            yield TextArea(
                self.initial_content,
                id="mariadb-editor",
                language="ini",
                soft_wrap=False,
            )

            with Horizontal(id="mariadb-editor-actions"):
                yield Button(
                    "Save",
                    id="mariadb-save",
                    variant="success",
                )
                yield Button("Cancel", id="mariadb-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "mariadb-cancel":
            self.dismiss(False)
            return

        if event.button.id != "mariadb-save":
            return

        content = self.query_one("#mariadb-editor", TextArea).text

        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(content, encoding="utf-8")

        except OSError as error:
            self.notify(
                f"Unable to save configuration: {error}",
                title="Save failed",
                severity="error",
            )
            return

        self.notify("Configuration saved successfully")
        self.dismiss(True)


class MariadbTab(TabPane):
    def __init__(self, **kwargs):
        super().__init__("MariaDB", **kwargs)

        self.config = APP_CONFIG.mariadb

        self.executable = self.config.executable or self.find_server_executable()

        self.client_executable = shutil.which("mariadb") or shutil.which("mysql")

        self.command = getattr(self.config, "command", None)

        self.pid_path = Path(self.config.pid_file).expanduser()
        self.log_path = Path(self.config.log_file).expanduser()

        self.config_path = self.get_optional_path("config_file")
        self.data_path = self.get_optional_path("data_dir")

        self.host = getattr(self.config, "host", None)
        self.port = getattr(self.config, "port", None)

    def find_server_executable(self) -> str | None:
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
        value = getattr(self.config, name, None)

        if value:
            return Path(value).expanduser()

        return None

    def compose(self) -> ComposeResult:
        with Vertical(id="mariadb-settings"):
            yield Label("MariaDB Server", classes="section-title")

            yield Static(
                f"Command: {self.command or 'Automatic detection'}",
                classes="config-value",
            )

            if self.executable:
                yield Button(
                    f"Server Executable: {self.executable}",
                    id="mariadb-executable",
                    classes="config-button",
                )
            else:
                yield Static(
                    "Server Executable: Not found",
                    classes="config-value",
                )

            if self.client_executable:
                yield Button(
                    f"Client Executable: {self.client_executable}",
                    id="mariadb-client",
                    classes="config-button",
                )
            else:
                yield Static(
                    "MariaDB client: Not found",
                    classes="config-value",
                )

            yield Label("Connection", classes="section-title")

            yield Static(
                f"Host: {self.host or 'Managed by MariaDB configuration'}",
                classes="config-value",
            )

            yield Static(
                f"Port: {self.port if self.port else 'Managed by MariaDB configuration'}",
                classes="config-value",
            )

            yield Label("Directories", classes="section-title")

            if self.data_path:
                yield Button(
                    f"Data Directory: {self.data_path}",
                    id="mariadb-data",
                    classes="config-button",
                )
            else:
                yield Static(
                    "Data Directory: Managed by my.cnf",
                    classes="config-value",
                )

            yield Label("Configuration", classes="section-title")

            if self.config_path:
                yield Button(
                    f"Edit Configuration: {self.config_path}",
                    id="mariadb-config",
                    variant="success",
                    classes="config-button",
                )
            else:
                yield Static(
                    "Configuration File: Using MariaDB defaults",
                    classes="config-value",
                )

            yield Label("Process Files", classes="section-title")

            yield Button(
                f"PID File: {self.pid_path}",
                id="mariadb-pid",
                classes="config-button",
            )

            yield Button(
                f"Log File: {self.log_path}",
                id="mariadb-log",
                classes="config-button",
            )

            yield Label("Quick Actions", classes="section-title")

            with Horizontal(classes="mariadb-actions"):
                yield Button(
                    "Open Log",
                    id="mariadb-open-log",
                    variant="primary",
                )

                yield Button(
                    "Open PID",
                    id="mariadb-open-pid",
                    variant="primary",
                )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "mariadb-config" and self.config_path:
            self.app.push_screen(
                MariaDBConfigEditor(self.config_path),
                callback=self.on_config_editor_closed,
            )
            return

        paths = {
            "mariadb-executable": self.executable,
            "mariadb-client": self.client_executable,
            "mariadb-data": self.data_path,
            "mariadb-pid": self.pid_path,
            "mariadb-log": self.log_path,
            "mariadb-open-log": self.log_path,
            "mariadb-open-pid": self.pid_path,
        }

        path = paths.get(button_id)

        if path:
            self.open_path(Path(path))

    def open_path(self, path: Path) -> None:
        path = path.expanduser()

        if not path.exists():
            self.notify(
                f"Path does not exist: {path}",
                title="Cannot open path",
                severity="warning",
            )
            return

        webbrowser.open(path.resolve().as_uri())

    def on_config_editor_closed(self, saved: bool | None) -> None:
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
