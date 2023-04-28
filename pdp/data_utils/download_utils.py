"""functions for downloading datasets"""

from __future__ import annotations

import os
import typing

from .. import spec
from . import file_utils
from . import manifest_utils
from . import schema_utils


def download_dataset(
    dataset: str,
    *,
    output_dir: str,
    portal_root: str | None = None,
    skip_existing: bool = True,
) -> None:
    """download files of a dataset"""

    print('Downloading dataset:', dataset)

    urls = get_dataset_file_urls(dataset, portal_root=portal_root)

    base_url = os.path.dirname(urls[0])
    readme_url = os.path.join(base_url, 'README.md')
    manifest_url = os.path.join(base_url, 'dataset_manifest.json')
    file_utils.download_files(
        urls=[readme_url, manifest_url],
        output_dir=output_dir,
        skip_existing=skip_existing,
    )

    # download files
    file_utils.download_files(
        urls=urls,
        output_dir=output_dir,
        skip_existing=skip_existing,
    )


def get_dataset_file_urls(
    dataset: str,
    *,
    portal_root: str | None,
    manifest: spec.DatasetManifest | None = None,
) -> typing.Sequence[str]:
    """get file urls of a dataset"""

    parsed = schema_utils.parse_dataset_name(dataset)

    if portal_root is None:
        portal_root = spec.portal_root
    if manifest is None:
        manifest = manifest_utils.get_dataset_manifest(
            dataset=dataset, portal_root=portal_root
        )
    urls = []
    for file in manifest['files']:
        url = spec.urls['dataset_file'].format(
            portal_root=portal_root,
            datatype=parsed['datatype'],
            network=parsed['network'],
            filename=file['name'],
        )
        urls.append(url)
    return urls


def get_dataset_file_url(
    datatype: str,
    network: str,
    filename: str,
    portal_root: str | None = None,
) -> str:
    if portal_root is None:
        portal_root = spec.portal_root
    return spec.urls['dataset_file'].format(
        portal_root=portal_root,
        datatype=datatype,
        network=network,
        filename=filename,
    )


def validate_dataset_directory(path: str, *, no_hashes: bool = False) -> bool:
    """validate the files in a dataset directory"""

    import json

    # load manifest
    manifest_path = os.path.join(path, spec.dataset_manifest_filename)
    if not os.path.isfile(manifest_path):
        raise Exception(
            'no ' + spec.dataset_manifest_filename + ' found in directory'
        )
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    manifest_files = {file['name'] for file in manifest['files']}

    print('validating data of', manifest['name'], 'in', path)

    # gather files present
    present_files = set(os.listdir(path))

    # check for missing files
    missing_files = manifest_files - present_files

    # check for extra files
    extra_files = (present_files - manifest_files) - {
        spec.dataset_manifest_filename
    }

    # check file hashes
    if no_hashes:
        bad_hashes = None
    else:
        bad_hashes = []
        for file in manifest['files']:
            if file['name'] in present_files:
                hash = file_utils.get_file_hash(
                    os.path.join(path, file['name'])
                )
                target_hash = file['hash']
                if hash != target_hash:
                    bad_hashes.append(file['name'])

    # print errors
    print()
    errors_found = 0
    skipping = False
    for error_name, errors in {
        'missing files': missing_files,
        'extra files': extra_files,
        'bad hashes': bad_hashes,
    }.items():
        if errors is None:
            print('SKIPPED checking for ' + error_name)
            skipping = True
            continue
        if len(errors) > 0:
            errors_found += len(errors)
            print(error_name + ':')
            for file in sorted(errors)[:10]:
                print('-', file)
            if len(errors) > 10:
                print('- ...')

    # print summary
    if errors_found > 0 or skipping:
        print()
    print(
        len(missing_files),
        'missing files,',
        len(extra_files),
        'extra files, and',
        len(bad_hashes) if bad_hashes is not None else 0,
        'bad hashes',
    )

    return not errors_found

