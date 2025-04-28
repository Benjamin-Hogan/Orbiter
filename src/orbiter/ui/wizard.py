from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, Static

from .panes.maneuvers import ManeuversPane
from .panes.propagation import PropagationPane
from .panes.constants import ConstantsPane

class CustomHeader(Header):
    def __init__(self, title: str, custom_content: str = ""):
        super().__init__(title)
        self.custom_content = custom_content

    def compose(self) -> ComposeResult:
        yield Static(self.custom_content, id="custom-content")
        yield from super().compose()

class Wizard(App):
    CSS_PATH = str(Path(__file__).with_name("wizard.css"))
    TITLE = "🛰️  Orbiter V1"

    def compose(self) -> ComposeResult:
        yield CustomHeader(self.TITLE, custom_content="Welcome to Orbiter Wizard!")

        # Create TabbedContent with tabs and their content directly
        yield TabbedContent(
            ("Maneuvers", ManeuversPane(id="tab-maneuvers")),
            ("Propagation", PropagationPane(id="tab-propagation")),
            ("Constants", ConstantsPane(id="tab-constants")),
            id="tabs"
        )

        yield Footer()

if __name__ == "__main__":
    Wizard().run()
