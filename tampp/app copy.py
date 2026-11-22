from textual.app import App, ComposeResult
from textual.containers import Container, Grid, Vertical  # pyright: ignore[reportMissingImports]
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, TabbedContent

from tampp.models import ServerStatus
from tampp.tabs import (
    HomeTab,
    MariadbTab,
    PhpTab,
    SettingsTab,
)
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

            with TabbedContent(initial="home", classes="main-tabs"):
                yield HomeTab()
                yield PhpTab()
                yield MariadbTab()
                yield SettingsTab()

        yield Footer()

    # def on_mount(self) -> None:
    # self.sync_server("php", self.php_status)
    # self.sync_server("mariadb", self.mariadb_status)

    def sync_server(self, name: str, status: ServerStatus) -> None:
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

        setattr(self, f"{name}_status", ServerStatus.PENDING)
        self.sync_server(name, ServerStatus.PENDING)

        self.set_timer(
            1,
            lambda: self.complete_toggle(name),
        )

    def toggle_server(self, name: str) -> None:
        current_status = getattr(self, f"{name}_status")

        if current_status == ServerStatus.PENDING:
            return

        target_status = (
            ServerStatus.OFF if current_status == ServerStatus.ON else ServerStatus.ON
        )

        self.transition_server(name, target_status)

    def complete_toggle(self, name: str) -> None:
        target_status = self.pending_targets.pop(name, None)

        if target_status is None:
            return

        setattr(self, f"{name}_status", target_status)
        self.sync_server(name, target_status)

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
