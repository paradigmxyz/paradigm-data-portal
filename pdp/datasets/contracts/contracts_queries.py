"""
TODO
- create block_number predicate pushdown
"""

from __future__ import annotations

import typing

import ctc
from pdp import query_utils
from pdp import spec
from . import contracts_spec

if typing.TYPE_CHECKING:
    import polars as pl


def get_contract(
    contract_address: str | bytes, **kwargs: typing.Any
) -> contracts_spec.Contract | None:
    """return most recent deployment of contract"""

    # query data
    result = get_contracts(contract_address=contract_address, collect=True, **kwargs)

    # convert to dict
    if len(result) == 0:
        return None
    else:
        return result.to_dicts()[0]  # type: ignore


def get_contracts(
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
    sort: bool | spec.PolarsExpression = True,
    unique_keep: typing.Literal['last', 'first', 'all'] = 'last',
    columns: spec.PolarsExpression | None = None,
    output_binary: bool = True,
    # inputs
    path: str | None = None,
    network: str | None = None,
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
    filters = query_utils._create_filters(
        binary_filters=binary_filters,
        block_filters=block_filters,
        binary_is_in_filters={'contract_address': contract_addresses},
    )

    # create sort expression
    if (sort or (unique_keep != 'all')) and isinstance(sort, bool):
        sort = ['block_number', 'create_index']

    return query_utils.query(
        filters=filters,
        sort=sort,
        columns=columns,
        output_binary=output_binary,
        path=path,
        network=network,
        unique_columns=['contract_address'],
        unique_keep=unique_keep,
        datatype='contracts',
        scan_kwargs=scan_kwargs,
        collect=collect,
        streaming=streaming,
    )

