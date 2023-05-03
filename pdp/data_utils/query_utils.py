from __future__ import annotations

import os
import typing

from .. import config_utils
from .. import spec

if typing.TYPE_CHECKING:
    import polars as pl


def query(
    filters: spec.PolarsExpression,
    # outputs
    columns: spec.PolarsExpression | None = None,
    group_by: spec.PolarsExpression | None = None,
    output_binary: bool = True,
    sort: spec.PolarsExpression | None = None,
    descending: bool = False,
    unique_sort: spec.PolarsExpression | None = None,
    unique_descending: bool = False,
    unique_columns: typing.Sequence[str] | None = None,
    unique_keep: typing.Literal['last', 'first', 'any'] | None = None,
    # inputs
    source_path: str | None = None,
    dataset: str | None = None,
    network: str | int | None = None,
    datatype: str | None = None,
    table: str | None = None,
    scan_kwargs: typing.Any = None,
    # outputs
    collect: bool = True,
    streaming: bool = True,
    output_path: str | None = None,
    output_kwargs: typing.Any = None,
) -> pl.DataFrame:
    import polars as pl

    # determine data source
    if source_path is None:
        if network is None:
            raise Exception('must specify network (e.g. network=\'ethereum\')')
        source_path = config_utils.get_dataset_glob(
            network=network,
            datatype=datatype,
            dataset=dataset,
            table=table,
        )
    elif os.path.isdir(source_path):
        source_path = os.path.join(source_path, '*.parquet')

    # initiate scan
    if scan_kwargs is None:
        scan_kwargs = {}
    lf = pl.scan_parquet(source_path, **scan_kwargs)

    # add filters
    if filters is not None:
        if isinstance(filters, (list, tuple)):
            filters_list = filters
        else:
            filters_list = [filters]

        if len(filters_list) > 0:
            filter = filters_list[0]
            for other_filter in filters_list[1:]:
                filter &= other_filter
            lf = lf.filter(filter)

    # filter unique
    if unique_columns is not None:
        if unique_keep is None:
            raise Exception(
                "must specify unique_keep (e.g. 'first', 'last', or 'any')"
            )

        # maintain order if unique_sort equals output sort
        if unique_sort is not None:
            lf = lf.sort(unique_sort, descending=unique_descending)
            already_sorted: bool = _polars_exprs_equal(sort, unique_sort) and (
                descending == unique_descending
            )
        else:
            already_sorted = False

        # keep unique
        lf = lf.unique(
            maintain_order=already_sorted,
            subset=unique_columns,
            keep=unique_keep,
        )
    else:
        already_sorted = False

    # group by
    if group_by is not None:
        # group and aggregate
        if columns is not None:
            raise Exception('must specify columns for agg when using groupby')
        lf = lf.groupby(group_by).agg(columns)

        # sort
        if sort:
            lf = lf.sort(sort, descending=descending)

    else:
        # sort
        if sort and not already_sorted:
            lf = lf.sort(sort, descending=descending)

        # select columns
        if columns is not None:
            lf = lf.select(columns)

    # encode binary as hex
    if not output_binary:
        encode_columns = [
            ('0x' + pl.col(column_name).bin.encode('hex')).alias(column_name)
            for column_name, column_type in lf.schema.items()
            if column_type == pl.Binary
        ]
        lf = lf.with_columns(encode_columns)

    # return output
    if output_kwargs is None:
        output_kwargs = {}
    if output_path:
        return lf.sink_parquet(output_path, **output_kwargs)
    elif collect and streaming:
        return lf.collect(streaming=True, **output_kwargs)
    elif collect:
        return lf.collect()
    else:
        return lf  # type: ignore


def create_query_filters(
    *,
    simple_filters: typing.Mapping[str, typing.Any] | None = None,
    block_filters: typing.Mapping[str, int | None] | None = None,
    binary_filters: typing.Mapping[str, str | bytes | None] | None = None,
    binary_is_in_filters: typing.Mapping[
        str, typing.Sequence[str | bytes] | None
    ]
    | None = None,
) -> typing.MutableSequence[pl.type_aliases.IntoExpr]:
    import polars as pl

    filters: typing.MutableSequence[pl.type_aliases.IntoExpr] = []

    # block filters
    if block_filters is not None:
        start_block = block_filters.get('start_block')
        end_block = block_filters.get('end_block')
        block_number = block_filters.get('block_number')
        if start_block is not None:
            filters.append(pl.col('block_number') >= start_block)
        if end_block is not None:
            filters.append(pl.col('block_number') <= end_block)
        if block_number is not None:
            filters.append(pl.col('block_number') == block_number)

    # binary filters
    if binary_filters is not None:
        for column, value in binary_filters.items():
            if value is not None:
                filters.append(pl.col(column) == spec.to_binary(value))

    # binary is_in filters
    if binary_is_in_filters is not None:
        for key, list_value in binary_is_in_filters.items():
            if list_value is not None:
                binary_values = [
                    spec.to_binary(subvalue) for subvalue in list_value
                ]
                filters.append(pl.col(key).is_in(binary_values))

    return filters


def _polars_exprs_equal(
    expr1: spec.PolarsExpression,
    expr2: spec.PolarsExpression,
) -> bool:
    if isinstance(expr1, str):
        expr1 = pl.col(expr1)
    if isinstance(expr2, str):
        expr1 = pl.col(expr2)
    return str(expr1) == str(expr2)

