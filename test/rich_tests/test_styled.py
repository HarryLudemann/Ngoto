import io

from ngoto.core.util.rich.console import Console
from ngoto.core.util.rich.measure import Measurement
from ngoto.core.util.rich.styled import Styled


def test_styled():
    styled_foo = Styled("foo", "on red")
    console = Console(file=io.StringIO(), force_terminal=True, _environ={})
    assert Measurement.get(console, console.options, styled_foo) == Measurement(3, 3)
    console.print(styled_foo)
    result = console.file.getvalue()
    expected = "\x1b[41mfoo\x1b[0m\n"
    assert result == expected