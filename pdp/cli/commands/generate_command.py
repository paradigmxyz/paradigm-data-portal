from __future__ import annotations

import typing

import toolcli

import pdp

if typing.TYPE_CHECKING:
    import ctc.spec


help_message = """generate a dataset

requires ctc to be installed and configured"""


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': generate_command,
        'help': 'generate a datset',
        'hidden': True,
        'args': [
            {'name': 'dataset', 'help': 'name of dataset to generate'},
            {'name': 'blocks', 'nargs': '?', 'help': 'name of dataset to generate'},
            {'name': '--output-dir', 'help': 'output directory of dataset'},
            {'name': '--chunk-size', 'help': 'blocks per chunk'},
            {
                'name': '--csv',
                'help': 'use csv as output format',
                'action': 'store_true',
            },
            {
                'name': '--parquet',
                'help': 'use parquet as output_format',
                'action': 'store_true',
            },
            {
                'name': '--serial',
                'help': 'use serial execution instead of parallel',
                'action': 'store_true',
            },
        ],
        'examples': [
            'ethereum_contracts',
            'ethereum_native_transfers',
            'ethereum_slots',
        ],
    }


def generate_command(
    dataset: str,
    blocks: str,
    output_dir: str | None,
    chunk_size: str | None,
    csv: bool,
    parquet: bool,
    serial: bool,
) -> None:
    # parse inputs
    if blocks is None:
        start_block = 0
        end_block: ctc.spec.BlockNumberReference = 'latest'
    else:
        if ':' not in blocks:
            print('must specify block range using one of these formats:')
            print('    `start_block:end_block`')
            print('    `start_block:`           (use latest block as end_block)')
            print('    `:end_block`             (use block 0 as start_block)')
            return
        start_block_str, end_block_str = blocks.split(':')
        if start_block_str == '':
            start_block = 0
        else:
            start_block = int(start_block_str)
        if end_block_str == '':
            end_block = 'latest'
        else:
            end_block = int(end_block_str)

    if output_dir is None:
        output_dir = '.'

    if chunk_size is not None:
        chunk_size_int = int(chunk_size)
    else:
        chunk_size_int = None

    if parquet:
        output_filetype = 'parquet'
    elif csv:
        output_filetype = 'csv'
    else:
        output_filetype = None

    if serial:
        executor: typing.Literal['parallel', 'serial'] = 'serial'
    else:
        executor = 'parallel'

    # get generator module
    parsed = pdp.parse_dataset_name(dataset)
    datatype = parsed['datatype']
    network = parsed['network']

    if datatype == 'contracts':
        from pdp.datasets import contracts

        contracts.generate_contracts_dataset(
            start_block=start_block,
            end_block=end_block,
            output_dir=output_dir,
            network=network,
            chunk_size=chunk_size_int,
            output_filetype=output_filetype,
            executor=executor,
        )
    elif datatype == 'native_transfers':
        from pdp.datasets import native_transfers

        native_transfers.generate_native_transfers_dataset(
            start_block=start_block,
            end_block=end_block,
            output_dir=output_dir,
            network=network,
            chunk_size=chunk_size_int,
            output_filetype=output_filetype,
            executor=executor,
        )
    elif datatype == 'slots':
        from pdp.datasets import slots

        slots.generate_slots_dataset(
            start_block=start_block,
            end_block=end_block,
            output_dir=output_dir,
            network=network,
            chunk_size=chunk_size_int,
            output_filetype=output_filetype,
            executor=executor,
        )
    else:
        raise Exception('invalid datatype: ' + str(datatype))

