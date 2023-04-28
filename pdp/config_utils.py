from __future__ import annotations

import os

from . import data_utils


def get_data_root() -> str:
    data_root = os.environ.get('PDP_DATA_ROOT')
    if data_root is None or data_root == '':
        raise Exception('PDP_DATA_ROOT not set, so must specify paths manually')
    return data_root


def get_dataset_path_template(
    dataset: str | None = None,
    table: str | None = None,
    *,
    network: str | int | None = None,
    datatype: str | None = None,
) -> str:

    if dataset is None:
        if network is None or datatype is None:
            raise Exception('must specify datatype and network to get dataset name')
        dataset = data_utils.get_dataset_name(
            datatype=datatype, network=network
        )

    if table is None:
        filename = '*.parquet'
    else:
        filename = table + '_*.parquet'

    return os.path.join(get_data_root(), dataset, filename)

