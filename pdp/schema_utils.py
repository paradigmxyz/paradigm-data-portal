from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import types
    import toolsql


def get_dataset_name(*, datatype: str, network: str) -> str:
    """create dataset name based on metadata"""
    return network + '_' + datatype


def parse_dataset_name(dataset: str) -> typing.Mapping[str, str]:
    """parse metadata from a dataset name"""
    network, datatype = dataset.split('_', maxsplit=1)
    return {
        'network': network,
        'datatype': datatype,
    }


def get_datatype_schema(datatype: str) -> toolsql.DBSchema:
    module = _get_datatype_module(datatype)
    schema: toolsql.DBSchema = module.schema
    return schema


def _get_datatype_module(datatype: str) -> types.ModuleType:
    import importlib

    try:
        return importlib.import_module('pdp.datasets.' + datatype)
    except Exception:
        raise Exception('could not get module for dataset' + str(datatype))

