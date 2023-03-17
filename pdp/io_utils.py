from __future__ import annotations

import os
import typing


def download_files(
    urls: typing.Sequence[str],
    *,
    output_dir: str,
    skip_existing: bool = True,
) -> None:
    """download a list of files"""

    # get output dir
    if output_dir is None:
        output_dir = '.'
    output_dir = os.path.abspath(os.path.expanduser(output_dir))

    print('downloading', len(urls), 'files')
    print()
    print('using output_dir', output_dir)

    # skip existing files
    if skip_existing:
        url_filenames = [os.path.basename(url) for url in urls]
        skip_urls = set()
        for url, filename in zip(urls, url_filenames):
            if filename in os.listdir(output_dir):
                skip_urls.add(url)
        if len(skip_urls) > 0:
            print()
            print('skipping', len(skip_urls), 'files that already exist')
    else:
        skip_urls = set()

    # download files
    for url in urls:
        if url not in skip_urls:
            download_file(url)

    print()
    print('done')


def download_file(url: str) -> None:
    """download a file"""
    import subprocess

    print()
    print('downloading', url)
    subprocess.call(['curl', url, '--output', os.path.basename(url)])


def get_file_hash(path: str) -> str:
    """get hash of file"""

    import hashlib

    with open(path, 'rb') as f:
        hashed = hashlib.md5(f.read())

    return hashed.hexdigest()


def get_file_hashes(paths: typing.Sequence[str]) -> typing.Sequence[str]:
    """get hashes of multiple files"""

    return [get_file_hash(path) for path in paths]


def upload_file(local_path: str, bucket_path: str) -> None:
    """upload single file to s3 bucket"""

    import subprocess

    command = [
        'rclone',
        'copyto',
        local_path,
        'paradigm-data-portal:' + bucket_path,
        '-v',
    ]

    subprocess.call(command)


def upload_directory(
    local_path: str,
    bucket_path: str,
    *,
    dir_files: typing.Sequence[str] | None,
    remove_deleted_files: bool = False,
) -> None:
    """upload nested directory of files to s3 bucket"""

    import subprocess

    print('uploading directory:', local_path)
    print('to bucket path:', bucket_path)
    print()

    if remove_deleted_files:
        action = 'sync'
    else:
        action = 'copy'

    command = [
        'rclone',
        action,
        local_path,
        'paradigm-data-portal:' + bucket_path,
        '-v',
    ]

    if dir_files is not None:
        # create tempfile with list of files to upload
        import tempfile

        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, 'file_list.txt')
        with open(temp_path, 'w') as f:
            f.write('\n'.join(dir_files))
        command.extend(['--files-from', temp_path])

    else:
        command.extend(['--exclude', '".*"'])

    subprocess.call(command)

