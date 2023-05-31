from __future__ import annotations

import os
import typing

import toolcli

import pdp


def cd_dir_help() -> typing.Mapping[str, str]:
    dir_dict = {
        '\[data_root]': 'directory where pdp datasets are stored',
    }
    local_datasets = pdp.get_local_datasets()
    for dataset in local_datasets:
        manifest = pdp.get_dataset_manifest(dataset, source='local')
        dir_dict[dataset] = manifest['description']
    return dir_dict


def cd_dir_getter(dirname: str) -> str:
    data_root = pdp.get_data_root(require=False)
    if data_root is None:
        raise toolcli.CDException('must set PDP_DATA_ROOT env var')

    if dirname in ['', 'data_root']:
        return data_root
    else:
        dirpath = os.path.join(data_root, dirname)
        if not os.path.isdir(dirpath):
            raise Exception('not a directory: ' + str(dirname))
        if not os.path.isfile(
            os.path.join(dirpath, pdp.dataset_manifest_filename)
        ):
            import toolstr

            toolstr.print(
                'no manifest file '
                + pdp.dataset_manifest_filename
                + ' detected for dataset',
                style='red',
            )

        return dirpath


def run_cli(raw_command: str | None = None) -> None:
    import tempfile

    help_cache_dir = os.path.join(tempfile.gettempdir(), 'pdp', 'help_cache')

    command_index: toolcli.CommandIndex = {
        ('',): 'pdp.cli.commands.root_command',
        ('collect',): 'pdp.cli.commands.collect_command',
        ('dataset',): 'pdp.cli.commands.dataset_command',
        ('download',): 'pdp.cli.commands.download_command',
        ('help',): 'toolcli.command_utils.standard_subcommands.help_command',
        ('ls',): 'pdp.cli.commands.ls_command',
        ('package',): 'pdp.cli.commands.package_command',
        ('update',): 'pdp.cli.commands.update_command',
        ('upload',): 'pdp.cli.commands.upload_command',
        ('validate',): 'pdp.cli.commands.validate_command',
        (
            'version',
        ): 'toolcli.command_utils.standard_subcommands.version_command',
    }

    config: toolcli.CLIConfig = {
        'base_command': 'pdp',
        'description': pdp.__doc__,
        'version': pdp.__version__,
        'include_standard_subcommands': [('cd',)],
        'default_command_sequence': ('help',),
        'include_debug_arg': True,
        'help_cache_dir': help_cache_dir,
        'style_theme': pdp.styles,
        'cd_dir_help': cd_dir_help,
        'cd_dir_getter': cd_dir_getter,
    }

    toolcli.run_cli(
        command_index=command_index,
        config=config,
    )

