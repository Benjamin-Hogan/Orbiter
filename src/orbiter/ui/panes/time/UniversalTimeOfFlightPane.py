import orbiter.core.time.UniversalTimeOfFlight as ut
from textual.widgets import Static
from textual.containers import Container


class UniversalTimeOfFlightPane(Container):
    def compose(self):
        yield Static("This is the Universal Time of Flight pane")
        # Add your UI components here, e.g., buttons, inputs, etc.
        # You can use the methods from the imported module `ut` to perform calculations or transformations.