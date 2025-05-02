import orbiter.core.propagation.TheKeplerProblem as tkp
from textual.widgets import Static
from textual.containers import Container


class TheKeplerProblemPane(Container):
    def compose(self):
        yield Static("This is the The Kepler Problem pane")
        # Add your UI components here, e.g., buttons, inputs, etc.
        # You can use the methods from the imported module `tkp` to perform calculations or transformations.