import webbrowser

from pathlib import Path

from tampp.widgets import ListGroup
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static, TabPane, TextArea

from tampp.config import APP_CONFIG
from tampp.services.platform import find_php
from tampp.widgets import StatusItem, ListGroup, ListGroupItem
from tampp.screens import CodeEditorScreen
from tampp.helpers import get_php_version


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

    def get_groups(self) -> list[ListGroup]:
        return [
            ListGroup(
                title="Info",
                items=[
                    ListGroupItem(
                        title="Host",
                        subtitle=self.config.host,
                    ),
                    ListGroupItem(
                        title="Port",
                        subtitle=self.config.port,
                    ),
                    ListGroupItem(
                        title="Php version",
                        subtitle=self.config.php_version,
                    ),
                    ListGroupItem(
                        title="Executable",
                        subtitle=self.executable,
                    ),
                ],
            ),
            ListGroup(
                title="Links",
                items=[
                    ListGroupItem(
                        title="Server Url",
                        url=self.base_url,
                    ),
                    ListGroupItem(
                        title="Dashboard",
                        url=self.dashboard_url,
                    ),
                    ListGroupItem(
                        title="Phpinfo",
                        url=self.php_info_url,
                    ),
                    ListGroupItem(
                        title="Phpmyadmin",
                        url=self.phpmyadmin_url,
                    ),
                ],
            ),
            ListGroup(
                title="Paths",
                items=[
                    ListGroupItem(
                        title="Document Root",
                        path=self.document_root,
                    ),
                    ListGroupItem(
                        title="Dashboard",
                        path=self.dashboard_path,
                    ),
                    ListGroupItem(
                        title="Temp directory",
                        path=self.temp_path,
                    ),
                ],
            ),
            ListGroup(
                title="Files",
                items=[
                    ListGroupItem(
                        title="Configuration (php.ini)",
                        path=self.ini_path,
                    ),
                    ListGroupItem(
                        title="Router",
                        path=self.router_path,
                    ),
                    ListGroupItem(
                        title="Log File",
                        path=self.log_path,
                    ),
                    ListGroupItem(
                        title="Pid File",
                        path=self.pid_path,
                    ),
                ],
            ),
        ]

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="php-settings"):
            yield from self.get_groups()
