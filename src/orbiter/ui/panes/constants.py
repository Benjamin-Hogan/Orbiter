from textual.widgets import TabPane, Static
from textual.app import ComposeResult
from orbiter.core.states import MU_EARTH  # if you add more

class ConstantsPane(TabPane):
    """Encapsulates the Constants tab."""

    TITLE = "Constants"

    def __init__(self, *, id: str | None = None):
        super().__init__(title=self.TITLE, id=id)

    def compose(self) -> ComposeResult:
        yield Static("Physical Constants", classes="pane-title")
        yield Static(f"• μₑ (Earth) = {MU_EARTH:.3e} m³/s²")
