from textual.binding import Binding
from textual.containers import Horizontal
from textual.events import Click
from textual.message import Message


class FgButton(Horizontal, can_focus=True):
    """A reusable button widget that can contain any child widgets."""

    BINDINGS = [
        Binding("enter", "press", "Press button", show=False),
        Binding("space", "press", "Press button", show=False),
    ]

    DEFAULT_CSS = """
    FgButton {
        width: auto;
        height: auto;
        background: $panel;
        border: tall $primary;
        padding: 0 2;
        align: center middle;
    }

    FgButton:hover {
        background: $primary-muted;
    }

    FgButton:focus {
        border: tall $accent;
        background: $primary-darken-1;
    }

    FgButton:disabled {
        opacity: 0.4;
        background: $panel;
    }

    FgButton * {
        background: transparent;
    }
    """

    class Pressed(Message):
        """Event sent when the button is clicked or activated via keyboard."""

        def __init__(self, button: "FgButton") -> None:
            self.button = button
            super().__init__()

    def action_press(self) -> None:
        """Trigger the button action when enabled."""
        if not self.disabled:
            self.post_message(self.Pressed(self))

    def on_click(self, event: Click) -> None:
        """Handle mouse clicks anywhere inside the container or its children."""
        event.stop()
        if not self.disabled:
            self.focus()
            self.action_press()
