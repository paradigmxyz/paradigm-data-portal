import os
import tempfile

import pytest

from pdp.datasets import contracts
from pdp.datasets import slots
from pdp.datasets import native_transfers


dataset_collectors = [
    contracts.collect_contracts_dataset,
    slots.collect_slots_dataset,
    native_transfers.collect_native_transfers_dataset,
]


collect_kwargs_sets = [
    {
        'start_block': 14_000_000,
        'end_block': 14_000_100,
        'chunk_size': 20,
        'network': 'ethereum',
        'executor': 'parallel',
        'verbose': True,
    },
]


@pytest.mark.parametrize('dataset_collector', dataset_collectors)
@pytest.mark.parametrize('collect_kwargs', collect_kwargs_sets)
@pytest.mark.parametrize('output_filetype', ['parquet', 'csv'])
def test(dataset_collector, collect_kwargs, output_filetype):
    output_dir = tempfile.mkdtemp()

    dataset_collector(
        output_dir=output_dir,
        output_filetype=output_filetype,
        **collect_kwargs,
    )

    output_files = os.listdir(output_dir)
    assert (
        len(output_files)
        == (collect_kwargs['end_block'] - collect_kwargs['start_block'])
        / collect_kwargs['chunk_size']
    )

