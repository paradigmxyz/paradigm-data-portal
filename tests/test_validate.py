import os

import pytest

import pdp


data_root = pdp.get_data_root(require=False)
ethereum_contracts_present = (
    data_root is not None
    and os.path.isdir(data_root)
    and 'ethereum_contracts' in os.listdir(data_root)
)


@pytest.mark.skipif(
    not ethereum_contracts_present,
    reason='ethereum_contracts dataset not present',
)
def test_validate_dataset():
    path = pdp.get_dataset_local_path('ethereum_contracts')
    pdp.validate_dataset_directory(path)

