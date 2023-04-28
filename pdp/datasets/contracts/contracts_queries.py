"""
TODO
- create block_number predicate pushdown
"""

from __future__ import annotations

import typing

import ctc

import pdp
from . import contracts_spec

if typing.TYPE_CHECKING:
    import polars as pl


def query_contract(
    contract_address: str | bytes, **kwargs: typing.Any
) -> contracts_spec.Contract | None:
    """return most recent deployment of contract"""

    # query data
    result = query_contracts(contract_address=contract_address, collect=True, **kwargs)

    # convert to dict
    if len(result) == 0:
        return None
    else:
        return result.to_dicts()[0]  # type: ignore


def query_contracts(
    *,
    # filters
    contract_address: str | bytes | None = None,
    contract_addresses: typing.Sequence[str | bytes] | None = None,
    deployer: str | bytes | None = None,
    factory: str | bytes | None = None,
    start_block: int | None = None,
    end_block: int | None = None,
    block_number: int | None = None,
    code: str | bytes | None = None,
    code_hash: str | bytes | None = None,
    init_code: str | bytes | None = None,
    init_code_hash: str | bytes | None = None,
    # outputs
    sort: bool | pdp.PolarsExpression = False,
    descending: bool = False,
    unique: bool = False,
    unique_keep: typing.Literal['last', 'first', 'any'] | None = 'last',
    columns: pdp.PolarsExpression | None = None,
    output_binary: bool = True,
    # inputs
    source_path: str | None = None,
    network: str | int | None = None,
    scan_kwargs: typing.Any = None,
    collect: bool = True,
    streaming: bool = True,
) -> pl.DataFrame:

    # convert to hashes
    if code is not None:
        code_hash = ctc.keccak(code)
    if init_code is not None:
        init_code_hash = ctc.keccak(init_code)

    # collect filters
    block_filters = {
        'start_block': start_block,
        'end_block': end_block,
        'block_number': block_number,
    }
    binary_filters = {
        'factory': factory,
        'deployer': deployer,
        'contract_address': contract_address,
        'code_hash': code_hash,
        'init_code_hash': init_code_hash,
    }
    filters = pdp.create_query_filters(
        binary_filters=binary_filters,
        block_filters=block_filters,
        binary_is_in_filters={'contract_address': contract_addresses},
    )

    # keep unique contracts
    if unique:
        unique_sort = ['block_number', 'create_index']
        unique_descending = False
        unique_columns = ['contract_address']
    else:
        unique_sort = None
        unique_descending = False
        unique_columns = None

    # create sort expression
    if sort and isinstance(sort, bool):
        sort = ['block_number', 'create_index']

    return pdp.query(
        datatype='contracts',
        filters=filters,
        sort=sort,
        descending=descending,
        columns=columns,
        output_binary=output_binary,
        source_path=source_path,
        network=network,
        unique_columns=unique_columns,
        unique_sort=unique_sort,
        unique_descending=unique_descending,
        unique_keep=unique_keep,
        scan_kwargs=scan_kwargs,
        collect=collect,
        streaming=streaming,
    )

