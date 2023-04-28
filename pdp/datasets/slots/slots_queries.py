from __future__ import annotations

import typing

import pdp
from . import slots_spec

if typing.TYPE_CHECKING:
    import polars as pl


def query_slots_of_contract(
    contract_address: str | bytes,
    network: str | int | None = None,
    **query_kwargs: typing.Any
) -> pl.DataFrame:
    return query_slots(
        contract_address=contract_address,
        network=network,
        **query_kwargs,
    )


def query_contract_slot_counts(
    network: str | int | None = None,
    **query_kwargs: typing.Any,
) -> pl.DataFrame:
    lf: pl.LazyFrame = (
        query_slots(collect=False, **query_kwargs)  # type: ignore
        .groupby('contract_address')
        .agg(pl.count())
        .sort('counts', descending=True)
    )

    return lf.collect(streaming=True)


def query_slot(
    contract_address: str | bytes,
    slot: str | bytes,
    network: str | int | None = None,
) -> slots_spec.Slot | None:
    result = query_slots(
        contract_address=contract_address,
        slot=slot,
    )
    if len(result) == 1:
        return result.to_dicts()[0]  # type: ignore
    else:
        return None


def query_slots(
    # filters
    contract_address: str | bytes | None = None,
    contract_addresses: typing.Sequence[str | bytes] | None = None,
    slot: str | bytes | None = None,
    slots: typing.Sequence[str | bytes] | None = None,
    # outputs
    sort: bool | pdp.PolarsExpression = True,
    unique_keep: typing.Literal['last', 'first', 'all'] = 'last',
    columns: pdp.PolarsExpression | None = None,
    output_binary: bool = True,
    # inputs
    source_path: str | None = None,
    network: str | int | None = None,
    scan_kwargs: typing.Any = None,
    collect: bool = True,
    streaming: bool = True,
) -> pl.DataFrame:

    # filters
    binary_filters = {
        'contract_address': contract_address,
        'slot': slot,
    }
    binary_is_in_filters = {
        'contract_addresses': contract_addresses,
        'slots': slots,
    }
    filters = pdp.create_query_filters(
        binary_filters=binary_filters,
        binary_is_in_filters=binary_is_in_filters,
    )

    return pdp.query(
        filters=filters,
        sort=sort,
        columns=columns,
        output_binary=output_binary,
        source_path=source_path,
        network=network,
        datatype='slots',
        scan_kwargs=scan_kwargs,
        collect=collect,
        streaming=streaming,
    )

