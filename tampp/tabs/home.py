from textual.widgets import TabPane, Static


class HomeTab(TabPane):
    def __init__(self):
        super().__init__("Home", id="home")

    def compose(self):
        yield Static("Welcome to Home Page")
        yield Static("This is the home tab.")
