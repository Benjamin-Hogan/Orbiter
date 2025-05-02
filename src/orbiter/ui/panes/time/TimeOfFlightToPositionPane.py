import orbiter.core.time.TimeOfFlightToPosition as tof
from textual.widgets import Static
from textual.containers import Container


class TimeOfFlightToPositionPane(Container):
    def compose(self):
        yield Static("This is the Time of Flight to Position pane")
        # Add your UI components here, e.g., buttons, inputs, etc.
        # You can use the methods from the imported module `tof` to perform calculations or transformations.