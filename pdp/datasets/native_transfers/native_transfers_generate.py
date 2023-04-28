from __future__ import annotations

import asyncio
import shutil
import typing

import polars as pl

import pdp
from . import native_transfers_spec

if typing.TYPE_CHECKING:
    import ctc.spec


def generate_native_transfers_dataset(
    *,
    start_block: int,
    end_block: ctc.spec.BlockNumberReference,
    output_dir: str,
    network: ctc.spec.NetworkReference,
    chunk_size: int | None = None,
    output_filetype: str | None = None,
    executor: typing.Literal['serial', 'parallel'] = 'parallel',
) -> None:

    if chunk_size is None:
        chunk_size = 1000
    if output_filetype is None:
        output_filetype = 'csv'

    dataset_name = pdp.get_versioned_dataset_name(
        datatype='native_transfers',
        network=network,
        version=native_transfers_spec.version,
    )

    extractor = _ExtractNativeTransfers(
        start_block=start_block,
        end_block=end_block,
        chunk_size=chunk_size,
        output_dir=output_dir,
        tracker='file',
        output_filetype=output_filetype,
        name=dataset_name,
        context={'network': network},
    )

    extractor.orchestrate_jobs(executor=executor)


class _ExtractNativeTransfers(pdp.BlockChunkJobs):
    def execute_job(self, i: int) -> typing.Any:
        job_data = self.get_job_data(i)
        job_name = self.get_job_name(i)
        path = self.tracker.get_job_output_path(i)
        _sync_extract_native_transfers(
            start_block=job_data['start_block'],
            end_block=job_data['end_block'],
            job_name=job_name,
            path=path,
            context=self.context,
        )


def _sync_extract_native_transfers(
    *,
    start_block: int,
    end_block: ctc.spec.BlockNumberReference,
    job_name: str,
    path: str,
    context: ctc.spec.Context,
) -> None:
    try:
        asyncio.run(
            _async_extract_native_transfers(
                start_block=start_block,
                end_block=end_block,
                path=path,
                context=context,
            )
        )
    except Exception as e:
        print('job', job_name, 'failed:' + str(e))
        raise e


async def _async_extract_native_transfers(
    *,
    start_block: int,
    end_block: ctc.spec.BlockNumberReference,
    path: str,
    context: ctc.spec.Context,
) -> None:

    transfers = await ctc.async_trace_native_transfers(
        start_block=start_block,
        end_block=end_block,
        context=context,
    )

    await ctc.rpc.async_close_http_session(context=context)

    # load data into output file
    df = pl.DataFrame(
        transfers,
        orient='row',
        schema=[
            ('block_number', pl.datatypes.Int32),
            ('transfer_index', pl.datatypes.Int32),
            ('transaction_hash', pl.datatypes.Utf8),
            ('from_address', pl.datatypes.Utf8),
            ('to_address', pl.datatypes.Utf8),
            ('value', pl.datatypes.Utf8),
        ],
    )
    temp_path = path + '_temp'
    df.write_csv(temp_path)
    shutil.move(temp_path, path)

