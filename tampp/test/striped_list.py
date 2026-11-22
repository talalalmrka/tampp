from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Static


class StripedList(App):

    CSS = """
    ListView {
        padding: 0 1;
    }

    ListItem {
        height: 3;
        margin: 0 0 1 0;
        padding: 0 1;
    }

    ListItem:odd {
        background: $surface;
    }

    ListItem:even {
        background: $boost;
    }

    ListView {
        keyline: thin $border;
    }

    ListItem.-highlight {
        background: $primary;
        color: $text;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        items = ["PHP", "MariaDB", "Apache", "Nginx", "Python", "Node.js"]

        yield ListView(
            *[ListItem(Static(item)) for item in items]
        )


if __name__ == "__main__":
    StripedList().run()
