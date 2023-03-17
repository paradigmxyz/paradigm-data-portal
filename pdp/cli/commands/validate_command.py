from __future__ import annotations

import os

import toolcli

import pdp


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': validate_command,
        'help': 'validate files in dataset manifest',
        'args': [
            {
                'name': 'dataset_directory',
                'help': 'dataset directory, default is current directory',
                'nargs': '?',
            },
            {'name': '--no-hashes', 'help': 'skip hashing each file', 'action': 'store_true'},
        ],
        'examples': {
            '': 'validate dataset in current directory',
            '/path/to/some/dir': 'validate dataset in some other directory',
        },
    }


def validate_command(dataset_directory: str | None, no_hashes: bool) -> None:
    if dataset_directory is None:
        path = '.'
    else:
        path = dataset_directory
    path = os.path.abspath(os.path.expanduser(path))

    pdp.validate_dataset_directory(path, no_hashes=no_hashes)

