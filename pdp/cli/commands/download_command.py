from __future__ import annotations

import os

import toolcli

import pdp


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': download_command,
        'help': 'download files for a dataset',
        'args': [
            {'name': 'dataset', 'help': 'dataset to list info of'},
            {'name': '--output-dir', 'help': 'output directory path'},
            {'name': '--portal-root', 'help': 'root url of data portal'},
        ],
        'examples': [
            'ethereum_contracts',
            'ethereum_contracts --output-dir /path/to/some/dir',
        ],
    }


def download_command(
    dataset: str,
    output_dir: str | None,
    portal_root: str | None,
) -> None:

    if output_dir is None:
        output_dir = os.path.abspath('.')

    pdp.download_dataset(
        dataset=dataset,
        output_dir=output_dir,
        portal_root=portal_root,
    )

