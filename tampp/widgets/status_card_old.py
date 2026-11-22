from textual.containers import Horizontal, Vertical, Container
from textual.message import Message
from textual.widgets import Static

from tampp.models import ServerStatus


class StatusCard(Container):
    class Pressed(Message):
        def __init__(self, card_id: str) -> None:
            super().__init__()
            self.card_id = card_id

    def __init__(
        self,
        title: str,
        id: str,
        status: ServerStatus = ServerStatus.OFF,
        **kwargs,
    ):
        super().__init__(
            id=id,
            classes="status-card",
            **kwargs,
        )

        self.title = title
        self.status = status

    def compose(self):
        yield Static(self.title, classes="card-title")

        with Horizontal(classes="card-status-row"):
            yield Static(
                "●",
                id="status-indicator",
                classes="status-indicator",
            )

            yield Static(
                self.status.value.upper(),
                id="status",
                classes="card-status",
            )

    def on_click(self) -> None:
        self.post_message(self.Pressed(self.id))

    def set_status(self, status: ServerStatus) -> None:
        self.status = status

        self.query_one("#status", Static).update(status.value.upper())

        self.remove_class(
            "status-on",
            "status-off",
            "status-pending",
        )

        self.add_class(f"status-{status.value}")
