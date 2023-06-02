from __future__ import annotations

import asyncio
import typing

import pdp
from . import contracts_spec

if typing.TYPE_CHECKING:
    import ctc.spec
    import tooljob.trackers.file_tracker


def collect_contracts_dataset(
    *,
    start_block: int,
    end_block: int,
    output_dir: str,
    network: ctc.spec.NetworkReference,
    chunk_size: int | None = None,
    output_filetype: str | None = None,
    executor: typing.Literal['serial', 'parallel'] = 'parallel',
    verbose: bool = False,
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
        styles=pdp.styles,
        verbose=verbose,
    )

    extractor.orchestrate_jobs(executor=executor)


class _ExtractContracts(pdp.BlockChunkJobs):
    tracker: tooljob.trackers.file_tracker.FileTracker

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
    import polars as pl

    pdp.ensure_ctc()
    import ctc
    import ctc.rpc
    from ctc.toolbox import pl_utils

    create_traces = await ctc.async_trace_contract_creations(
        start_block=start_block,
        end_block=end_block,
        context=context,
    )
    await ctc.rpc.async_close_http_session()

    df = pl.DataFrame(create_traces)
    pl_utils.write_df(df=df, path=path, create_dir=True)

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
        raise e

