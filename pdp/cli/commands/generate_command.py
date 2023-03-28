from __future__ import annotations

import toolcli

import pdp

help_message = """generate a dataset

requires ctc to be installed and configured"""


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': generate_command,
        'help': 'generate a datset',
        'hidden': True,
        'args': [
            {'name': 'dataset', 'help': 'name of dataset to generate'},
            {'name': '--start-block', 'help': 'start block of dataset'},
            {'name': '--end-block', 'help': 'end block of dataset'},
            {'name': '--output-dir', 'help': 'output directory of dataset'},
        ],
        'examples': [
            'ethereum_contracts',
            'ethereum_native_transfers',
            'ethereum_slots',
        ],
    }


def generate_command(
    dataset: str,
    start_block: str | None,
    end_block: str | None,
    output_dir: str | None,
) -> None:

    # parse inputs
    if isinstance(start_block, str):
        start_block_int = int(start_block)
    else:
        raise Exception('must specify --start_block')
    if isinstance(end_block, str):
        end_block_int = int(end_block)
    else:
        raise Exception('must specify --end_block')
    if output_dir is None:
        output_dir = '.'

    # get generator module
    parsed = pdp.parse_dataset_name(dataset)
    datatype = parsed['datatype']
    raise NotImplementedError()
    # generator_module = pdp.get_generator_module(datatype)

    # # generate dataset
    # generator_module.generate(
    #     output_dir=output_dir,
    #     start_block=start_block_int,
    #     end_block=end_block_int,
    # )

