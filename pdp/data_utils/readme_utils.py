"""functions for creating dataset README's"""

from __future__ import annotations

import os

from .. import spec
from . import download_utils
from . import schema_utils


readme_template = """
# {network} {datatype} Dataset v{version}

This is a dataset of {description}

The dataset was created by using [this script]({script_url})

Data is distributed as [parquet](https://data.paradigm.xyz/about) files and released into the public domain under a [CC0 license](https://creativecommons.org/share-your-work/public-domain/cc0/)

## Usage

Some example uses of this dataset include:
{example_usage}

{notebook_str}

## Schema

{schema}

## Download

This dataset can be downloaded using either the `pdp` cli tool or the urls below

The total dataset size is **{dataset_size}**

### Use `pdp`

The command `pdp download {dataset_name}` will download all files in this dataset

See `pdp download -h` for available options

### Use URLs

| | file | size |
| - | - | - |
{file_urls}
"""

script_url_template = 'https://github.com/paradigmxyz/paradigm-data-portal/blob/main/pdp/datasets/{dataset}/{dataset}_collect.py'

notebook_url_template = 'https://github.com/paradigmxyz/paradigm-data-portal/blob/main/notebooks/explore_{dataset_name}.ipynb'

table_schema_template = """#### `{table_name}` table
{table_description}
| column | type | description |
| - | - | - |
{table_rows}"""


def create_dataset_readme(
    dataset_manifest: spec.DatasetManifest,
    output_path: str | bool = False,
    confirm: bool = False,
) -> str:

    import shutil

    readme_str = _create_readme_str(dataset_manifest)

    if output_path is not None and output_path:
        if isinstance(output_path, bool):
            output_path = spec.dataset_readme_filename
        if os.path.exists(output_path) and not confirm:
            print('use --confirm to overwrite existing README')
        with open(output_path + '_tmp', 'w') as f:
            f.write(readme_str)
        shutil.move(output_path + '_tmp', output_path)
        print('wrote README to ' + output_path)

    return readme_str


def _create_readme_str(dataset_manifest: spec.DatasetManifest) -> str:

    import toolsql
    import toolstr

    module = schema_utils._get_datatype_module(dataset_manifest['datatype'])
    example_usage_pieces = ['- ' + example for example in module.example_usage]
    example_usage_str = '\n'.join(example_usage_pieces)

    schema_pieces = []
    db_schema = toolsql.normalize_shorthand_db_schema(
        dataset_manifest['schema']
    )
    for table_name, table in db_schema['tables'].items():
        table_table_pieces = [
            '| '
            + column['name']
            + ' | '
            + column['type']
            + ' | '
            + (column['description'] or '')
            + ' |'
            for column in table['columns']
        ]
        table_table = '\n'.join(table_table_pieces)
        table_schema_str = table_schema_template.format(
            table_name=table['name'],
            table_description=table['description'],
            table_rows=table_table,
        )
        schema_pieces.append(table_schema_str)
    schema_str = '\n'.join(schema_pieces)

    url_pieces: list[str] = []
    for file in dataset_manifest['files']:
        if file['name'] == spec.dataset_readme_filename:
            continue
        file_url = download_utils.get_dataset_file_url(
            datatype=dataset_manifest['datatype'],
            network=dataset_manifest['network'],
            filename=file['name'],
        )
        url_piece = (
            '| '
            + str(len(url_pieces) + 1)
            + ' | '
            + ('[' + file['name'] + '](' + file_url + ')')
            + ' | '
            + toolstr.format_nbytes(file['n_bytes'])
            + ' |'
        )
        url_pieces.append(url_piece)
    url_str = '\n'.join(url_pieces)

    dataset_nbytes = sum(file['n_bytes'] for file in dataset_manifest['files'])

    if dataset_manifest['datatype'] == 'contracts':
        notebook_url = notebook_url_template.format(
            dataset_name=dataset_manifest['name']
        )
        notebook_str = """An example notebook exploring this dataset can be found [here]({notebook_url})""".format(
            notebook_url=notebook_url
        )
    else:
        notebook_str = ''

    return readme_template.format(
        dataset_name=dataset_manifest['name'],
        network=dataset_manifest['network'].replace('_', ' ').title(),
        datatype=dataset_manifest['datatype'].replace('_', ' ').title(),
        version=dataset_manifest['version'],
        description=dataset_manifest['description'],
        example_usage=example_usage_str,
        schema=schema_str,
        dataset_size=toolstr.format_nbytes(dataset_nbytes),
        script_url=script_url_template.format(dataset=dataset_manifest['name']),
        notebook_str=notebook_str,
        file_urls=url_str,
    )

