from textual.widgets import TabPane, Static, Input, Button
from textual.app import ComposeResult
from rich.text import Text

from orbiter.core.maneuvers import hohmann_delta_v

class ManeuversPane(TabPane):
    """Encapsulates the Maneuvers tab."""

    TITLE = "Maneuvers"

    def __init__(self, *, id: str | None = None):
        super().__init__(title=self.TITLE, id=id)

    def compose(self) -> ComposeResult:
        yield Static("Hohmann ΔV", classes="pane-title")
        yield Input(id="m-r1", placeholder="Initial radius r₁ (m)")
        yield Input(id="m-r2", placeholder="Target  radius r₂ (m)")
        yield Button("Compute ΔV", id="m-compute")
        yield Static("", id="m-result", markup=False, classes="result-box")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "m-compute":
            return
        result = self.query_one("#m-result", Static)
        try:
            r1 = float(self.query_one("#m-r1", Input).value or 0)
            r2 = float(self.query_one("#m-r2", Input).value or 0)
            dv1, dv2, tot = hohmann_delta_v(r1, r2)
            txt = f"ΔV₁={dv1:,.1f} m/s   ΔV₂={dv2:,.1f} m/s   Total={tot:,.1f} m/s"
            result.update(Text(txt, markup=False))
        except Exception as e:
            result.update(Text(f"Error: {e}", style="red", markup=False))
