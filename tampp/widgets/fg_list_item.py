from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import ListItem, Static


class FgListItem(ListItem):
    """A reusable resource list item."""

    def __init__(
        self,
        title: str,
        subtitle: str | None = None,
        link: str | None = None,
        path: str | Path | None = None,
    ):
        super().__init__()

        self.title = title
        self.subtitle = subtitle
        self.link = link
        self.path = path

    def compose(self) -> ComposeResult:
        with Vertical(classes="fg-list-item-content"):
            yield Static(
                self.title,
                classes="fg-list-item-title",
            )

            if self.subtitle:
                yield Static(
                    self.subtitle,
                    classes="fg-list-item-subtitle",
                )
