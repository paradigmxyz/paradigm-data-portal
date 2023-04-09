from __future__ import annotations

import typing


if typing.TYPE_CHECKING:

    import toolcli
    import toolsql

    class GlobalManifest(typing.TypedDict):
        """manifest of all datasets"""

        version: str
        datasets: typing.Mapping[str, DatasetManifestSlim]

    class DatasetManifest(typing.TypedDict):
        """manifest of a particular dataset"""

        name: str
        version: str
        description: str
        datatype: str
        network: str
        files: typing.Sequence[FileMetadata]
        schema: toolsql.DBSchemaShorthand

    class DatasetManifestSlim(typing.TypedDict):
        """manifest of a particular dataset"""

        name: str
        version: str
        description: str
        datatype: str
        network: str
        n_files: int
        n_bytes: int
        schema: toolsql.DBSchemaShorthand

    class FileMetadata(typing.TypedDict):
        """metadata of a dataset file"""

        name: str
        hash: str
        n_bytes: int

#
# # datasets
#

global_version = '1.0.0'

networks = {
    1: 'ethereum',
}

#
# # urls and paths
#

# default portal root
portal_root = 'https://datasets.paradigm.xyz/datasets'
bucket_root_path = 'datasets'

# schema for various portal urls
urls = {
    'global_manifest': '{portal_root}/global_manifest.json',
    'dataset_manifest': '{portal_root}/{network}_{datatype}/dataset_manifest.json',
    'dataset_file': '{portal_root}/{network}_{datatype}/{filename}',
    'old_global_manifests': '{portal_root}/old_global_manifests/v{version}.json',
    'old_dataset_manifest': '{portal_root}/old_dataset_manifests/{dataset}__v{version}.json',
}

global_manifest_filename = 'global_manifest.json'
dataset_manifest_filename = 'dataset_manifest.json'
dataset_readme_filename = 'README.md'
dataset_filename_template = '{dataset}__v{version}__{file_id}.{filetype}'
dataset_license_filenames = ['LICENSE-CC0']


#
# # cli behavior
#

styles: toolcli.StyleTheme = {
    'title': 'bold #00e100',
    'metavar': '#e5e9f0',
    'description': '#aaaaaa',
    'content': '#00B400',
    'option': 'bold #e5e9f0',
    'comment': '#888888',
}

