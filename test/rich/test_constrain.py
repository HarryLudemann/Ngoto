from ngoto.core.util.rich.console import Console
from ngoto.core.util.rich.constrain import Constrain
from ngoto.core.util.rich.text import Text


def test_width_of_none():
    console = Console()
    constrain = Constrain(Text("foo"), width=None)
    min_width, max_width = constrain.__rich_measure__(
        console, console.options.update_width(80)
    )
    assert min_width == 3
    assert max_width == 3
