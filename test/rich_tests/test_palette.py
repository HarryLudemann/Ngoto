from ngoto.core.util.rich._palettes import STANDARD_PALETTE
from ngoto.core.util.rich.table import Table


def test_rich_cast():
    table = STANDARD_PALETTE.__rich__()
    assert isinstance(table, Table)
    assert table.row_count == 16
