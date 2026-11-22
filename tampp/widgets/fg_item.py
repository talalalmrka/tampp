from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, Link, ListItem, Static


class FgItem(ListItem):
    """A reusable resource list item."""

    def __init__(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        url: str | None = None,
        path: str | Path | None = None,
        file: str | Path | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.title = title
        self.subtitle = subtitle
        self.url = url
        self.path = Path(path) if path else None
        self.file = Path(file) if file else None

    def compose(self) -> ComposeResult:
        with Vertical(classes="fg-item-content"):
            if self.title:
                yield Label(
                    str(self.title),
                    classes="fg-item-title",
                )

            if self.subtitle:
                yield Static(
                    str(self.subtitle),
                    classes="fg-item-subtitle",
                )

            if self.url:
                yield Link(
                    f"🔗 {self.url}",
                    url=str(self.url),
                    tooltip=str(self.title or self.url),
                    classes="fg-item-url",
                )

            if self.path:
                yield Static(
                    f"📁 {self.path}",
                    classes="fg-item-path",
                )

            if self.file:
                yield Static(
                    f"📄 {self.file}",
                    classes="fg-item-file",
                )
