from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import toolsql

    class Slot(typing.TypedDict):
        contract_address: str
        slot: str
        value: bytes
        first_updated_block: int
        last_updated_block: int
        n_tx_updates: int


version = '1.1.0'

example_usage = [
    'look up how much storage space is used by a given contract',
    'look up which slots are used by a given contract',
    'look up which slots change most frequently for a given contract',
]

schema: toolsql.DBSchemaShorthand = {
    'name': 'slots',
    'description': 'all slots of each contract, including historical usage metadata',
    'tables': {
        'slots': {
            'description': 'each row corresponds to a slot of a contract',
            'columns': [
                {
                    'name': 'contract_address',
                    'type': 'BINARY',
                    'description': 'contract of slot',
                },
                {
                    'name': 'slot',
                    'type': 'BINARY',
                    'description': 'address of slot',
                },
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
            ],
        },
    },
}

