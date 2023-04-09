from __future__ import annotations

import os
import typing

from . import config_utils
from pdp import spec

if typing.TYPE_CHECKING:
    import polars as pl


def query(
    filters: spec.PolarsExpression,
    # outputs
    pre_filter_sort: spec.PolarsExpression | None = None,
    pre_filter_descending: bool = False,
    sort: spec.PolarsExpression | None = None,
    descending: bool = False,
    unique_columns: typing.Sequence[str] | None = None,
    unique_keep: typing.Literal['last', 'first', 'all'] = 'last',
    columns: spec.PolarsExpression | None = None,
    output_binary: bool = True,
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

    # determine data source
    if source_path is None:
        source_path = config_utils.get_dataset_path_template(
            network=network,
            datatype=datatype,
            dataset=dataset,
            table=table,
        )
    if os.path.isdir(source_path):
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

    # pre filter sort
    if pre_filter_sort is not None:
        lf = lf.sort(pre_filter_sort, descending=pre_filter_descending)

    # filter unique
    if unique_columns is not None:
        if unique_keep != 'all':
            if unique_keep in ['last', 'first']:
                lf = lf.unique(subset=unique_columns, keep=unique_keep)
            else:
                raise Exception('invalid value for keep')

    # post filter sort
    if sort is not None:
        done = sort == pre_filter_sort and descending == pre_filter_descending
        if not done:
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


def _create_filters(
    *,
    simple_filters: typing.Mapping[str, typing.Any] | None = None,
    block_filters: typing.Mapping[str, int | None] | None = None,
    binary_filters: typing.Mapping[str, str | bytes | None] | None = None,
    binary_is_in_filters: typing.Mapping[str, typing.Sequence[str | bytes] | None] | None = None,
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
                binary_values = [spec.to_binary(subvalue) for subvalue in list_value]
                filters.append(pl.col(key).is_in(binary_values))

    return filters

