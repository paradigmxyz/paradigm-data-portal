from __future__ import annotations

import sys

import toolcli
import toolstr

import pdp


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': ls_command,
        'help': 'list datasets or dataset files',
        'args': [
            {
                'name': 'dataset',
                'help': 'dataset to list info of, omit for global manifest',
                'nargs': '?',
            },
            {
                'name': '--hashes',
                'help': 'show md5 hashes of each file',
                'action': 'store_true',
            },
            {
                'name': '--urls',
                'help': 'show full urls of each file',
                'action': 'store_true',
            },
            {'name': '--portal-root', 'help': 'root url of data portal'},
        ],
        'examples': {
            '': 'show all datasets',
            'ethereum_contracts': 'show files of dataset',
            'ethereum_contracts --hashes': 'show files of dataset with hashes',
            'ethereum_contracts --urls': 'show urls of files in dataset',
        },
    }


def ls_command(
    dataset: str | None,
    hashes: bool,
    urls: bool,
    portal_root: str | None,
) -> None:

    if dataset is None:

        toolstr.print(
            'fetching global manifest...', style=pdp.styles['comment'], end='\r'
        )
        global_manifest = pdp.get_global_manifest()
        sys.stdout.write("\033[K")
        toolstr.print('Datasets', style=pdp.styles['title'])
        for dataset_name, dataset_manifest in global_manifest[
            'datasets'
        ].items():
            toolstr.print_bullet(
                key=dataset_name,
                value=dataset_manifest['description'],
                styles=pdp.styles,
            )
        print()
        toolstr.print(
            '(use '
            + toolstr.add_style(
                'pdp dataset <DATASET>', pdp.styles['description']
            )
            + ' for info or '
            + toolstr.add_style('pdp ls <DATASET>', pdp.styles['description'])
            + ' for file list)',
            style=pdp.styles['comment'],
        )

    else:

        # get dataset manifest
        manifest = pdp.get_dataset_manifest(dataset=dataset)

        # get id of each file, either filename or url
        if urls:
            file_ids = pdp.get_dataset_file_urls(
                dataset=dataset,
                portal_root=portal_root,
                manifest=manifest,
            )
        else:
            file_ids = [file['name'] for file in manifest['files']]

        # print either with or without hashes
        if hashes:
            rows = [
                [file_id, file['hash']]
                for file_id, file in zip(file_ids, manifest['files'])
            ]
            toolstr.print_table(rows, compact=True)
        else:
            for file_id in file_ids:
                print(file_id)

