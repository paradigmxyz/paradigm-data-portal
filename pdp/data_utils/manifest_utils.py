from __future__ import annotations

import os
import typing

from .. import config_utils
from .. import spec
from . import file_utils
from . import schema_utils

if typing.TYPE_CHECKING:
    import toolsql


def get_global_manifest(
    *,
    portal_root: str | None = None,
    source: typing.Literal['remote', 'local'] = 'remote',
) -> spec.GlobalManifest:
    """get global manifest of all datasets"""

    if source == 'remote':

        import requests

        # build url
        if portal_root is None:
            portal_root = spec.portal_root
        url = spec.urls['global_manifest'].format(portal_root=portal_root)

        # get manifest
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('could not obtain global manifest at url: ' + str(url))
        manifest: spec.GlobalManifest = response.json()

        return manifest

    elif source == 'local':
        import json

        if portal_root is not None:
            data_root = portal_root
        else:
            data_root = config_utils.get_data_root(require=True)
        path = os.path.join(data_root, spec.global_manifest_filename)
        with open(path, 'r') as f:
            result: spec.GlobalManifest = json.load(f)
            return result

    else:
        raise Exception('invalid source: ' + str(source))


def get_dataset_manifest(
    dataset: str,
    *,
    portal_root: str | None = None,
    source: typing.Literal['remote', 'local'] = 'remote',
) -> spec.DatasetManifest:
    """get manifest of a particular dataset"""

    if source == 'remote':
        import requests

        parsed = schema_utils.parse_dataset_name(dataset)

        # build url
        if portal_root is None:
            portal_root = spec.portal_root
        url = spec.urls['dataset_manifest'].format(
            portal_root=portal_root,
            datatype=parsed['datatype'],
            network=parsed['network'],
        )

        # get manifest
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                'could not obtain dataset manifest at url: ' + str(url)
            )
        manifest: spec.DatasetManifest = response.json()

        return manifest

    elif source == 'local':
        import json

        if portal_root is not None:
            data_root = portal_root
        else:
            data_root = config_utils.get_data_root(require=True)
        path = os.path.join(data_root, dataset, spec.dataset_manifest_filename)
        with open(path, 'r') as f:
            result: spec.DatasetManifest = json.load(f)
            return result

    else:
        raise Exception('invalid source: ' + str(source))


def create_global_manifest(
    *,
    data_root: str | None = None,
    datasets: typing.Mapping[str, spec.DatasetManifestSlim] | None = None,
    version: str | None,
    output_path: str | bool | None = None,
    confirm: bool = False,
) -> spec.GlobalManifest:
    """create global manifest describing all datasets"""

    import json

    # versions
    if version is None:
        version = spec.global_version

    print('creating global manifest', version)
    print()

    # gather dataset manifests
    if datasets is None:
        if data_root is None:
            raise Exception('must specify data_root or datasets')
        found_datasets: typing.MutableMapping[
            str, spec.DatasetManifestSlim
        ] = {}
        for item in os.listdir(data_root):
            path = os.path.join(data_root, item)
            if os.path.isdir(path):
                if spec.dataset_manifest_filename in os.listdir(path):
                    manifest_path = os.path.join(
                        path, spec.dataset_manifest_filename
                    )
                    with open(manifest_path) as f:
                        dataset_manifest = json.load(f)
                    name = dataset_manifest['name']
                    found_datasets[name] = _reduce_dataset_manifest(
                        dataset_manifest
                    )
                    print('gathered:', item)
                else:
                    print('no dataset manifest found for: ' + item)
        datasets = found_datasets

    # create global manifest
    global_manifest: spec.GlobalManifest = {
        'version': version,
        'datasets': datasets,
    }

    if len(datasets) == 0:
        print('no datasets detected for global manifest')
        return global_manifest

    # write output file
    if output_path is not None and output_path:
        import shutil

        if isinstance(output_path, bool):
            if data_root is not None:
                output_dir = data_root
            else:
                output_dir = '.'
            output_path = os.path.join(
                output_dir, spec.global_manifest_filename
            )

        if os.path.exists(output_path) and not confirm:
            raise Exception('use --confirm to overwrite existing file')

        with open(output_path + '_tmp', 'w') as f:
            json.dump(global_manifest, f, indent=4, sort_keys=True)
        shutil.move(output_path + '_tmp', output_path)
        if data_root is not None:
            print_dir = os.path.relpath(output_path, data_root)
        else:
            print_dir = output_path
        print()
        print('wrote global manifest to:', print_dir)

    return global_manifest


