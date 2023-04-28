
# Ethereum Slots Dataset v1.0.0

This is a dataset of all slots of each contract, including historical usage metadata

The dataset was created by using [this script](https://github.com/paradigmxyz/paradigm-data-portal/blob/main/pdp/datasets/slots/slots_collect.py)

Data is distributed as [parquet](https://data.paradigm.xyz/about) files and released into the public domain under a [CC0 license](https://creativecommons.org/share-your-work/public-domain/cc0/)

## Usage

Some example uses of this dataset include:
- look up how much storage space is used by a given contract
- look up which slots are used by a given contract
- look up which slots change most frequently for a given contract



## Schema

#### `slots` table
each row corresponds to a slot of a contract
| column | type | description |
| - | - | - |
| contract_address | BINARY | contract of slot |
| slot | BINARY | address of slot |
| value | BINARY | last data stored in slot |
| first_updated_block | INTEGER | first block where slot was used |
| last_updated_block | INTEGER | last block where slot was updated |
| n_tx_updates | INTEGER | number of transactions that updated slot |

## Download

This dataset can be downloaded using either the `pdp` cli tool or the urls below

The total dataset size is **38.38GB**

### Use `pdp`

The command `pdp download ethereum_slots` will download all files in this dataset

See `pdp download -h` for available options

### Use URLs

| | file | size |
| - | - | - |
| 1 | [ethereum_slots__v1.0.0__0x00_to_0x0f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x00_to_0x0f.parquet) | 3.80GB |
| 2 | [ethereum_slots__v1.0.0__0x10_to_0x1f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x10_to_0x1f.parquet) | 1.92GB |
| 3 | [ethereum_slots__v1.0.0__0x20_to_0x2f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x20_to_0x2f.parquet) | 2.23GB |
| 4 | [ethereum_slots__v1.0.0__0x30_to_0x3f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x30_to_0x3f.parquet) | 2.00GB |
| 5 | [ethereum_slots__v1.0.0__0x40_to_0x4f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x40_to_0x4f.parquet) | 2.15GB |
| 6 | [ethereum_slots__v1.0.0__0x50_to_0x5f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x50_to_0x5f.parquet) | 3.09GB |
| 7 | [ethereum_slots__v1.0.0__0x60_to_0x6f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x60_to_0x6f.parquet) | 1.86GB |
| 8 | [ethereum_slots__v1.0.0__0x70_to_0x7f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x70_to_0x7f.parquet) | 3.21GB |
| 9 | [ethereum_slots__v1.0.0__0x80_to_0x8f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x80_to_0x8f.parquet) | 2.51GB |
| 10 | [ethereum_slots__v1.0.0__0x90_to_0x9f.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0x90_to_0x9f.parquet) | 1.98GB |
| 11 | [ethereum_slots__v1.0.0__0xa0_to_0xaf.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0xa0_to_0xaf.parquet) | 2.72GB |
| 12 | [ethereum_slots__v1.0.0__0xb0_to_0xbf.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0xb0_to_0xbf.parquet) | 2.01GB |
| 13 | [ethereum_slots__v1.0.0__0xc0_to_0xcf.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0xc0_to_0xcf.parquet) | 2.12GB |
| 14 | [ethereum_slots__v1.0.0__0xd0_to_0xdf.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0xd0_to_0xdf.parquet) | 3.32GB |
| 15 | [ethereum_slots__v1.0.0__0xe0_to_0xef.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0xe0_to_0xef.parquet) | 1.50GB |
| 16 | [ethereum_slots__v1.0.0__0xf0_to_0xff.parquet](https://datasets.paradigm.xyz/datasets/ethereum_slots/ethereum_slots__v1.0.0__0xf0_to_0xff.parquet) | 1.97GB |
