from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import toolsql


version = '1.1.0'

example_usage = [
    'look up all inbound transfers to an address',
    'analyze transfer size distributions',
    'analyze transfer frequency distributions',
]

schema: toolsql.DBSchemaShorthand = {
    'name': 'native_transfers',
    'description': 'all native transfers in similar format to ERC20 Transfers (excluding tx fees)',
    'tables': {
        'native_transfers': {
            'description': 'each row corresponds to a trace that transfers native token',
            'columns': [
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
            ],
        },
    },
}

