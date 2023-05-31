from __future__ import annotations

import typing


def update_dataset(
    dataset_name: str,
    *,
    method: typing.Literal['download', 'collect'] = 'download',
) -> None:
    raise NotImplementedError()

