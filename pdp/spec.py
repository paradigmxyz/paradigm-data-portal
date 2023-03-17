from __future__ import annotations

import typing


if typing.TYPE_CHECKING:

    import toolcli
    import toolsql

    class GlobalManifest(typing.TypedDict):
        """manifest of all datasets"""

        version: str
        datasets: typing.Mapping[str, DatasetManifestSlim]

    class DatasetManifest(typing.TypedDict):
        """manifest of a particular dataset"""

        name: str
        version: str
        description: str
        datatype: str
        network: str
        files: typing.Sequence[FileMetadata]
        schema: toolsql.DBSchemaShorthand

    class DatasetManifestSlim(typing.TypedDict):
        """manifest of a particular dataset"""

        name: str
        version: str
        description: str
        datatype: str
        network: str
        n_files: int
        n_bytes: int
        schema: toolsql.DBSchemaShorthand

    class FileMetadata(typing.TypedDict):
        """metadata of a dataset file"""

        name: str
        hash: str
        n_bytes: int


#
# # urls and paths
#

# default portal root
portal_root = 'https://datasets.paradigm.xyz/datasets'
bucket_root_path = 'datasets'

# schema for various portal urls
urls = {
    'global_manifest': '{portal_root}/global_manifest.json',
    'dataset_manifest': '{portal_root}/{network}_{datatype}/dataset_manifest.json',
    'dataset_file': '{portal_root}/{network}_{datatype}/{filename}',
    'old_global_manifests': '{portal_root}/old_global_manifests/v{version}.json',
    'old_dataset_manifest': '{portal_root}/old_dataset_manifests/{dataset}__v{version}.json',
}

global_manifest_filename = 'global_manifest.json'
dataset_manifest_filename = 'dataset_manifest.json'
dataset_readme_filename = 'README.md'
dataset_filename_template = '{dataset}__v{version}__{file_id}.{filetype}'
dataset_license_filenames = ['LICENSE-CC0']


#
# # datasets
#

global_version = '1.0.0'

dataset_versions = {
    'ethereum_contracts': '1.0.0',
    'ethereum_native_transfers': '1.0.0',
    'ethereum_slots': '1.0.0',
}

contracts_columns: toolsql.ColumnsShorthand = [
    {
        'name': 'block_number',
        'type': 'INTEGER',
        'description': 'block number when contract was created',
    },
    {
        'name': 'create_index',
        'type': 'INTEGER',
        'description': 'increased by 1 for each contract created in block',
    },
    {
        'name': 'transaction_hash',
        'type': 'BINARY',
        'description': 'hash of transaction that created contract',
    },
    {
        'name': 'contract_address',
        'type': 'BINARY',
        'description': 'address of deployed contract',
    },
    {
        'name': 'deployer',
        'type': 'BINARY',
        'description': 'EOA that deployed the contract',
    },
    {
        'name': 'factory',
        'type': 'BINARY',
        'description': 'the `from` field in the creation trace',
    },
    {
        'name': 'init_code',
        'type': 'BINARY',
        'description': 'initialization bytecode of contract',
    },
    {'name': 'code', 'type': 'BINARY', 'description': 'bytecode of contract'},
    {
        'name': 'init_code_hash',
        'type': 'BINARY',
        'description': 'keccak hash of contract initialization code',
    },
    {
        'name': 'code_hash',
        'type': 'BINARY',
        'description': 'keccak hash of contract bytecode',
    },
]
native_transfers_columns: toolsql.ColumnsShorthand = [
    {
        'name': 'block_number',
        'type': 'INTEGER',
        'description': 'block number where native token was transfered',
    },
    {
        'name': 'transfer_index',
        'type': 'INTEGER',
        'description': 'increased by 1 for each native transfer in block',
    },
    {
        'name': 'transaction_hash',
        'type': 'BINARY',
        'description': 'hash of transaction that contains transfer',
    },
    {
        'name': 'to_address',
        'type': 'BINARY',
        'description': 'address that native token is transferred to',
    },
    {
        'name': 'from_address',
        'type': 'BINARY',
        'description': 'address that native token is transferred from',
    },
    {
        'name': 'value',
        'type': 'BINARY',
        'description': 'amount of native token transferred',
    },
]
slots_columns: toolsql.ColumnsShorthand = [
    {
        'name': 'contract_address',
        'type': 'BINARY',
        'description': 'contract of slot',
    },
    {'name': 'slot', 'type': 'BINARY', 'description': 'address of slot'},
    {
        'name': 'value',
        'type': 'BINARY',
        'description': 'last data stored in slot',
    },
    {
        'name': 'first_updated_block',
        'type': 'INTEGER',
        'description': 'first block where slot was used',
    },
    {
        'name': 'last_updated_block',
        'type': 'INTEGER',
        'description': 'last block where slot was updated',
    },
    {
        'name': 'n_tx_updates',
        'type': 'INTEGER',
        'description': 'number of transactions that updated slot',
    },
]

datatype_schemas: typing.Mapping[str, toolsql.DBSchemaShorthand] = {
    'contracts': {
        'description': 'all historical contract deployments',
        'tables': {
            'contracts': {
                'description': 'each row corresponds to a contract create trace',
                'columns': contracts_columns,
            }
        }
    },
    'native_transfers': {
        'description': 'all native transfers in similar format to ERC20 Transfers (excluding tx fees)',
        'tables': {
            'native_transfers': {
                'description': 'each row corresponds to a trace that transfers native token',
                'columns': native_transfers_columns,
            }
        }
    },
    'slots': {
        'description': 'all slots of each contract, including historical usage metadata',
        'tables': {
            'slots': {
                'description': 'each row corresponds to a slot of a contract',
                'columns': slots_columns,
            }
        }
    },
}

datatype_example_usage = {
    'contracts': [
        'look up all contracts deployed by an address',
        'look up all contracts that have a given bytecode',
        'analyze distribution of contract bytecode motifs',
    ],
    'native_transfers': [
        'look up all inbound transfers to an address',
        'analyze transfer size distributions',
        'analyze transfer frequency distributions',
    ],
    'slots': [
        'look up how much storage space is used by a given contract',
        'look up which slots are used by a given contract',
        'look up which slots change most frequently for a given contract',
    ],
}


#
# # cli behavior
#

styles: toolcli.StyleTheme = {
    'title': 'bold #00e100',
    'metavar': '#e5e9f0',
    'description': '#aaaaaa',
    'content': '#00B400',
    'option': 'bold #e5e9f0',
    'comment': '#888888',
}

