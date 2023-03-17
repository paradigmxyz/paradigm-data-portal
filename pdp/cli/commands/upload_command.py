from __future__ import annotations

import json
import os

import toolcli

import pdp


help_message = """upload files to bucket

If local-path not specified, upload current directory

If bucket-path not specified, upload relative to global manifest location"""


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': upload_command,
        'help': help_message,
        'args': [
            {
                'name': 'local-path',
                'help': 'local path to upload from',
                'nargs': '?',
            },
            {
                'name': 'bucket-path',
                'help': 'bucket path to upload to',
                'nargs': '?',
            },
            {
                'name': '--all',
                'help': 'upload all files in directory instead of just manifest files',
                'action': 'store_true',
                'dest': 'all_files',
            },
        ],
        'examples': {
            '': 'upload current directory',
            '/path/to/some/dir': 'upload some other directory',
        },
        'hidden': True,
    }


def upload_command(
    *, local_path: str, bucket_path: str, all_files: bool
) -> None:

    if local_path is None:
        local_path = '.'
    local_path = os.path.abspath(os.path.expanduser(local_path))
    if os.path.isdir(local_path):
        local_dir = local_path
    elif os.path.isfile(local_path):
        local_dir = os.path.dirname(local_path)
    else:
        raise Exception()

    # if local_path is a dataset directory, upload according to manifest
    dir_files = None
    if os.path.isdir(local_path):
        dir_contents = os.listdir(local_path)

        if all_files:
            dir_files = None

        elif pdp.global_manifest_filename in dir_contents:
            print('uploading global manifest:', pdp.global_manifest_filename)
            dir_files = [pdp.global_manifest_filename]

        elif pdp.dataset_manifest_filename in dir_contents:
            print(
                'uploading files in dataset manifest:',
                pdp.dataset_manifest_filename,
            )
            manifest_path = os.path.join(
                local_path, pdp.dataset_manifest_filename
            )
            with open(manifest_path) as f:
                dataset_manifest = json.load(f)
            dir_files = [pdp.dataset_manifest_filename]
            for file in dataset_manifest['files']:
                dir_files.append(file['name'])

        else:
            raise Exception(
                'no manifest file found, use --all to upload all files'
            )

    if bucket_path is None:

        if pdp.global_manifest_filename in os.listdir(local_dir):
            # assume local_dir is global root,
            bucket_path = pdp.bucket_root_path

        else:

            # find root dir
            data_root = local_dir
            while pdp.global_manifest_filename not in os.listdir(data_root):
                next_data_root = os.path.dirname(data_root)
                if next_data_root == data_root:
                    raise Exception(
                        'could not find global data root, must specify bucket-path manually'
                    )
                data_root = next_data_root

            # get path relative to root dir
            local_relpath = os.path.relpath(local_path, data_root)
            bucket_path = os.path.join(pdp.bucket_root_path, local_relpath)

    if os.path.isfile(local_path):
        pdp.upload_file(
            local_path=local_path,
            bucket_path=bucket_path,
        )
    else:
        pdp.upload_directory(
            local_path=local_path,
            dir_files=dir_files,
            bucket_path=bucket_path,
        )

