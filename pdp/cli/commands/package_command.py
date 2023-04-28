from __future__ import annotations

import os

import toolcli

import pdp


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': package_command,
        'help': 'package a dataset manifest or a global manifest',
        'args': [
            {
                'name': 'directory',
                'help': 'data directory to use for manifest',
                'nargs': '?',
            },
            {
                'name': '--global',
                'help': 'create a global manifest instead of a dataset manifest',
                'action': 'store_true',
                'dest': 'global_manifest',
            },
            {
                'name': '--output-path',
                'help': 'output path of manifest',
            },
            {
                'name': '--confirm',
                'help': 'confirm overwriting ',
                'action': 'store_true',
            },
            {
                'name': '--reuse-hashes',
                'help': '',
                'action': 'store_true',
            },
        ],
        'examples': [
            '',
            'path/to/some/dataset',
            '--global',
            '--confirm',
        ],
    }


def package_command(
    *,
    global_manifest: bool,
    directory: str | None,
    output_path: str | bool | None,
    confirm: bool,
    reuse_hashes: bool,
) -> None:

    if directory is None:
        directory = '.'
    directory = os.path.expanduser(directory)
    if output_path is None:
        output_path = True
    if isinstance(output_path, str):
        output_path = os.path.expanduser(output_path)

    if global_manifest:

        pdp.create_global_manifest(
            data_root=directory,
            version=pdp.global_version,
            output_path=output_path,
            confirm=confirm,
        )

    else:

        # check no subdatasets contained
        for item in os.listdir(directory):
            subpath = os.path.join(directory, item)
            if os.path.isdir(
                subpath
            ) and pdp.dataset_manifest_filename in os.listdir(subpath):
                raise Exception('use --global to package a global manifest')

        dataset_manifest = pdp.create_dataset_manifest(
            dataset_dir=directory,
            output_path=output_path,
            confirm=confirm,
            reuse_hashes=reuse_hashes,
        )

        # get readme path
        if isinstance(output_path, bool):
            readme_path: str | bool = True
        elif isinstance(output_path, str):
            readme_path = os.path.join(
                os.path.dirname(output_path),
                pdp.dataset_readme_filename,
            )
        else:
            raise Exception('unknown output_path type: ' + str(output_path))

        # create readme
        pdp.create_dataset_readme(
            dataset_manifest=dataset_manifest,
            output_path=readme_path,
            confirm=confirm,
        )

