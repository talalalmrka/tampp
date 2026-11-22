import webbrowser

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static, TabPane, TextArea

from tampp.config import APP_CONFIG
from tampp.services.platform import find_php
from tampp.widgets.divider import Divider
from tampp.widgets.fg_button import FgButton
from tampp.widgets.status_item import StatusItem
from tampp.screens.file_editor import FileEditorScreen
from tampp.helpers import get_php_version


class IniEditorScreen(ModalScreen):
    def __init__(self, ini_path: Path):
        super().__init__()

        self.ini_path = Path(ini_path).expanduser()

        try:
            self.initial_content = (
                self.ini_path.read_text(encoding="utf-8")
                if self.ini_path.is_file()
                else ""
            )
        except OSError:
            self.initial_content = ""

    def compose(self) -> ComposeResult:
        with Vertical(id="ini-editor-dialog", classes="ini-editor-screen"):
            yield Label(
                f"Editing: {self.ini_path}",
                id="ini-editor-title",
                classes="ini-editor-title",
            )
            with Container(classes="ini-editor-content"):
                yield TextArea.code_editor(
                    self.initial_content,
                    id="ini-editor",
                    classes="ini-editor-textarea",
                    language="ini",
                    soft_wrap=False,
                )

            with Horizontal(id="ini-editor-actions", classes="ini-editor-actions"):
                yield Button("Save", id="ini-save", variant="success")
                yield Button("Cancel", id="ini-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ini-cancel":
            self.dismiss(False)
            return

        if event.button.id != "ini-save":
            return

        content = self.query_one("#ini-editor", TextArea).text

        try:
            self.ini_path.parent.mkdir(parents=True, exist_ok=True)
            self.ini_path.write_text(content, encoding="utf-8")

        except OSError as error:
            self.notify(
                f"Unable to save php.ini: {error}",
                title="Save failed",
                severity="error",
            )
            return

        self.notify("php.ini saved successfully", severity="information")
        self.dismiss(True)


class PhpTab(TabPane):
    def __init__(self, **kwargs):
        super().__init__("PHP", **kwargs)

        self.config = APP_CONFIG.php

        self.document_root = Path(self.config.root).expanduser()
        self.ini_path = Path(self.config.ini_path).expanduser()
        self.router_path = Path(self.config.router_path).expanduser()
        self.dashboard_path = Path(self.config.dashboard_path).expanduser()
        self.php_info_path = Path(self.config.php_info_path).expanduser()
        self.temp_path = Path(self.config.temp_path).expanduser()
        self.log_path = Path(self.config.log_file).expanduser()
        self.pid_path = Path(self.config.pid_file).expanduser()

        self.executable = (
            self.config.executable or find_php() or "PHP executable not found"
        )
        self.php_version = self.config.php_version
        self.base_url = f"http://localhost:{self.config.port}"
        self.dashboard_url = f"{self.base_url}/dashboard"
        self.php_info_url = f"{self.base_url}/dashboard/phpinfo.php"
        self.phpmyadmin_url = f"{self.base_url}/dashboard/phpmyadmin"

    def get_status_items(self) -> list[StatusItem]:
        return [
            StatusItem(
                id="php-host",
                label="Host",
                content=self.config.host,
            ),
            StatusItem(
                id="php-port",
                label="Port",
                content=self.config.port,
            ),
            StatusItem(
                id="php-version",
                label="Version",
                content=self.config.php_version,
            ),
            StatusItem(
                id="php-executable",
                label="Executable",
                content=self.executable,
                onclick=True,
            ),
            StatusItem(
                id="php-url",
                label="Server url",
                content=self.base_url,
                onclick=True,
            ),
            StatusItem(
                id="dashboard-url",
                label="Dashboard url",
                content=self.dashboard_url,
                onclick=True,
            ),
            StatusItem(
                id="php-info-url",
                label="Php Info Url",
                content=self.php_info_url,
                onclick=True,
            ),
            StatusItem(
                id="phpmyadmin-url",
                label="Phpmyadmin url",
                content=self.phpmyadmin_url,
                onclick=True,
            ),
            StatusItem(
                id="php-document-root",
                label="Document Root",
                content=self.document_root,
                onclick=True,
            ),
            StatusItem(
                id="php-dashboard-path",
                label="Dashboard",
                content=self.dashboard_path,
                onclick=True,
            ),
            StatusItem(
                id="php-temp",
                label="Temporary Directory",
                content=self.temp_path,
                onclick=True,
            ),
            StatusItem(
                id="php-ini",
                label="Configuration (php.ini)",
                content=self.ini_path,
                onclick=True,
            ),
            StatusItem(
                id="php-router",
                label="Router",
                content=self.router_path,
                onclick=True,
            ),
            StatusItem(
                id="php-log",
                label="Log File",
                content=self.log_path,
                onclick=True,
            ),
            StatusItem(
                id="php-pid",
                label="PID File",
                content=self.pid_path,
                onclick=True,
            ),
        ]

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="php-settings"):
            yield Label("PHP Server", classes="section-title")
            # for item in self.get_status_items():
            #     yield Button(
            #         f"{item.label}:\n{item.content}",
            #         id=f"btn-{item.id}",
            #         flat=False,
            #         classes="status-item-btn",
            #     )

            for index, item in enumerate(self.get_status_items()):
                if index % 2 == 0:
                    item.classes = "status-item striped"
                else:
                    item.classes = "status-item"
                yield item
                # if index < len(self.get_status_items()) - 1:
                #     yield Divider()

            yield Static(
                f"Host: {self.config.host}",
                classes="config-value",
            )

            yield Button(
                f"Open server: {self.base_url}",
                id="php-open-server",
                variant="primary",
                classes="config-button",
            )

            yield Static(
                f"Port: {self.config.port}",
                classes="config-value",
            )

            yield Label("PHP Executable", classes="section-title")
            yield Button(
                f"Open: {self.executable}",
                id="php-executable-button",
                classes="config-button",
            )

            yield Label("Directories", classes="section-title")

            yield Button(
                f"Document Root: {self.document_root}",
                id="php-root",
                classes="config-button",
            )

            yield Button(
                f"Dashboard: {self.dashboard_path}",
                id="php-dashboard-path-button",
                classes="config-button",
            )

            yield Button(
                f"Temporary Directory: {self.temp_path}",
                id="php-temp-button",
                classes="config-button",
            )

            yield Label("Configuration Files", classes="section-title")

            yield Button(
                f"Edit php.ini: {self.ini_path}",
                id="php-ini-button",
                variant="success",
                classes="config-button",
            )

            yield Button(
                f"Router: {self.router_path}",
                id="php-router-button",
                classes="config-button",
            )

            yield Label("Logs and Process", classes="section-title")

            yield Button(
                f"Log File: {self.log_path}",
                id="php-log-button",
                classes="config-button",
            )

            yield Button(
                f"PID File: {self.pid_path}",
                id="php-pid-button",
                classes="config-button",
            )

            yield Label("Quick Links", classes="section-title")

            with Horizontal(classes="php-links"):
                yield Button(
                    "phpinfo",
                    id="php-info-url",
                    variant="primary",
                )

                yield Button(
                    "Dashboard",
                    id="php-dashboard-url",
                    variant="primary",
                )

                yield Button(
                    "phpMyAdmin",
                    id="phpmyadmin-url",
                    variant="primary",
                )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "php-ini-button":
            self.app.push_screen(
                IniEditorScreen(self.ini_path),
                callback=self.on_ini_editor_closed,
            )
            return

        urls = {
            "php-open-server": self.base_url,
            "php-info-url": self.php_info_url,
            "php-dashboard-url": self.dashboard_url,
            "phpmyadmin-url": self.phpmyadmin_url,
        }

        if button_id in urls:
            self.app.open_url(urls[button_id])
            return

        paths = {
            "php-executable": Path(self.executable),
            "php-root": self.document_root,
            "php-dashboard-path": self.dashboard_path,
            "php-temp": self.temp_path,
            "php-router": self.router_path,
            "php-log": self.log_path,
            "php-pid": self.pid_path,
        }

        path = paths.get(button_id)

        if path is not None:
            self.open_path(path)

    def open_path(self, path: Path) -> None:
        path = path.expanduser()

        if not path.exists():
            path = path.parent

        if not path.exists():
            self.notify(
                f"Path does not exist: {path}",
                title="Cannot open path",
                severity="warning",
            )
            return

        webbrowser.open(path.resolve().as_uri())

    def on_ini_editor_closed(self, saved: bool | None) -> None:
        if saved:
            self.notify(
                "PHP configuration updated. Restart PHP to apply changes.",
                title="Configuration saved",
                severity="information",
            )

            log_event = getattr(self.app, "log_event", None)

            if callable(log_event):
                log_event("php", "php.ini configuration updated")

    def on_status_item_clicked(self, event: StatusItem.Clicked) -> None:
        item_id = event.item_id
        match item_id:
            case "php-ini":
                self.app.push_screen(
                    IniEditorScreen(self.ini_path),
                    callback=self.on_ini_editor_closed,
                )
            case "php-executable":
                self.open_path(Path(self.executable))
            case "php-document-root":
                self.open_path(self.document_root)
            case "php-dashboard-path":
                self.open_path(self.dashboard_path)
            case "php-temp":
                self.open_path(self.temp_path)
            case "php-router":
                self.open_path(self.router_path)
            case "php-log":
                self.open_path(self.log_path)
            case "php-pid":
                self.open_path(self.pid_path)
            case _:
                self.notify(
                    f"Unknown status item clicked: {item_id}",
                    title="Status item clicked",
                    severity="warning",
                )

    def on_status_item_clickedd(self, event: StatusItem.Clicked) -> None:
        paths = {
            "php-executable": Path(self.executable),
            "php-document-root": self.document_root,
            "php-dashboard-path": self.dashboard_path,
            "php-temp": self.temp_path,
            "php-router": self.router_path,
            "php-log": self.log_path,
            "php-pid": self.pid_path,
        }
        if event.item_id == "php-ini":
            self.app.push_screen(
                IniEditorScreen(self.ini_path),
                callback=self.on_ini_editor_closed,
            )
            return
        path = paths.get(event.item_id)
        if path is not None:
            self.open_path(path)
