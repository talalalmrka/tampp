from textual.widgets import TabPane, Static


class SettingsTab(TabPane):
    def __init__(self, **kwargs):
        super().__init__("Settings", **kwargs)

    def compose(self):
        yield Static("Application Settings")
        yield Static("Configure your application here.")
