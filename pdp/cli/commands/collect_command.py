from __future__ import annotations

import os
import typing

import toolcli

import pdp

if typing.TYPE_CHECKING:
    import ctc.spec


help_message = """collect a dataset

collecting on-chain datasets requires ctc to be installed and configured"""


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': collect_command,
        'help': 'collect a dataset',
        'args': [
            {'name': 'dataset', 'help': 'name of dataset to collect'},
            {
                'name': 'output-dir',
                'nargs': '?',
                'help': 'output directory, omit to use PDP_DATA_ROOT',
            },
            {
                'name': '--blocks',
                'help': 'block range, as `\[start_block]:\[end_block]`',
            },
            {
                'name': '--rpc',
                'help': 'rpc node url, omit to use ctc configuration',
            },
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
            {
                'name': '--chunk-size',
                'help': 'blocks per chunk',
            },
            {
                'name': ('-v', '--verbose'),
                'help': 'output additional information',
                'action': 'store_true',
            },
        ],
        'examples': [
            'ethereum_contracts',
            'ethereum_native_transfers',
            'ethereum_slots',
        ],
    }


def collect_command(
    dataset: str,
    blocks: str | None,
    rpc: str | None,
    output_dir: str | None,
    chunk_size: str | None,
    csv: bool,
    parquet: bool,
    serial: bool,
    verbose: bool,
) -> None:
    #
    # # parse inputs
    #
    parsed = pdp.parse_dataset_name(dataset)
    datatype = parsed['datatype']
    network = parsed['network']

    if rpc is None:
        context: ctc.spec.Context = {'network': network}
    else:
        context = {'network': network, 'provider': rpc}

    if blocks is None:
        ctc = pdp.get_ctc()
        start_block = 0
        end_block = ctc.rpc.sync_eth_block_number(context=context)
    else:
        if ':' not in blocks:
            print('must specify block range using one of these formats:')
            print('    `start_block:end_block`')
            print(
                '    `start_block:`           (use latest block as end_block)'
            )
            print('    `:end_block`             (use block 0 as start_block)')
            return
        start_block_str, end_block_str = blocks.split(':')
        if start_block_str == '':
            start_block = 0
        else:
            start_block = int(start_block_str)
        if end_block_str == '':
            ctc = pdp.get_ctc()
            end_block = ctc.rpc.sync_eth_block_number(context=context)
        else:
            end_block = int(end_block_str)

    if output_dir is None:
        data_root = pdp.get_data_root(require=False)
        if data_root is None or data_root == '':
            raise Exception(
                'must specify output_dir or set PDP_DATA_ROOT env var'
            )
        else:
            output_dir = os.path.join(data_root, dataset)

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

    #
    # # perform collection
    #

    if datatype == 'contracts':
        from pdp.datasets import contracts

        contracts.collect_contracts_dataset(
            start_block=start_block,
            end_block=end_block,
            output_dir=output_dir,
            network=network,
            chunk_size=chunk_size_int,
            output_filetype=output_filetype,
            executor=executor,
            verbose=verbose,
        )
    elif datatype == 'native_transfers':
        from pdp.datasets import native_transfers

        native_transfers.collect_native_transfers_dataset(
            start_block=start_block,
            end_block=end_block,
            output_dir=output_dir,
            network=network,
            chunk_size=chunk_size_int,
            output_filetype=output_filetype,
            executor=executor,
            verbose=verbose,
        )
    elif datatype == 'slots':
        from pdp.datasets import slots

        slots.collect_slots_dataset(
            start_block=start_block,
            end_block=end_block,
            output_dir=output_dir,
            network=network,
            chunk_size=chunk_size_int,
            output_filetype=output_filetype,
            executor=executor,
            verbose=verbose,
        )
    else:
        raise Exception('invalid datatype: ' + str(datatype))

