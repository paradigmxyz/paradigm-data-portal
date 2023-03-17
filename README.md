
# Paradigm Data Portal

The Paradigm Data Portal is a collection of open source crypto datasets for researchers and tool builders

## Datasets
- [`ethereum_contracts`](https://github.com/paradigmxyz/paradigm-data-portal/tree/main/datasets/ethereum_contracts): all historical contract deployments
- [`ethereum_native_transfers`](https://github.com/paradigmxyz/paradigm-data-portal/tree/main/datasets/ethereum_native_transfers): all native transfers in similar format to ERC20 Transfers (excluding tx fees)
- [`ethereum_slots`](https://github.com/paradigmxyz/paradigm-data-portal/tree/main/datasets/ethereum_slots): all slots of each contract, including historical usage metadata

All datasets are released under a [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/) license into the public domain unless otherwise noted.

## `pdp`

`pdp` is a CLI tool that can be used to obtain and manage PDP datasets

To install: `pip install paradigm-data-portal`


#### Example Usage

- List available datasets `pdp ls`
- List dataset files `pdp ls <dataset_name>`
- Download a dataset `pdp download <dataset_name>`

Each command has multiple options, view help with `pdp <command> -h`


## Dataset Versioning

Every dataset has a version in `<major>.<minor>.<patch>` format, e.g. `1.2.8`
- when a schema is updated, the major version is increased
- when rows are added, removed, or modified, the minor version is increased
- when rows are added due to new blocks, the patch is increased

Updates will be documented in dataset changelogs

