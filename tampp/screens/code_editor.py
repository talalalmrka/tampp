from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static, TextArea


class CodeEditorScreen(Screen):
    """A reusable file-based code editor screen."""

    TITLE = "Edit file"
    BINDINGS = [
        Binding("ctrl+s", "save_file", "Save", priority=True),
        Binding("escape", "close_editor", "Close"),
    ]

    # CSS_PATH = "code_editor.tcss"

    LANGUAGE_MAP = {
        ".py": "python",
        ".php": "php",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".md": "markdown",
        ".sql": "sql",
        ".sh": "bash",
        ".bash": "bash",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".xml": "xml",
        ".txt": None,
    }

    def __init__(self, file_path: str | Path, **kwargs) -> None:
        super().__init__(**kwargs)

        self.file_path = Path(file_path).expanduser().resolve()
        self.saved_text = ""

        if self.file_path.exists():
            self.saved_text = self.file_path.read_text(encoding="utf-8")

        self.language = self.LANGUAGE_MAP.get(self.file_path.suffix.lower())

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(
            id="code-editor-container",
            classes="code-editor-container",
        ):
            yield Label(
                str(self.file_path),
                id="code-editor-path",
                classes="code-editor-path",
            )

            yield TextArea.code_editor(
                self.saved_text,
                language=self.language,
                id="code-editor-textarea",
                classes="code-editor-textarea",
            )

            with Container(
                id="code-editor-actions",
                classes="code-editor-actions",
            ):
                with Container(
                    id="buttons-container",
                    classes="buttons-container",
                ):
                    yield Button(
                        "Save",
                        id="save-button",
                        classes="btn save-button",
                        variant="primary",
                        flat=True,
                    )

                    yield Button(
                        "Close",
                        id="close-button",
                        classes="btn save-button",
                        variant="error",
                        flat=True,
                    )

                yield Static(
                    "Saved",
                    id="code-editor-status",
                    classes="code-editor-status",
                )

        yield Footer()

    def on_mount(self) -> None:
        self.editor.focus()

    @property
    def editor(self) -> TextArea:
        return self.query_one("#code-editor-textarea", TextArea)

    @property
    def is_dirty(self) -> bool:
        return self.editor.text != self.saved_text

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-button":
            self.action_save_file()

        elif event.button.id == "close-button":
            self.action_close_editor()

    def on_text_area_changed(
        self,
        event: TextArea.Changed,
    ) -> None:
        self.update_status()

    def update_status(self) -> None:
        status = self.query_one("#code-editor-status", Static)

        if self.is_dirty:
            status.update("Modified • Unsaved changes")
        else:
            status.update("Saved")

    def action_save_file(self) -> None:
        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.file_path.write_text(
                self.editor.text,
                encoding="utf-8",
            )

            self.saved_text = self.editor.text
            self.update_status()
            self.notify("File saved successfully.")

        except OSError as error:
            self.notify(
                f"Save failed: {error}",
                severity="error",
            )

    def action_close_editor(self) -> None:
        if self.is_dirty:
            self.notify(
                "Unsaved changes. Save before closing.",
                severity="warning",
            )
            return

        self.app.pop_screen()
