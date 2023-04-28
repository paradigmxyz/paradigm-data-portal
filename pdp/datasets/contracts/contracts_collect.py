from __future__ import annotations

import asyncio
import os
import shutil
import typing

import pdp
from . import contracts_spec

if typing.TYPE_CHECKING:
    import ctc.spec


def collect_contracts_dataset(
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
        datatype='contracts',
        network=network,
        version=contracts_spec.version,
    )

    extractor = _ExtractContracts(
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


class _ExtractContracts(pdp.BlockChunkJobs):
    def execute_job(self, i: int) -> typing.Any:
        job_data = self.get_job_data(i)
        job_name = self.get_job_name(i)
        path = self.tracker.get_job_output_path(i)
        _sync_trace_blocks(
            start_block=job_data['start_block'],
            end_block=job_data['end_block'],
            job_name=job_name,
            path=path,
            context=self.context,
        )


async def _async_trace_blocks(
    *,
    start_block: int,
    end_block: ctc.spec.BlockNumberReference,
    path: str,
    context: ctc.spec.Context,
) -> None:
    import ctc.rpc
    import polars as pl

    create_traces = await ctc.async_trace_contract_creations(
        start_block=start_block,
        end_block=end_block,
        context=context,
    )
    await ctc.rpc.async_close_http_session()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    temp_path = path + '_temp'
    pl.DataFrame(create_traces).write_csv(temp_path)
    shutil.move(temp_path, path)

    return None


def _sync_trace_blocks(
    *,
    start_block: int,
    end_block: ctc.spec.BlockNumberReference,
    job_name: str,
    path: str,
    context: ctc.spec.Context,
) -> None:
    try:
        asyncio.run(
            _async_trace_blocks(
                start_block=start_block,
                end_block=end_block,
                path=path,
                context=context,
            )
        )
    except Exception as e:
        print('job', job_name, 'failed:' + str(e))

