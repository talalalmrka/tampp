from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TextArea, Header, Footer


class FileEditorScreen(ModalScreen):
    def __init__(self, file_path: Path | str):
        super().__init__()

        self.file_path = Path(file_path).expanduser()
        self.initial_content = ""

        self.language = self._detect_language()

    def _detect_language(self) -> str | None:
        languages = {
            ".py": "python",
            ".php": "php",
            ".js": "javascript",
            ".ts": "typescript",
            ".html": "html",
            ".css": "css",
            ".json": "json",
            ".xml": "xml",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
            ".ini": "ini",
            ".sh": "bash",
            ".sql": "sql",
            ".md": "markdown",
        }

        return languages.get(self.file_path.suffix.lower())

    def on_mount(self) -> None:
        if not self.file_path.exists():
            return

        if not self.file_path.is_file():
            self.notify(
                "The selected path is not a file.",
                title="Invalid file",
                severity="error",
            )
            self.dismiss(False)
            return

        try:
            self.initial_content = self.file_path.read_text(encoding="utf-8")

            self.query_one("#file-editor", TextArea).text = self.initial_content

        except (OSError, UnicodeError) as error:
            self.notify(
                str(error),
                title="Unable to read file",
                severity="error",
            )
            self.dismiss(False)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="file-editor-dialog"):
            yield Label(
                f"Editing: {self.file_path}",
                id="file-editor-title",
            )

            yield TextArea.code_editor(
                self.initial_content,
                id="file-editor",
                language=self.language,
                soft_wrap=False,
            )

            with Horizontal(id="file-editor-actions"):
                yield Button(
                    "Save",
                    id="file-save",
                    variant="success",
                )

                yield Button(
                    "Cancel",
                    id="file-cancel",
                )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "file-cancel":
            self.dismiss(False)
            return

        if event.button.id != "file-save":
            return
        self.save_file()

    def action_save_file(self) -> None:
        editor = self.query_one("#file-editor", TextArea)

        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.file_path.write_text(
                editor.text,
                encoding="utf-8",
            )

        except OSError as error:
            self.notify(
                str(error),
                title="Save failed",
                severity="error",
            )
            return

        self.notify(
            f"Saved: {self.file_path.name}",
            severity="information",
        )

        self.dismiss(True)
