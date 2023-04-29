from __future__ import annotations

import asyncio
import shutil
import typing

import pdp
from . import slots_spec

if typing.TYPE_CHECKING:
    import ctc.spec


def collect_slots_dataset(
    *,
    start_block: int,
    end_block: int,
    output_dir: str,
    network: ctc.spec.NetworkReference,
    chunk_size: int | None = None,
    output_filetype: str | None = None,
    executor: typing.Literal['serial', 'parallel'] = 'parallel',
) -> None:

    if chunk_size is None:
        chunk_size = 1000
    if output_filetype is None:
        output_filetype = 'parquet'

    dataset_name = pdp.get_versioned_dataset_name(
        datatype='slots',
        network=network,
        version=slots_spec.version,
    )

    extractor = _ExtractSlots(
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


class _ExtractSlots(pdp.BlockChunkJobs):
    def execute_job(self, i: int) -> typing.Any:
        job_data = self.get_job_data(i)
        job_name = self.get_job_name(i)
        path = self.tracker.get_job_output_path(i)
        _sync_extract_slots(
            start_block=job_data['start_block'],
            end_block=job_data['end_block'],
            job_name=job_name,
            path=path,
            context=self.context,
        )


def _sync_extract_slots(
    *,
    start_block: int,
    end_block: ctc.spec.BlockNumberReference,
    job_name: str,
    path: str,
    context: ctc.spec.Context,
) -> None:
    try:
        asyncio.run(
            _async_extract_slots(
                start_block=start_block,
                end_block=end_block,
                path=path,
                context=context,
            )
        )
    except Exception as e:
        print('job', job_name, 'failed:' + str(e))


async def _async_extract_slots(
    *,
    start_block: int,
    end_block: ctc.spec.BlockNumberReference,
    path: str,
    context: ctc.spec.Context,
) -> None:
    df = await ctc.async_trace_slot_stats(
        start_block=start_block,
        end_block=end_block,
        context=context,
    )

    await ctc.rpc.async_close_http_session()

    temp_path = path + '_temp'
    df.write_parquet(temp_path)
    shutil.move(temp_path, path)

