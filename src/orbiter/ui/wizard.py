from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input

class Wizard(App):
    """Terminal-UI front door for Orbiter."""
    TITLE = "🛰️  Orbiter V1  — Hohmann ΔV Calculator"

    def compose(self) -> ComposeResult:
        yield Header()  # Removed 'title' and 'show_clock' arguments
        yield Static("Enter your orbit radii (SI units, metres):", id="prompt")
        yield Input(placeholder="Initial radius (e.g. 6771000)", id="input-r1")
        yield Input(placeholder="Target radius  (e.g. 42164000)", id="input-r2")
        yield Button("Compute ΔV", id="btn-hohmann")
        yield Static("", id="result")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-hohmann":
            # grab user text
            r1_str = self.query_one("#input-r1", Input).value
            r2_str = self.query_one("#input-r2", Input).value

            # try to parse & compute
            try:
                r1 = float(r1_str)
                r2 = float(r2_str)
                from orbiter.core.maneuvers import hohmann_delta_v
                dv1, dv2, total = hohmann_delta_v(r1, r2)

                # display nicely
                self.query_one("#result", Static).update(
                    f"🚀 ΔV₁: {dv1:,.1f} m/s   ΔV₂: {dv2:,.1f} m/s   •  Total: {total:,.1f} m/s"
                )
            except ValueError:
                self.query_one("#result", Static).update(
                    "[red]Invalid input. Please enter numeric values for both radii.[/]"
                )

if __name__ == "__main__":
    Wizard().run()
