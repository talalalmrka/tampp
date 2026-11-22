from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import TabPane, ListItem, ListView, Label
from tampp.widgets import FgListItem, FgListView, FgItem

from tampp.config import APP_CONFIG
from tampp.services.platform import find_php
from tampp.screens.file_editor import FileEditorScreen
from tampp.helpers import get_php_version


class ListTab(TabPane):
    def __init__(self, **kwargs):
        super().__init__("LIST", **kwargs)
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

    def get_items(self) -> list[FgItem]:
        return [
            FgItem(
                id="php-host",
                title="Host",
                subtitle=self.config.host,
            ),
            FgItem(
                id="php-port",
                title="Port",
                subtitle=self.config.port,
            ),
            FgItem(
                id="php-version",
                title="Version",
                subtitle=self.config.php_version,
            ),
            FgItem(
                id="php-executable",
                title="Executable",
                subtitle=self.executable,
            ),
            FgItem(
                id="php-url",
                title="Server url",
                url=self.base_url,
            ),
            FgItem(
                id="dashboard-url",
                title="Dashboard url",
                url=self.dashboard_url,
            ),
            FgItem(
                id="php-info-url",
                title="Php Info Url",
                url=self.php_info_url,
            ),
            FgItem(
                id="phpmyadmin-url",
                title="Phpmyadmin url",
                url=self.phpmyadmin_url,
            ),
            FgItem(
                id="php-document-root",
                title="Document Root",
                path=self.document_root,
            ),
            FgItem(
                id="php-dashboard-path",
                title="Dashboard",
                path=self.dashboard_path,
            ),
            FgItem(
                id="php-temp",
                title="Temporary Directory",
                path=self.temp_path,
            ),
            FgItem(
                id="php-ini",
                title="Configuration (php.ini)",
                file=self.ini_path,
            ),
            FgItem(
                id="php-router",
                title="Router",
                file=self.router_path,
            ),
            FgItem(
                id="php-log",
                title="Log File",
                file=self.log_path,
            ),
            FgItem(
                id="php-pid",
                title="PID File",
                file=self.pid_path,
            ),
        ]

    def compose(self) -> ComposeResult:
        yield ListView(
            *self.get_items(),
            # FgItem(
            #     id="php-version",
            #     title="Version",
            #     subtitle=self.config.php_version,
            # ),
            # FgItem(
            #     id="php-executable",
            #     title="Executable",
            #     subtitle=self.executable,
            # ),
            # FgItem(
            #     id="php-url",
            #     title="Server url",
            #     url=self.base_url,
            # ),
            # FgItem(
            #     id="dashboard-url",
            #     title="Dashboard url",
            #     url=self.dashboard_url,
            # ),
            classes="fg-items",
        )
        # yield FgListView(
        #     FgListItem(
        #         title="PHP Version",
        #         subtitle="PHP 8.5.6",
        #         link="https://www.php.net/",
        #     ),
        #     FgListItem(
        #         title="PHP Configuration",
        #         subtitle="Open php.ini",
        #         path="/usr/local/etc/php/8.5/php.ini",
        #     ),
        # )
