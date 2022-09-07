from typing import Any


def load_ipython_extension(ip: Any) -> None:  # pragma: no cover
    # prevent circular import
    from ngoto.core.util.rich.pretty import install
    from ngoto.core.util.rich.traceback import install as tr_install

    install()
    tr_install()
