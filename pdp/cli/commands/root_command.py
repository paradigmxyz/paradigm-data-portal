from __future__ import annotations

import toolcli


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': root_command,
        'help': 'display help message',
        'hidden': True,
        'extra_data': ['parse_spec'],
    }


def root_command(parse_spec: toolcli.ParseSpec) -> None:
    toolcli.command_utils.execution.execute_other_command_sequence(
        ('help',),
        args={'parse_spec': parse_spec},
        parse_spec=parse_spec,
    )

