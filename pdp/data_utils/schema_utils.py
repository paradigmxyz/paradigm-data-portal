from __future__ import annotations

import typing

from .. import spec

if typing.TYPE_CHECKING:
    import types
    import toolsql


def get_dataset_name(*, datatype: str, network: str | int) -> str:
    """create dataset name based on metadata"""
    if isinstance(network, int):
        network = spec.networks[network]
    return network + '_' + datatype


def get_versioned_dataset_name(*, datatype: str, network: str | int, version: str) -> str:
    """create versioned dataset name for use in file names"""
    dataset_name = get_dataset_name(datatype=datatype, network=network)
    version_str = 'v' + version.replace('.', '_')
    return dataset_name + '__' + version_str


def parse_dataset_name(dataset: str) -> typing.Mapping[str, str]:
    """parse metadata from a dataset name"""
    network, datatype = dataset.split('_', maxsplit=1)
    return {
        'network': network,
        'datatype': datatype,
    }


def get_datatype_schema(datatype: str) -> toolsql.DBSchema:
    import toolsql

    module = _get_datatype_module(datatype)
    schema: toolsql.DBSchema = toolsql.normalize_shorthand_db_schema(
        module.schema
    )
    return schema


def get_dataset_schema(
    dataset: str, multichain_tables: bool = False
) -> toolsql.DBSchema:
    import copy
    import toolsql

    # parse dataset name
    parsed = parse_dataset_name(dataset)
    network = parsed['network']

    # load schema
    datatype_schema = get_datatype_schema(parsed['datatype'])
    datatype_schema = copy.deepcopy(datatype_schema)
    datatype_schema['name'] = dataset

    # make schema names dataset-specific
    if multichain_tables:
        # if a multichain table, add chain_id to each table
        for table_schema in datatype_schema['tables'].values():

            # make chain_id primary only if there exist other primary keys
            is_primary = any(
                other_column.get('primary')
                for other_column in table_schema['columns']
            )
            raw_column: toolsql.ColumnSchemaShorthand = {
                'name': 'chain_id',
                'type': 'INTEGER',
                'index': True,
                'primary': is_primary,
            }
            column = toolsql.normalize_shorthand_column_schema(raw_column)
            table_schema['columns'].append(column)  # type: ignore

    else:
        # if a single chain table, add network to table names
        datatype_schema['tables'] = {
            network + '_' + k: v for k, v in datatype_schema['tables'].items()
        }

    return datatype_schema


def _get_datatype_module(datatype: str) -> types.ModuleType:
    import importlib

    try:
        return importlib.import_module('pdp.datasets.' + datatype)
    except Exception:
        raise Exception('could not get module for dataset' + str(datatype))

