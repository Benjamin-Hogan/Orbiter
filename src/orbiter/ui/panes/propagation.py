from textual.widgets import TabPane, Static, Input, Button
from textual.app import ComposeResult
from rich.text import Text
import numpy as np

from orbiter.core.propagate import propagate_two_body
from orbiter.core.states import StateRV

class PropagationPane(TabPane):
    """Encapsulates the Propagation tab."""

    TITLE = "Propagation"

    def __init__(self, *, id: str | None = None):
        super().__init__(title=self.TITLE, id=id)

    def compose(self) -> ComposeResult:
        yield Static("Two-Body Propagation", classes="pane-title")
        yield Input(id="p-r0",    placeholder="r₀ as x,y,z (m)")
        yield Input(id="p-v0",    placeholder="v₀ as vx,vy,vz (m/s)")
        yield Input(id="p-tmax",  placeholder="Duration (s)")
        yield Input(id="p-dt",    placeholder="Time step (s)")
        yield Button("Run Propagation", id="p-compute")
        yield Static("", id="p-result", markup=False, classes="result-box")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "p-compute":
            return
        result = self.query_one("#p-result", Static)
        try:
            r0 = np.fromstring(self.query_one("#p-r0", Input).value or "", sep=",")
            v0 = np.fromstring(self.query_one("#p-v0", Input).value or "", sep=",")
            tmax = float(self.query_one("#p-tmax", Input).value or 0)
            dt   = float(self.query_one("#p-dt",  Input).value or 0)

            if r0.size != 3 or v0.size != 3:
                raise ValueError("r₀/v₀ must be three comma-separated numbers")

            traj = propagate_two_body(StateRV(r0, v0), tmax, dt)
            rf, vf = traj[-1].r, traj[-1].v
            txt = (
                f"Ran {len(traj)} steps.\n"
                f"Final r = [{rf[0]:.1f}, {rf[1]:.1f}, {rf[2]:.1f}] m\n"
                f"Final v = [{vf[0]:.1f}, {vf[1]:.1f}, {vf[2]:.1f}] m/s"
            )
            result.update(Text(txt, markup=False))
        except Exception as e:
            result.update(Text(f"Error: {e}", style="red", markup=False))
