import asyncio

from textual.app import App, ComposeResult
from textual.containers import Container, Grid, Vertical
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, TabPane, TabbedContent

from tampp.config import APP_CONFIG
from tampp.models import ServerStatus
from tampp.services import MariaDBConfig, MariaDBServer, PhpServer, PhpServerConfig
from tampp.tabs import LogTab, MariadbTab, PhpIniTab, PhpTab, SettingsTab
from tampp.widgets import StatusCard


class TamppServer(App):
    TITLE = "TAMP Server Manager"
    CSS_PATH = "app.tcss"

    php_status = reactive(ServerStatus.OFF)
    mariadb_status = reactive(ServerStatus.OFF)

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "start_all", "Start all"),
        ("x", "stop_all", "Stop all"),
        ("right", "next_tab", "Next Tab"),
        ("left", "previous_tab", "Previous Tab"),
    ]

    def __init__(self):
        super().__init__()

        self.pending_targets = {}

        self.php_server = PhpServer(
            PhpServerConfig(
                document_root=APP_CONFIG.php.root,
                host=APP_CONFIG.php.host,
                port=APP_CONFIG.php.port,
                executable=APP_CONFIG.php.executable,
                router=(
                    APP_CONFIG.php.router_path
                    if APP_CONFIG.php.router_path.is_file()
                    else None
                ),
                ini_file=(
                    APP_CONFIG.php.ini_path
                    if APP_CONFIG.php.ini_path.is_file()
                    else None
                ),
                log_file=APP_CONFIG.php.log_file,
            )
        )

        self.mariadb_server = MariaDBServer(
            MariaDBConfig(
                executable=APP_CONFIG.mariadb.executable,
                pid_file=APP_CONFIG.mariadb.pid_file,
                log_file=APP_CONFIG.mariadb.log_file,
            )
        )

        self.services = {
            "php": self.php_server,
            "mariadb": self.mariadb_server,
        }

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            with Container(classes="status-container"):
                with Grid(classes="status-grid"):
                    yield StatusCard(
                        "PHP Server",
                        id="php-card",
                        status=self.php_status,
                    )

                    yield StatusCard(
                        "MariaDB Server",
                        id="mariadb-card",
                        status=self.mariadb_status,
                    )

                with Grid(classes="status-grid"):
                    yield Button(
                        "Start All",
                        id="start-all",
                        variant="success",
                        classes="status-btn",
                        flat=True,
                    )
                    yield Button(
                        "Stop All",
                        id="stop-all",
                        variant="error",
                        classes="status-btn",
                        flat=True,
                    )

            with TabbedContent(classes="main-tabs"):
                yield LogTab(
                    id="tab-log",
                    log_files={
                        "PHP": APP_CONFIG.php.log_file,
                        "MariaDB": APP_CONFIG.mariadb.log_file,
                    },
                )
                yield PhpTab(
                    id="tab-php",
                )
                yield MariadbTab(
                    id="tab-mariadb",
                )
                yield PhpIniTab(
                    id="tab-php-ini",
                )
                yield SettingsTab(
                    id="tab-settings",
                )

        yield Footer()

    def on_mount(self) -> None:
        self.run_worker(self.refresh_statuses())

    async def refresh_statuses(self) -> None:
        loop = asyncio.get_running_loop()

        for name, service in self.services.items():
            try:
                running = await loop.run_in_executor(
                    None,
                    service.is_running,
                )
            except Exception:
                running = False

            status = ServerStatus.ON if running else ServerStatus.OFF
            self.set_server_status(name, status)

    def set_server_status(
        self,
        name: str,
        status: ServerStatus,
    ) -> None:
        setattr(self, f"{name}_status", status)
        self.sync_server(name, status)

    def sync_server(
        self,
        name: str,
        status: ServerStatus,
    ) -> None:
        card = self.query_one(f"#{name}-card", StatusCard)
        card.set_status(status)

    def on_status_card_pressed(
        self,
        event: StatusCard.Pressed,
    ) -> None:
        if event.card_id == "php-card":
            self.toggle_server("php")

        elif event.card_id == "mariadb-card":
            self.toggle_server("mariadb")

    def toggle_server(self, name: str) -> None:
        current_status = getattr(self, f"{name}_status")

        if current_status == ServerStatus.PENDING:
            return

        target_status = (
            ServerStatus.OFF if current_status == ServerStatus.ON else ServerStatus.ON
        )

        self.transition_server(name, target_status)

    def transition_server(
        self,
        name: str,
        target_status: ServerStatus,
    ) -> None:
        current_status = getattr(self, f"{name}_status")

        if current_status == ServerStatus.PENDING:
            return

        if current_status == target_status:
            return

        self.pending_targets[name] = target_status
        self.set_server_status(name, ServerStatus.PENDING)

        self.run_worker(
            self.perform_transition(name, target_status),
            group=f"service-{name}",
        )

    async def perform_transition(
        self,
        name: str,
        target_status: ServerStatus,
    ) -> None:
        service = self.services[name]
        loop = asyncio.get_running_loop()

        try:
            if target_status == ServerStatus.ON:
                await loop.run_in_executor(None, service.start)
            else:
                await loop.run_in_executor(None, service.stop)

            running = await loop.run_in_executor(
                None,
                service.is_running,
            )

            actual_status = ServerStatus.ON if running else ServerStatus.OFF

            self.set_server_status(name, actual_status)

        except Exception as error:
            try:
                running = await loop.run_in_executor(
                    None,
                    service.is_running,
                )
            except Exception:
                running = False

            actual_status = ServerStatus.ON if running else ServerStatus.OFF

            self.set_server_status(name, actual_status)

            self.notify(
                str(error),
                title=f"{name.capitalize()} service error",
                severity="error",
                timeout=8,
            )

        finally:
            self.pending_targets.pop(name, None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "start-all":
            self.start_all()

        elif button_id == "stop-all":
            self.stop_all()

    def start_all(self) -> None:
        self.transition_server("php", ServerStatus.ON)
        self.transition_server("mariadb", ServerStatus.ON)

    def stop_all(self) -> None:
        self.transition_server("php", ServerStatus.OFF)
        self.transition_server("mariadb", ServerStatus.OFF)

    def action_next_tab(self) -> None:
        self.query_one(TabbedContent).action_next_tab()

    def action_previous_tab(self) -> None:
        self.query_one(TabbedContent).action_previous_tab()


if __name__ == "__main__":
    TamppServer().run()
