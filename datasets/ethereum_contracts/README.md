
# Ethereum Contracts Dataset v1.0.0

This is a dataset of all historical contract deployments

The dataset was created by using [this script](https://github.com/paradigmxyz/paradigm-data-portal/blob/main/pdp/datasets/contracts/contracts_collect.py)

Data is distributed as [parquet](https://data.paradigm.xyz/about) files and released into the public domain under a [CC0 license](https://creativecommons.org/share-your-work/public-domain/cc0/)

## Usage

Some example uses of this dataset include:
- look up all contracts deployed by an address
- look up all contracts that have a given bytecode
- analyze distribution of contract bytecode motifs

An example notebook exploring this dataset can be found [here](https://github.com/paradigmxyz/paradigm-data-portal/blob/main/notebooks/explore_ethereum_contracts.ipynb)

## Schema

#### `contracts` table
each row corresponds to a contract create trace
| column | type | description |
| - | - | - |
| block_number | INTEGER | block number when contract was created |
| create_index | INTEGER | increased by 1 for each contract created in block |
| transaction_hash | BINARY | hash of transaction that created contract |
| contract_address | BINARY | address of deployed contract |
| deployer | BINARY | EOA that deployed the contract |
| factory | BINARY | the `from` field in the creation trace |
| init_code | BINARY | initialization bytecode of contract |
| code | BINARY | bytecode of contract |
| init_code_hash | BINARY | keccak hash of contract initialization code |
| code_hash | BINARY | keccak hash of contract bytecode |

## Download

This dataset can be downloaded using either the `pdp` cli tool or the urls below

The total dataset size is **6.57GB**

### Use `pdp`

The command `pdp download ethereum_contracts` will download all files in this dataset

See `pdp download -h` for available options

### Use URLs

| | file | size |
| - | - | - |
| 1 | [ethereum_contracts__v1_0_0__00000000_to_00999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__00000000_to_00999999.parquet) | 2.96MB |
| 2 | [ethereum_contracts__v1_0_0__01000000_to_01999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__01000000_to_01999999.parquet) | 13.08MB |
| 3 | [ethereum_contracts__v1_0_0__02000000_to_02999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__02000000_to_02999999.parquet) | 24.86MB |
| 4 | [ethereum_contracts__v1_0_0__03000000_to_03999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__03000000_to_03999999.parquet) | 83.30MB |
| 5 | [ethereum_contracts__v1_0_0__04000000_to_04999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__04000000_to_04999999.parquet) | 295.85MB |
| 6 | [ethereum_contracts__v1_0_0__05000000_to_05999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__05000000_to_05999999.parquet) | 313.06MB |
| 7 | [ethereum_contracts__v1_0_0__06000000_to_06999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__06000000_to_06999999.parquet) | 384.52MB |
| 8 | [ethereum_contracts__v1_0_0__07000000_to_07999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__07000000_to_07999999.parquet) | 338.28MB |
| 9 | [ethereum_contracts__v1_0_0__08000000_to_08999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__08000000_to_08999999.parquet) | 318.73MB |
| 10 | [ethereum_contracts__v1_0_0__09000000_to_09999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__09000000_to_09999999.parquet) | 401.13MB |
| 11 | [ethereum_contracts__v1_0_0__10000000_to_10999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__10000000_to_10999999.parquet) | 484.85MB |
| 12 | [ethereum_contracts__v1_0_0__11000000_to_11999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__11000000_to_11999999.parquet) | 529.76MB |
| 13 | [ethereum_contracts__v1_0_0__12000000_to_12999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__12000000_to_12999999.parquet) | 618.64MB |
| 14 | [ethereum_contracts__v1_0_0__13000000_to_13999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__13000000_to_13999999.parquet) | 567.07MB |
| 15 | [ethereum_contracts__v1_0_0__14000000_to_14999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__14000000_to_14999999.parquet) | 761.28MB |
| 16 | [ethereum_contracts__v1_0_0__15000000_to_15999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__15000000_to_15999999.parquet) | 909.94MB |
| 17 | [ethereum_contracts__v1_0_0__16000000_to_16799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_contracts/ethereum_contracts__v1_0_0__16000000_to_16799999.parquet) | 677.91MB |
