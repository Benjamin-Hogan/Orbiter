import orbiter.core.maneuvers.Hohmann as hm
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input, Button, Label
from textual.app import ComposeResult
from rich.text import Text

class HohmannPane(Container):
    """Interface for calculating Hohmann transfer maneuvers."""
    
    DEFAULT_CSS = """
    HohmannPane {
        padding: 1;
    }
    
    #inputs {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    
    .input-row {
        height: 3;
        margin-bottom: 1;
        align-vertical: middle;
    }
    
    Label {
        width: 30;
        padding: 2;
    }
    
    Input {
        width: 30;
    }
    
    #results {
        margin-top: 2;
    }
    
    .result-text {
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Hohmann Transfer Calculator", id="title")
        
        with Vertical(id="inputs"):
            with Horizontal(classes="input-row"):
                yield Label("Initial orbit radius (m):")
                yield Input(placeholder="e.g. 6771000", id="r1")
            
            with Horizontal(classes="input-row"):
                yield Label("Target orbit radius (m):")
                yield Input(placeholder="e.g. 42164000", id="r2")
            
            yield Button("Calculate Transfer", id="calculate")
        
        with Vertical(id="results"):
            yield Static("", id="dv1", classes="result-text")
            yield Static("", id="dv2", classes="result-text")
            yield Static("", id="total", classes="result-text")
            yield Static("", id="transfer_orbit", classes="result-text")
            yield Static("", id="semi_latus", classes="result-text")
            yield Static("", id="tof", classes="result-text")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the calculate button press."""
        if event.button.id == "calculate":
            self._calculate_transfer()

    def _calculate_transfer(self) -> None:
        """Calculate and display the Hohmann transfer results."""
        try:
            # Get input values and validate
            r1_input = self.query_one("#r1").value
            r2_input = self.query_one("#r2").value
            
            if not r1_input or not r2_input:
                raise ValueError("Please enter both radii")
                
            r1 = float(r1_input)
            r2 = float(r2_input)
            
            if r1 <= 0 or r2 <= 0:
                raise ValueError("Orbit radii must be positive")
            
            # Calculate transfer - now handle all 6 return values
            dv1, dv2, dv_total, a_transfer, p_transfer, e_transfer = hm.hohmann_delta_v(r1, r2)
            
            # Update result displays
            self.query_one("#dv1").update(
                Text.assemble(("ΔV1: ", "bold green"), f"{dv1:.2f} m/s")
            )
            self.query_one("#dv2").update(
                Text.assemble(("ΔV2: ", "bold green"), f"{dv2:.2f} m/s")
            )
            self.query_one("#total").update(
                Text.assemble(("Total ΔV: ", "bold green"), f"{dv_total:.2f} m/s")
            )
            self.query_one("#transfer_orbit").update(
                Text.assemble(
                    ("Transfer orbit semi-major axis: ", "bold green"), 
                    f"{a_transfer/1000:.2f} km"
                )
            )
            self.query_one("#semi_latus").update(
                Text.assemble(
                    ("Semi-latus rectum: ", "bold green"), 
                    f"{p_transfer/1000:.2f} km"
                )
            )
            self.query_one("#tof").update(
                Text.assemble(
                    ("Time of Flight of Orbit: ", "bold green"), 
                    f"{e_transfer/3600:.4f} hrs"
                )
            )
        except ValueError as e:
            # Handle invalid input with specific error message
            error_msg = str(e) if str(e) else "Please enter valid numbers"
            self.query_one("#dv1").update(
                Text(f"Error: {error_msg}", style="bold red")
            )
            self.query_one("#dv2").update("")
            self.query_one("#total").update("")
            self.query_one("#transfer_orbit").update("")
            self.query_one("#semi_latus").update("")
            self.query_one("#tof").update("")
