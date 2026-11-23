from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ListItem, Static

from screens import CodeEditorScreen
from utils import open_dir, open_url


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
                yield Label(
                    str(self.title),
                    classes="item-title",
                )

            if self.subtitle:
                yield Static(
                    str(self.subtitle),
                    classes="item-subtitle",
                )

            if self.url:
                yield Static(
                    str(self.url),
                    classes="item-url",
                )

            if self.path:
                yield Static(
                    f"{self.get_path_icon()} {str(self.path)}",
                    classes="item-path",
                )

    def on_click(self) -> None:
        """Open the associated resource when clicked."""

        if self.url:
            self._open_url()
        elif self.path:
            self._open_path()

    def _open_url(self) -> None:
        self.notify(f"Openinig url: {self.url}")
        if not open_url(self.url):
            self.notify(
                "Unable to open URL.",
                severity="error",
            )

    def _open_path(self) -> None:
        self.notify(f"Opening path: {self.path}")
        if not self.path.exists():
            self.notify(
                f"Path does not exist: {self.path}",
                severity="error",
            )
            return

        if self.path.is_dir():
            self._open_dir()
        elif self.path.is_file():
            self._open_file()

    def _open_dir(self) -> None:
        self.notify(f"Opening dir: {self.path}")
        if not open_dir(self.path):
            self.notify(
                "Unable to open directory.",
                severity="error",
            )

    def _open_file(self) -> None:
        # from screens.code_editor import CodeEditorScreen

        self.app.push_screen(CodeEditorScreen(self.path))
