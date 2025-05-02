from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Button, Static
from textual import on
from orbiter.ui.panes.maneuvers.HohmannPane import HohmannPane  # Explicit class import
from orbiter.ui.panes.maneuvers.PlaneChangePane import PlaneChangePane
from orbiter.ui.panes.time.UniversalTimeOfFlightPane import UniversalTimeOfFlightPane
from orbiter.ui.panes.time.TimeOfFlightToPositionPane import TimeOfFlightToPositionPane
from orbiter.ui.panes.propagation.TheKeplerProblemPane import TheKeplerProblemPane


class OrbiterApp(App):
    CSS_PATH = "wizard.tcss"  # Put layout and styling in here

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                # Maneuvers category
                yield Static("Maneuvers", classes="category-header")
                yield Button("Hohmann Transfer", id="btn-hohmann")
                yield Button("Plane Change", id="btn-plane-change")
                
                # Time calculations category
                yield Static("Time Calculations", classes="category-header")
                yield Button("Universal Time of Flight", id="btn-universal-tof")
                yield Button("Time of Flight to Position", id="btn-tof-position")
                
                # Propagation category
                yield Static("Propagation", classes="category-header")
                yield Button("Kepler Problem", id="btn-kepler")
                
            yield Container(HohmannPane(), id="main-pane")  # Default view
        yield Footer()

    # Maneuvers handlers
    @on(Button.Pressed, "#btn-hohmann")
    def show_hohmann(self) -> None:
        self.switch_main_pane(HohmannPane)

    @on(Button.Pressed, "#btn-plane-change")
    def show_plane_change(self) -> None:
        self.switch_main_pane(PlaneChangePane)

    # Time calculation handlers
    @on(Button.Pressed, "#btn-universal-tof")
    def show_universal_tof(self) -> None:
        self.switch_main_pane(UniversalTimeOfFlightPane)

    @on(Button.Pressed, "#btn-tof-position")
    def show_tof_position(self) -> None:
        self.switch_main_pane(TimeOfFlightToPositionPane)

    # Propagation handlers
    @on(Button.Pressed, "#btn-kepler")
    def show_kepler(self) -> None:
        self.switch_main_pane(TheKeplerProblemPane)

    def switch_main_pane(self, pane_class):
        main = self.query_one("#main-pane", Container)
        main.remove_children()
        main.mount(pane_class())

if __name__ == "__main__":
    OrbiterApp().run()
