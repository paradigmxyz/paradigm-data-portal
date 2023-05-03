from __future__ import annotations

import os
import typing

from . import data_utils
from . import spec


@typing.overload
def get_data_root(*, require: typing.Literal[True]) -> str:
    ...


@typing.overload
def get_data_root(*, require: bool) -> str | None:
    ...


@typing.overload
def get_data_root() -> str:
    ...


def get_data_root(*, require: bool = True) -> str | None:
    data_root = os.environ.get('PDP_DATA_ROOT')
    if (data_root is None or data_root == '') and require:
        raise Exception('PDP_DATA_ROOT not set')
    return data_root


def get_dataset_glob(
    dataset: str | None = None,
    table: str | None = None,
    *,
    network: str | int | None = None,
    datatype: str | None = None,
) -> str:
    dataset_path = get_dataset_local_path(
        dataset=dataset,
        network=network,
        datatype=datatype,
    )

    if table is None:
        filename = '*.parquet'
    else:
        filename = table + '_*.parquet'

    return os.path.join(dataset_path, filename)


def get_dataset_local_path(
    dataset: str | None = None,
    *,
    network: str | int | None = None,
    datatype: str | None = None,
) -> str:
    if dataset is None:
        if network is None or datatype is None:
            raise Exception(
                'must specify datatype and network to get dataset name'
            )
        dataset = data_utils.get_dataset_name(
            datatype=datatype, network=network
        )

    return os.path.join(get_data_root(), dataset)


def get_local_datasets(
    data_root: str | None = None,
) -> typing.Sequence[str]:
    if data_root is None:
        data_root = get_data_root(require=True)

    data_dirs = []
    for subdir in os.listdir(data_root):
        subpath = os.path.join(data_root, subdir)
        if os.path.isdir(subpath):
            manifest_path = os.path.join(
                subpath, spec.dataset_manifest_filename
            )
            if os.path.isfile(manifest_path):
                data_dirs.append(subdir)

    return data_dirs

