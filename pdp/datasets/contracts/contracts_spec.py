from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import toolsql


version = '1.1.0'

example_usage = [
    'look up all contracts deployed by an address',
    'look up all contracts that have a given bytecode',
    'analyze distribution of contract bytecode motifs',
]

schema: toolsql.DBSchemaShorthand = {
    'name': 'contracts',
    'description': 'all historical contract deployments',
    'tables': {
        'contracts': {
            'description': 'each row corresponds to a contract create trace',
            'columns': [
                {
                    'name': 'block_number',
                    'type': 'INTEGER',
                    'description': 'block number when contract was created',
                    'primary': True,
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
                    'index': True,
                },
                {
                    'name': 'contract_address',
                    'type': 'BINARY',
                    'description': 'address of deployed contract',
                    'primary': True,
                },
                {
                    'name': 'deployer',
                    'type': 'BINARY',
                    'description': 'EOA that deployed the contract',
                    'index': True,
                },
                {
                    'name': 'factory',
                    'type': 'BINARY',
                    'description': 'the `from` field in the creation trace',
                    'index': True,
                },
                {
                    'name': 'init_code',
                    'type': 'BINARY',
                    'description': 'initialization bytecode of contract',
                },
                {
                    'name': 'code',
                    'type': 'BINARY',
                    'description': 'bytecode of contract',
                },
                {
                    'name': 'init_code_hash',
                    'type': 'BINARY',
                    'description': 'keccak hash of contract initialization code',
                },
                {
                    'name': 'code_hash',
                    'type': 'BINARY',
                    'description': 'keccak hash of contract bytecode',
                    'index': True,
                },
            ],
        },
    },
}

