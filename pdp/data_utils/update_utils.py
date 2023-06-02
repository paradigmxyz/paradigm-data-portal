from __future__ import annotations

import typing


def update(
    dataset: str,
    *,
    method: typing.Literal['download', 'collect'] = 'download',
) -> None:
    raise NotImplementedError()

