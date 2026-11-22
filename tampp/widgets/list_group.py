from collections.abc import Iterable

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ListView

from .list_group_item import ListGroupItem


class ListGroup(Vertical):
    """A reusable list view with an optional title and items."""

    def __init__(
        self,
        title: str | None = None,
        items: Iterable[ListGroupItem] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.title = title
        self.items = list(items or [])

    def compose(self) -> ComposeResult:
        if self.title:
            yield Label(self.title, classes="list-group-title")
            # yield ListItem(
            #     Label(self.title, classes="list-group-title"),
            #     disabled=True,
            #     classes="list-group-header",
            # )
        yield ListView(*self.items)
        # yield from self.items
