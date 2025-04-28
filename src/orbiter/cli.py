import typer
from rich import print
from orbiter.core.maneuvers import hohmann_delta_v

# Create the main app
app = typer.Typer(add_completion=False, help="Orbiter command-line interface")

# Create a subgroup for maneuvers
maneuver_app = typer.Typer(help="Orbital maneuver calculations")

@maneuver_app.command("hohmann")
def hohmann(
    r1: float = typer.Argument(..., help="Initial orbit radius (meters)"),
    r2: float = typer.Argument(..., help="Target orbit radius (meters)")
):
    """Compute ΔV for a Hohmann transfer between two circular orbits."""
    dv1, dv2, total = hohmann_delta_v(r1, r2)
    print(f"🚀 1st impulse: [bold]{dv1:.2f}[/] m/s")
    print(f"🚀 2nd impulse: [bold]{dv2:.2f}[/] m/s")
    print(f"[green]Total ΔV: {total:.2f} m/s[/]")

# Attach the subgroup to the main app
app.add_typer(maneuver_app, name="maneuver")

if __name__ == "__main__":
    app()

