#!/usr/bin/env python3

from __future__ import annotations


from ctc.toolbox.batch_utils import extract_create_traces


output_dir = '/Users/stormslivkoff/data/pdp/raw_data/ethereum_contracts_1.1_raw'

extractor = extract_create_traces.ExtractCreateTraces(
    start_block=0,
    end_block=16_800_000,
    # start_block=16_000_000,
    # end_block=16_001_000,
    chunk_size=1000,
    output_dir=output_dir,
    tracker='file',
    output_filetype='csv',
    name='ethereum_contracts__v1_1_0',
    context={'network': 1},
)

if __name__ == '__main__':
    extractor.orchestrate_jobs(executor='parallel')

