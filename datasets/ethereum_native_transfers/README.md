
# Ethereum Native Transfers Dataset v1.0.0

This is a dataset of all native transfers in similar format to ERC20 Transfers (excluding tx fees)

The dataset was created by using [this script](https://github.com/paradigmxyz/paradigm-data-portal/blob/main/pdp/datasets/native_transfers/native_transfers_collect.py)

Data is distributed as [parquet](https://data.paradigm.xyz/about) files and released into the public domain under a [CC0 license](https://creativecommons.org/share-your-work/public-domain/cc0/)

## Usage

Some example uses of this dataset include:
- look up all inbound transfers to an address
- analyze transfer size distributions
- analyze transfer frequency distributions



## Schema

#### `native_transfers` table
each row corresponds to a trace that transfers native token
| column | type | description |
| - | - | - |
| block_number | INTEGER | block number where native token was transfered |
| transfer_index | INTEGER | increased by 1 for each native transfer in block |
| transaction_hash | BINARY | hash of transaction that contains transfer |
| to_address | BINARY | address that native token is transferred to |
| from_address | BINARY | address that native token is transferred from |
| value | BINARY | amount of native token transferred |

## Download

This dataset can be downloaded using either the `pdp` cli tool or the urls below

The total dataset size is **61.00GB**

### Use `pdp`

The command `pdp download ethereum_native_transfers` will download all files in this dataset

See `pdp download -h` for available options

### Use URLs

| | file | size |
| - | - | - |
| 1 | [ethereum_native_transfers__v1_0_0__00000000_to_00199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__00000000_to_00199999.parquet) | 5.43MB |
| 2 | [ethereum_native_transfers__v1_0_0__00200000_to_00399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__00200000_to_00399999.parquet) | 10.81MB |
| 3 | [ethereum_native_transfers__v1_0_0__00400000_to_00599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__00400000_to_00599999.parquet) | 12.15MB |
| 4 | [ethereum_native_transfers__v1_0_0__00600000_to_00799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__00600000_to_00799999.parquet) | 15.24MB |
| 5 | [ethereum_native_transfers__v1_0_0__00800000_to_00999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__00800000_to_00999999.parquet) | 23.57MB |
| 6 | [ethereum_native_transfers__v1_0_0__01000000_to_01199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__01000000_to_01199999.parquet) | 43.13MB |
| 7 | [ethereum_native_transfers__v1_0_0__01200000_to_01399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__01200000_to_01399999.parquet) | 52.66MB |
| 8 | [ethereum_native_transfers__v1_0_0__01400000_to_01599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__01400000_to_01599999.parquet) | 68.87MB |
| 9 | [ethereum_native_transfers__v1_0_0__01600000_to_01799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__01600000_to_01799999.parquet) | 71.94MB |
| 10 | [ethereum_native_transfers__v1_0_0__01800000_to_01999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__01800000_to_01999999.parquet) | 75.75MB |
| 11 | [ethereum_native_transfers__v1_0_0__02000000_to_02199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__02000000_to_02199999.parquet) | 78.88MB |
| 12 | [ethereum_native_transfers__v1_0_0__02200000_to_02399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__02200000_to_02399999.parquet) | 119.10MB |
| 13 | [ethereum_native_transfers__v1_0_0__02400000_to_02599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__02400000_to_02599999.parquet) | 66.45MB |
| 14 | [ethereum_native_transfers__v1_0_0__02600000_to_02799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__02600000_to_02799999.parquet) | 66.38MB |
| 15 | [ethereum_native_transfers__v1_0_0__02800000_to_02999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__02800000_to_02999999.parquet) | 65.67MB |
| 16 | [ethereum_native_transfers__v1_0_0__03000000_to_03199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__03000000_to_03199999.parquet) | 70.41MB |
| 17 | [ethereum_native_transfers__v1_0_0__03200000_to_03399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__03200000_to_03399999.parquet) | 106.03MB |
| 18 | [ethereum_native_transfers__v1_0_0__03400000_to_03599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__03400000_to_03599999.parquet) | 136.80MB |
| 19 | [ethereum_native_transfers__v1_0_0__03600000_to_03799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__03600000_to_03799999.parquet) | 233.24MB |
| 20 | [ethereum_native_transfers__v1_0_0__03800000_to_03999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__03800000_to_03999999.parquet) | 469.12MB |
| 21 | [ethereum_native_transfers__v1_0_0__04000000_to_04199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__04000000_to_04199999.parquet) | 592.62MB |
| 22 | [ethereum_native_transfers__v1_0_0__04200000_to_04399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__04200000_to_04399999.parquet) | 804.41MB |
| 23 | [ethereum_native_transfers__v1_0_0__04400000_to_04599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__04400000_to_04599999.parquet) | 516.11MB |
| 24 | [ethereum_native_transfers__v1_0_0__04600000_to_04799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__04600000_to_04799999.parquet) | 1.09GB |
| 25 | [ethereum_native_transfers__v1_0_0__04800000_to_04999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__04800000_to_04999999.parquet) | 1.71GB |
| 26 | [ethereum_native_transfers__v1_0_0__05000000_to_05199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__05000000_to_05199999.parquet) | 1020.42MB |
| 27 | [ethereum_native_transfers__v1_0_0__05200000_to_05399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__05200000_to_05399999.parquet) | 769.68MB |
| 28 | [ethereum_native_transfers__v1_0_0__05400000_to_05599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__05400000_to_05599999.parquet) | 878.05MB |
| 29 | [ethereum_native_transfers__v1_0_0__05600000_to_05799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__05600000_to_05799999.parquet) | 893.71MB |
| 30 | [ethereum_native_transfers__v1_0_0__05800000_to_05999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__05800000_to_05999999.parquet) | 705.26MB |
| 31 | [ethereum_native_transfers__v1_0_0__06000000_to_06199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__06000000_to_06199999.parquet) | 745.70MB |
| 32 | [ethereum_native_transfers__v1_0_0__06200000_to_06399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__06200000_to_06399999.parquet) | 643.32MB |
| 33 | [ethereum_native_transfers__v1_0_0__06400000_to_06599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__06400000_to_06599999.parquet) | 588.53MB |
| 34 | [ethereum_native_transfers__v1_0_0__06600000_to_06799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__06600000_to_06799999.parquet) | 607.73MB |
| 35 | [ethereum_native_transfers__v1_0_0__06800000_to_06999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__06800000_to_06999999.parquet) | 587.19MB |
| 36 | [ethereum_native_transfers__v1_0_0__07000000_to_07199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__07000000_to_07199999.parquet) | 598.46MB |
| 37 | [ethereum_native_transfers__v1_0_0__07200000_to_07399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__07200000_to_07399999.parquet) | 588.88MB |
| 38 | [ethereum_native_transfers__v1_0_0__07400000_to_07599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__07400000_to_07599999.parquet) | 629.00MB |
| 39 | [ethereum_native_transfers__v1_0_0__07600000_to_07799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__07600000_to_07799999.parquet) | 663.01MB |
| 40 | [ethereum_native_transfers__v1_0_0__07800000_to_07999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__07800000_to_07999999.parquet) | 729.28MB |
| 41 | [ethereum_native_transfers__v1_0_0__08000000_to_08199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__08000000_to_08199999.parquet) | 627.52MB |
| 42 | [ethereum_native_transfers__v1_0_0__08200000_to_08399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__08200000_to_08399999.parquet) | 560.94MB |
| 43 | [ethereum_native_transfers__v1_0_0__08400000_to_08599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__08400000_to_08599999.parquet) | 522.91MB |
| 44 | [ethereum_native_transfers__v1_0_0__08600000_to_08799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__08600000_to_08799999.parquet) | 475.54MB |
| 45 | [ethereum_native_transfers__v1_0_0__08800000_to_08999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__08800000_to_08999999.parquet) | 496.36MB |
| 46 | [ethereum_native_transfers__v1_0_0__09000000_to_09199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__09000000_to_09199999.parquet) | 509.63MB |
| 47 | [ethereum_native_transfers__v1_0_0__09200000_to_09399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__09200000_to_09399999.parquet) | 437.48MB |
| 48 | [ethereum_native_transfers__v1_0_0__09400000_to_09599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__09400000_to_09599999.parquet) | 531.73MB |
| 49 | [ethereum_native_transfers__v1_0_0__09600000_to_09799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__09600000_to_09799999.parquet) | 559.07MB |
| 50 | [ethereum_native_transfers__v1_0_0__09800000_to_09999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__09800000_to_09999999.parquet) | 669.82MB |
| 51 | [ethereum_native_transfers__v1_0_0__10000000_to_10199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__10000000_to_10199999.parquet) | 794.10MB |
| 52 | [ethereum_native_transfers__v1_0_0__10200000_to_10399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__10200000_to_10399999.parquet) | 856.74MB |
| 53 | [ethereum_native_transfers__v1_0_0__10400000_to_10599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__10400000_to_10599999.parquet) | 1.02GB |
| 54 | [ethereum_native_transfers__v1_0_0__10600000_to_10799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__10600000_to_10799999.parquet) | 1016.86MB |
| 55 | [ethereum_native_transfers__v1_0_0__10800000_to_10999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__10800000_to_10999999.parquet) | 901.55MB |
| 56 | [ethereum_native_transfers__v1_0_0__11000000_to_11199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__11000000_to_11199999.parquet) | 911.41MB |
| 57 | [ethereum_native_transfers__v1_0_0__11200000_to_11399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__11200000_to_11399999.parquet) | 950.09MB |
| 58 | [ethereum_native_transfers__v1_0_0__11400000_to_11599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__11400000_to_11599999.parquet) | 1020.27MB |
| 59 | [ethereum_native_transfers__v1_0_0__11600000_to_11799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__11600000_to_11799999.parquet) | 1.12GB |
| 60 | [ethereum_native_transfers__v1_0_0__11800000_to_11999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__11800000_to_11999999.parquet) | 1.20GB |
| 61 | [ethereum_native_transfers__v1_0_0__12000000_to_12199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__12000000_to_12199999.parquet) | 1.28GB |
| 62 | [ethereum_native_transfers__v1_0_0__12200000_to_12399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__12200000_to_12399999.parquet) | 1.50GB |
| 63 | [ethereum_native_transfers__v1_0_0__12400000_to_12599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__12400000_to_12599999.parquet) | 1.42GB |
| 64 | [ethereum_native_transfers__v1_0_0__12600000_to_12799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__12600000_to_12799999.parquet) | 1.18GB |
| 65 | [ethereum_native_transfers__v1_0_0__12800000_to_12999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__12800000_to_12999999.parquet) | 1.23GB |
| 66 | [ethereum_native_transfers__v1_0_0__13000000_to_13199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__13000000_to_13199999.parquet) | 1.24GB |
| 67 | [ethereum_native_transfers__v1_0_0__13200000_to_13399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__13200000_to_13399999.parquet) | 1.28GB |
| 68 | [ethereum_native_transfers__v1_0_0__13400000_to_13599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__13400000_to_13599999.parquet) | 1.43GB |
| 69 | [ethereum_native_transfers__v1_0_0__13600000_to_13799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__13600000_to_13799999.parquet) | 1.39GB |
| 70 | [ethereum_native_transfers__v1_0_0__13800000_to_13999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__13800000_to_13999999.parquet) | 1.33GB |
| 71 | [ethereum_native_transfers__v1_0_0__14000000_to_14199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__14000000_to_14199999.parquet) | 1.33GB |
| 72 | [ethereum_native_transfers__v1_0_0__14200000_to_14399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__14200000_to_14399999.parquet) | 1.29GB |
| 73 | [ethereum_native_transfers__v1_0_0__14400000_to_14599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__14400000_to_14599999.parquet) | 1.29GB |
| 74 | [ethereum_native_transfers__v1_0_0__14600000_to_14799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__14600000_to_14799999.parquet) | 1.30GB |
| 75 | [ethereum_native_transfers__v1_0_0__14800000_to_14999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__14800000_to_14999999.parquet) | 1.20GB |
| 76 | [ethereum_native_transfers__v1_0_0__15000000_to_15199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__15000000_to_15199999.parquet) | 1.23GB |
| 77 | [ethereum_native_transfers__v1_0_0__15200000_to_15399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__15200000_to_15399999.parquet) | 1.30GB |
| 78 | [ethereum_native_transfers__v1_0_0__15400000_to_15599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__15400000_to_15599999.parquet) | 1.20GB |
| 79 | [ethereum_native_transfers__v1_0_0__15600000_to_15799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__15600000_to_15799999.parquet) | 1.03GB |
| 80 | [ethereum_native_transfers__v1_0_0__15800000_to_15999999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__15800000_to_15999999.parquet) | 975.74MB |
| 81 | [ethereum_native_transfers__v1_0_0__16000000_to_16199999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__16000000_to_16199999.parquet) | 1009.98MB |
| 82 | [ethereum_native_transfers__v1_0_0__16200000_to_16399999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__16200000_to_16399999.parquet) | 958.26MB |
| 83 | [ethereum_native_transfers__v1_0_0__16400000_to_16599999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__16400000_to_16599999.parquet) | 972.90MB |
| 84 | [ethereum_native_transfers__v1_0_0__16600000_to_16799999.parquet](https://datasets.paradigm.xyz/datasets/ethereum_native_transfers/ethereum_native_transfers__v1_0_0__16600000_to_16799999.parquet) | 1.00GB |
