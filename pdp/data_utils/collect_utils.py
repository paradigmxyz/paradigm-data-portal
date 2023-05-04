from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import types


def ensure_ctc() -> types.ModuleType:
    try:
        import ctc

        return ctc
    except ImportError:
        raise Exception('must install ctc to use this functionality')

