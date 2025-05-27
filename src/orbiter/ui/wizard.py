from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Button, Static
from textual.widgets import Collapsible  # Uncomment this line
from textual import on
from orbiter.ui.panes.maneuvers.HohmannPane import HohmannPane
from orbiter.ui.panes.maneuvers.PlaneChangePane import PlaneChangePane
from orbiter.ui.panes.time.UniversalTimeOfFlightPane import UniversalTimeOfFlightPane
from orbiter.ui.panes.time.TimeOfFlightToPositionPane import TimeOfFlightToPositionPane
from orbiter.ui.panes.propagation.TheKeplerProblemPane import TheKeplerProblemPane


class OrbiterApp(App):
    CSS_PATH = "wizard.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                # Maneuvers category
                collapsible = Collapsible(title="Maneuvers")
                with collapsible:
                    yield Button("Hohmann Transfer", id="btn-hohmann", classes="dropdown-button")
                    yield Button("Plane Change", id="btn-plane-change", classes="dropdown-button")
                yield collapsible

                # Time calculations category
                collapsible = Collapsible(title="Time Calculations")
                with collapsible:
                    yield Button("Universal Time of Flight", id="btn-universal-tof", classes="dropdown-button")
                    yield Button("Time of Flight to Position", id="btn-tof-position", classes="dropdown-button")
                yield collapsible

                # Propagation category
                collapsible = Collapsible(title="Propagation")
                with collapsible:
                    yield Button("Kepler Problem", id="btn-kepler", classes="dropdown-button")
                yield collapsible
                
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
