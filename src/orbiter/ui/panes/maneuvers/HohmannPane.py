import orbiter.core.maneuvers.Hohmann as hm
from textual.widgets import Static
from textual.containers import Container

class HohmannPane(Container):
    def compose(self):
        yield Static("Hohmann Transfer Calculator")
        yield Static("Coming soon...")
