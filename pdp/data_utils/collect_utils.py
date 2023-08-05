from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import types


def ensure_ctc() -> types.ModuleType:
    try:
        import ctc

        return ctc
    except ImportError:
        raise Exception('`pip install checkthechain` to use this functionality')

