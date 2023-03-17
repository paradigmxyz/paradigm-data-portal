from __future__ import annotations

import types


def get_generator_module(datatype: str) -> types.ModuleType:
    """get module that generates datasets of a partiucular datatype"""
    if datatype == 'contracts':
        from . import generate_contracts_dataset

        return generate_contracts_dataset
    elif datatype == 'native_transfers':
        from . import generate_native_transfers_dataset

        return generate_native_transfers_dataset
    elif datatype == 'slots':
        from . import generate_slots_dataset

        return generate_slots_dataset
    else:
        raise Exception('unknown datatype: ' + str(datatype))

