from __future__ import annotations

import os
import typing

import toolcli

import pdp

if typing.TYPE_CHECKING:
    import ctc.spec

    class StandardCollectKwargs(typing.TypedDict):
        start_block: int
        end_block: int
        output_dir: str
        network: str
        chunk_size: int | None
        output_filetype: str | None
        executor: typing.Literal['parallel', 'serial']
        verbose: bool


help_message = """collect a dataset from RPC nodes or other sources

collecting on-chain datasets requires ctc to be installed and configured"""


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': collect_command,
        'help': help_message,
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
                'name': ('-v', '--verbose'),
                'help': 'output additional information',
                'action': 'store_true',
            },
            {
                'name': '--extension',
                'help': 'extension module.function for dataset collection',
                'hidden': True,
            },
            {
                'name': '--parameters',
                'help': 'extra parameters given to collection function',
                'hidden': True,
            },
        ],
        'examples': [
            'ethereum_contracts',
            'ethereum_native_transfers',
            'ethereum_slots --blocks 14_000_000:14_100_000',
        ],
    }


def collect_command(
    dataset: str,
    blocks: str | None,
    rpc: str | None,
    output_dir: str | None,
    csv: bool,
    parquet: bool,
    serial: bool,
    verbose: bool,
    extension: str | None,
    parameters: str | None,
) -> None:
    # get context
    parsed = pdp.parse_dataset_name(dataset)
    datatype = parsed['datatype']
    network = parsed['network']
    if rpc is None:
        context: ctc.spec.Context = {'network': network}
    else:
        context = {'network': network, 'provider': rpc}

    # get block range
    if blocks is None:
        pdp.ensure_ctc()
        import ctc
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

        if blocks.count(':') == 1:
            start_block_str, end_block_str = blocks.split(':')
        elif blocks.count(':') == 2:
            start_block_str, end_block_str, chunk_size_str = blocks.split(':')
            if chunk_size_str == '':
                chunk_size_int = None
            else:
                chunk_size_int = int(chunk_size_str)
                if chunk_size_int < 1:
                    raise Exception('chunk_size must be >= 1')
        if start_block_str == '':
            start_block = 0
        else:
            start_block = int(start_block_str)
        if end_block_str == '':
            pdp.ensure_ctc()
            import ctc
            end_block = ctc.rpc.sync_eth_block_number(context=context)
        else:
            end_block = int(end_block_str)

    # parse output parameters
    if output_dir is None:
        data_root = pdp.get_data_root(require=False)
        if data_root is None or data_root == '':
            raise Exception(
                'must specify output_dir or set PDP_DATA_ROOT env var'
            )
        else:
            output_dir = os.path.join(data_root, dataset)
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

    # collect parameters
    if parameters is not None:
        import ast

        extra_kwargs = ast.literal_eval(parameters)
        if not isinstance(extra_kwargs, dict):
            raise Exception(
                'extra parameters should be specified with dict syntax'
            )
    else:
        extra_kwargs = {}
    standard_kwargs: StandardCollectKwargs = {
        'start_block': start_block,
        'end_block': end_block,
        'output_dir': output_dir,
        'network': network,
        'chunk_size': chunk_size_int,
        'output_filetype': output_filetype,
        'executor': executor,
        'verbose': verbose,
    }

    #
    # # perform collection
    #

    if datatype == 'contracts':
        from pdp.datasets import contracts

        contracts.collect_contracts_dataset(**standard_kwargs, **extra_kwargs)

    elif datatype == 'native_transfers':
        from pdp.datasets import native_transfers

        native_transfers.collect_native_transfers_dataset(
            **standard_kwargs, **extra_kwargs
        )

    elif datatype == 'slots':
        from pdp.datasets import slots

        slots.collect_slots_dataset(**standard_kwargs, **extra_kwargs)

    elif extension is not None:
        import importlib

        try:
            module_path = (
                extension
                + '.datasets.'
                + datatype
                + '.'
                + datatype
                + '_collect'
            )
            module = importlib.import_module(module_path)
            function_name = 'collect_' + datatype + '_dataset'
            function = getattr(module, function_name)
        except (ValueError, ImportError, AttributeError):
            print('invalid extension, could not get extension function')
            return

        function(**standard_kwargs, **extra_kwargs)

    else:
        raise Exception('invalid datatype: ' + str(datatype))

