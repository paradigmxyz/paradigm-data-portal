#!/usr/bin/env python3

from __future__ import annotations


from ctc.toolbox.batch_utils import extract_slots


output_dir = '/Users/stormslivkoff/repos/paradigm-data-portal/datasets/ethereum_slots_raw'

extractor = extract_slots.ExtractSlots(
    start_block=1000,
    end_block=16_800_000,
    chunk_size=1000,
    output_dir=output_dir,
    tracker='file',
    output_filetype='parquet',
    name='ethereum_slots__v1_0_0',
    context={'network': 1},
)

if __name__ == '__main__':
    extractor.orchestrate_jobs(executor='parallel')

