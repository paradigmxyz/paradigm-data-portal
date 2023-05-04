from __future__ import annotations

import toolcli
import toolstr

import pdp


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': dataset_command,
        'help': 'show info about a dataset',
        'args': [
            {'name': 'dataset', 'help': 'name of dataset'},
        ],
        'examples': [
            'ethereum_contracts',
            'ethereum_native_transfers',
        ],
    }


def dataset_command(dataset: str) -> None:
    manifest = pdp.get_dataset_manifest(dataset)
    toolstr.print_text_box(
        toolstr.add_style(manifest['name'] + ' dataset', pdp.styles['metavar']),
        style=pdp.styles['title'],
    )
    toolstr.print_bullet(
        key='description',
        value=manifest['description'],
        styles=pdp.styles,
    )
    toolstr.print_bullet(
        key='version',
        value=manifest['version'],
        styles=pdp.styles,
    )
    toolstr.print_bullet(
        key='n_files',
        value=len(manifest['files']),
        styles=pdp.styles,
    )
    total_size = sum(file['n_bytes'] for file in manifest['files'])
    toolstr.print_bullet(
        key='total_size',
        value=toolstr.format_nbytes(total_size, decimals=1),
        styles=pdp.styles,
    )

    print()
    for table_name, table in manifest['schema']['tables'].items():
        if len(manifest['schema']['tables']) > 1:
            toolstr.print(
                table_name + ' table', style=pdp.styles['content'], indent=4
            )
        rows = []
        for column in table['columns']:
            row = [column['name'], column['type'], column['description']]
            rows.append(row)
        labels = ['column', 'type', 'description']
        toolstr.print_table(
            rows,
            labels=labels,
            column_styles={
                'column': pdp.styles['metavar'],
                'type': pdp.styles['content'],
                'description': pdp.styles['description'],
            },
            # style=pdp.styles['metavar'],
            border=pdp.styles['content'],
            label_style=pdp.styles['metavar'],
            indent=4,
        )

