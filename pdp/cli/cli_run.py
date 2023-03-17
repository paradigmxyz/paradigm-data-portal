from __future__ import annotations

import os

import toolcli

import pdp


def run_cli(raw_command: str | None = None) -> None:

    import tempfile

    help_cache_dir = os.path.join(tempfile.gettempdir(), 'ctc', 'help_cache')

    command_index: toolcli.CommandIndex = {
        ('',): 'pdp.cli.commands.root_command',
        ('dataset',): 'pdp.cli.commands.dataset_command',
        ('download',): 'pdp.cli.commands.download_command',
        ('generate',): 'pdp.cli.commands.generate_command',
        ('ls',): 'pdp.cli.commands.ls_command',
        ('package',): 'pdp.cli.commands.package_command',
        ('upload',): 'pdp.cli.commands.upload_command',
        ('validate',): 'pdp.cli.commands.validate_command',
        (
            'version',
        ): 'toolcli.command_utils.standard_subcommands.version_command',
        ('help',): 'toolcli.command_utils.standard_subcommands.help_command',
    }

    config: toolcli.CLIConfig = {
        'description': pdp.__doc__,
        'version': pdp.__version__,
        'base_command': 'pdp',
        'include_standard_subcommands': False,
        'default_command_sequence': ('help',),
        'include_debug_arg': True,
        'help_cache_dir': help_cache_dir,
        'style_theme': pdp.styles,
    }

    toolcli.run_cli(
        command_index=command_index,
        config=config,
    )

