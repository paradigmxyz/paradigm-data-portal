from __future__ import annotations

import typing

import toolcli

import pdp


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': update_command,
        'help': 'update a dataset or datasets to their latest versions',
        'hidden': True,
        'args': [
            {
                'name': 'datasets',
                'help': 'space-separated list of datasets to update',
                'nargs': '+',
            },
            {
                'name': ['-a', '--all'],
                'help': 'update all datasets',
                'dest': 'all_datasets',
                'action': 'store_true',
            },
            {
                'name': ['-m', '--method'],
                'help': 'method used for syncing ("download" or "collect")',
            },
        ],
        'examples': [
            'ethereum_contracts',
            'ethereum_contracts ethereum_slots',
            '--all',
        ],
    }


def update_command(
    datasets: typing.Sequence[str],
    all_datasets: bool,
    method: typing.Literal['download', 'collect'],
) -> None:
    if all_datasets:
        datasets = pdp.get_local_datasets()

    for dataset in datasets:
        pdp.update(dataset=dataset, method=method)

