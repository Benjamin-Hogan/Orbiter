import orbiter.core.maneuvers.PlaneChange as pc
from textual.widgets import Static
from textual.containers import Container


class PlaneChangePane(Container):
    def compose(self):
        yield Static("This is the Plane Change pane")
        # Add your UI components here, e.g., buttons, inputs, etc.
        # You can use the methods from the imported module `pc` to perform calculations or transformations.