def _reduce_dataset_manifest(
    manifest: spec.DatasetManifest,
) -> spec.DatasetManifestSlim:
    return {
        'name': manifest['name'],
        'version': manifest['version'],
        'description': manifest['description'],
        'datatype': manifest['datatype'],
        'network': manifest['network'],
        'n_files': len(manifest['files']),
        'n_bytes': sum(file['n_bytes'] for file in manifest['files']),
        'schema': manifest['schema'],
    }


def create_dataset_manifest(
    *,
    dataset_dir: str | None = None,
    name: str | None = None,
    version: str | None = None,
    datatype: str | None = None,
    network: str | None = None,
    description: str | None = None,
    data_root: str | None = None,
    schema: toolsql.DBSchemaShorthand | None = None,
    paths: typing.Sequence[str] | None = None,
    reuse_hashes: bool = False,
    output_path: str | bool | None = None,
    confirm: bool = False,
) -> spec.DatasetManifest:
    """describe dataset manifest describing dataset contents"""

    import json

    # ensure valid output path
    if output_path is not None and output_path:
        if isinstance(output_path, bool):
            if data_root is not None:
                output_dir = data_root
            else:
                output_dir = '.'
            output_path = os.path.join(
                output_dir, spec.dataset_manifest_filename
            )
        if os.path.exists(output_path) and not confirm:
            raise Exception('use --confirm to overwrite existing file')

    # gather metadata
    if dataset_dir is not None:
        dataset_dir = os.path.abspath(os.path.expanduser(dataset_dir))
    if name is None:
        if dataset_dir is None:
            raise Exception('must specify dataset_dir or name')
        name = os.path.basename(dataset_dir)
    if network is None or datatype is None:
        parsed = schema_utils.parse_dataset_name(name)
        parsed_network = parsed['network']
        parsed_datatype = parsed['datatype']
        if network is None:
            network = parsed_network
        elif network != parsed_network:
            raise Exception('parsed network does not equal input network')
        if datatype is None:
            datatype = parsed_datatype
        elif datatype != parsed_datatype:
            raise Exception('parsed datatype does not equal input datatype')
    try:
        module = schema_utils._get_datatype_module(datatype)
    except Exception:
        module = None
    if version is None:
        if module is not None:
            version = module.version
        else:
            raise Exception('unknown version for dataset')
    if description is None:
        if module is not None:
            description = module.schema['description']
        else:
            raise Exception('could not find description for dataset')
    if schema is None:
        if module is not None:
            schema = module.schema
        else:
            raise Exception('could not find schema for dataset')
    schema_normalized = toolsql.normalize_shorthand_db_schema(schema)
    print('creating manifest for', name, version)

    # gather files
    if paths is None:
        if dataset_dir is None:
            raise Exception('must specify paths or dataset_dir')
        exclude = [
            spec.dataset_manifest_filename,
            spec.dataset_readme_filename,
        ] + spec.dataset_license_filenames
        paths = [
            os.path.join(dataset_dir, filename)
            for filename in sorted(os.listdir(dataset_dir))
            if filename not in exclude
        ]

    # gather hashes
    print('gathering hashes of', len(paths), 'files')
    if reuse_hashes:
        if output_path is None:
            raise Exception('must specify output_path when reuse_hashes=True')
        with open(output_path, 'r') as f:
            old_data = json.load(f)
        old_hashes = {file['name']: file['hash'] for file in old_data['files']}
    file_hashes = []
    for path in paths:
        if reuse_hashes and os.path.basename(path) in old_hashes:
            file_hashes.append(old_hashes[os.path.basename(path)])
        else:
            file_hashes.append(file_utils.get_file_hash(path))

    # assemble files
    files = []
    for path, file_hash in zip(paths, file_hashes):
        file: spec.FileMetadata = {
            'name': os.path.basename(path),
            'hash': file_hash,
            'n_bytes': os.path.getsize(path),
        }
        files.append(file)

    # build manifest
    manifest: spec.DatasetManifest = {
        'name': name,
        'version': version,
        'description': description or '',
        'datatype': datatype,
        'network': network,
        'files': files,
        'schema': schema_normalized,
    }

    # save manifest
    if output_path is not None and output_path:
        import shutil

        with open(output_path + '_tmp', 'w') as f:
            json.dump(manifest, f, indent=4, sort_keys=True)

        shutil.move(output_path + '_tmp', output_path)
        if data_root is not None:
            print_dir = os.path.relpath(output_path, data_root)
        else:
            print_dir = output_path
        print('wrote dataset manifest to:', print_dir)

    return manifest

