import asyncio
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ListItem, Static

from tampp.screens import CodeEditorScreen
from tampp.utils import open_path, open_url


class ListGroupItem(ListItem):
    """A reusable resource list item."""

    def __init__(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        url: str | None = None,
        path: str | Path | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.title = title
        self.subtitle = subtitle
        self.url = url
        self.path = Path(path).expanduser() if path else None

    def get_path_icon(self) -> str:
        if not self.path:
            return ""

        if self.path.is_file():
            return "📄"

        if self.path.is_dir():
            return "📁"

        return "❓"

    def compose(self) -> ComposeResult:
        with Vertical(classes="item-content"):
            if self.title:
                yield Label(str(self.title), classes="item-title")

            if self.subtitle:
                yield Static(str(self.subtitle), classes="item-subtitle")

            if self.url:
                yield Static(str(self.url), classes="item-url")

            if self.path:
                yield Static(
                    f"{self.get_path_icon()} {self.path}",
                    classes="item-path",
                )

    async def on_click(self) -> None:
        """Apply a press effect and open the associated resource."""

        self.add_class("pressed")

        try:
            await asyncio.sleep(0.12)
        finally:
            self.remove_class("pressed")

        if self.url:
            self._open_url()
        elif self.path:
            self._open_path()

    def _open_url(self) -> None:
        self.notify(f"Opening URL: {self.url}")

        if not open_url(self.url):
            self.notify("Unable to open URL.", severity="error")

    def _open_path(self) -> None:
        self.notify(f"Opening path: {self.path}")

        # if not self.path.exists():
        #     self.notify(
        #         f"Path does not exist: {self.path}",
        #         severity="error",
        #     )
        #     return

        if self.path.is_dir():
            self._open_dir()
        elif self.path.is_file():
            self._open_file()

    def _open_dir(self) -> None:
        if not open_path(self.path):
            self.notify("Unable to open directory.", severity="error")

    def _open_file(self) -> None:
        self.app.push_screen(CodeEditorScreen(self.path))
