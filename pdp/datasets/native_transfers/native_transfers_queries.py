from __future__ import annotations

import typing

import pdp

if typing.TYPE_CHECKING:
    import polars as pl


def query_native_transfers(
    # filters
    from_address: str | bytes | None = None,
    to_address: str | bytes | None = None,
    from_addresses: typing.Sequence[str | bytes] | None = None,
    to_addresses: typing.Sequence[str | bytes] | None = None,
    start_block: int | None = None,
    end_block: int | None = None,
    block_number: int | None = None,
    # outputs
    sort: bool | pdp.PolarsExpression = True,
    descending: bool = False,
    unique_keep: typing.Literal['last', 'first', 'any'] = 'last',
    columns: pdp.PolarsExpression | None = None,
    output_binary: bool = True,
    # inputs
    source_path: str | None = None,
    network: str | int | None = None,
    scan_kwargs: typing.Any = None,
    collect: bool = True,
    streaming: bool = True,
) -> pl.DataFrame:

    # collect filters
    block_filters = {
        'start_block': start_block,
        'end_block': end_block,
        'block_number': block_number,
    }
    binary_filters = {
        'from_address': from_address,
        'to_address': to_address,
    }
    binary_is_in_filters = {
        'from_addresses': from_addresses,
        'to_addresses': to_addresses,
    }
    filters = pdp.create_query_filters(
        binary_filters=binary_filters,
        block_filters=block_filters,
        binary_is_in_filters=binary_is_in_filters,
    )

    if sort and isinstance(sort, bool):
        sort = ['block_number', 'transfer_index']

    return pdp.query(
        datatype='native_transfers',
        filters=filters,
        sort=sort,
        descending=descending,
        columns=columns,
        output_binary=output_binary,
        source_path=source_path,
        network=network,
        unique_keep=unique_keep,
        scan_kwargs=scan_kwargs,
        collect=collect,
        streaming=streaming,
    )

