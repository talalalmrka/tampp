from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Static


class StatusItem(Horizontal):
    class Clicked(Message):
        def __init__(self, item_id: str) -> None:
            super().__init__()
            self.item_id = item_id

    def __init__(
        self,
        label: str,
        content: str,
        *,
        id: str,
        onclick: bool = False,
        classes: str | None = None,
    ) -> None:
        super().__init__(id=id, classes=classes)

        self.label = label
        self.content = str(content)
        self.onclick = onclick

    def compose(self) -> ComposeResult:
        yield Static(self.label, classes="status-item-label")
        yield Static(self.content, classes="status-item-content")

    def on_click(self) -> None:
        if self.onclick:
            self.post_message(self.Clicked(self.id))
