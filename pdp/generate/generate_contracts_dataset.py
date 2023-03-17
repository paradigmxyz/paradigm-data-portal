#!/usr/bin/env python3

from __future__ import annotations


from ctc.toolbox.batch_utils import extract_create_traces


output_dir = '/Users/stormslivkoff/repos/paradigm-data-portal/datasets/ethereum_contracts_raw'

extractor = extract_create_traces.ExtractCreateTraces(
    start_block=0,
    end_block=16_800_000,
    chunk_size=1000,
    output_dir=output_dir,
    tracker='file',
    output_filetype='csv',
    name='ethereum_contracts__v1_0_0',
    context={'network': 'ethereum'},
)

if __name__ == '__main__':
    extractor.orchestrate_jobs(executor='parallel')

