import webbrowser

from textual.message import Message
from textual.widgets import ListView

from tampp.helpers.system import open_path
from tampp.widgets.fg_list_item import FgListItem


class FgListView(ListView):
    """A clickable list of resources."""

    class ResourceOpened(Message):
        def __init__(self, item: FgListItem):
            self.item = item
            super().__init__()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item

        if not isinstance(item, FgListItem):
            return

        try:
            if item.link:
                webbrowser.open(item.link)

            elif item.path:
                open_path(item.path)

            else:
                return

            self.post_message(self.ResourceOpened(item))

        except Exception as error:
            self.app.notify(
                str(error),
                title="Unable to open resource",
                severity="error",
            )
