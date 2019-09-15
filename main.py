import argparse
import logging
import sys

from typing import List

from doc_mocker.manager import Manager
from doc_mocker.models import PageType
from doc_mocker.seeders import PageSeeder
from doc_mocker.plugin_loader import PluginLoader


logger = logging.getLogger(__name__)


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command to run", choices=["generate"])
    parser.add_argument(
        "-n",
        "--number-of-pages",
        help="number of pages to generate (default: 1)",
        default="1",
        type=int,
    )
    parser.add_argument(
        "-t",
        "--page-type",
        help=f"page type (default: {PageType.A4.name})",
        default=PageType.A4.name,
        choices=[type_.name for type_ in PageType],
    )
    parser.add_argument(
        "-s",
        "--page-seeder",
        help=f"page seeder (default: {PageSeeder.BASIC.name})",
        default=PageSeeder.BASIC.name,
        choices=[seeder.name for seeder in PageSeeder],
    )
    parser.add_argument(
        "-o", "--output-path", help="output path (default: current path)", default="."
    )

    if '-h' not in sys.argv and '--help' not in sys.argv:
        main_args, argv = parser.parse_known_args()

    # setting up plugin arguments
    plugins_index = {}
    for name, plugin in PluginLoader.get_all().items():
        for arg_name, arg_config in plugin.arguments:
            parser.add_argument(*arg_name, **arg_config)
            plugins_index[arg_name[0]] = plugin

    parser.parse_args()

    plugins = []
    for argv in split_plugins_arguments(argv):
        plugin = plugins_index[argv[0]]
        parser = argparse.ArgumentParser()
        for arg_name, arg_config in plugin.arguments:
            parser.add_argument(*arg_name, **arg_config)
        namespace, _ = parser.parse_known_args(argv)
        try:
            plugins.append(plugin.cls(namespace))
        except Exception as e:
            logger.error(f"Plugin setup failed [{' '.join(argv)}]: {e}")

    Manager(
        pages=main_args.number_of_pages,
        type_=main_args.page_type,
        seeder=main_args.page_seeder,
        output_path=main_args.output_path,
        plugins=plugins,
    ).run(main_args.command)


def split_plugins_arguments(arguments: List[str]) -> List[List[str]]:
    split_args = []
    for argument in arguments:
        if argument.startswith('-'):
            split_args.append([argument])
        else:
            split_args[-1].append(argument)
    return split_args


if __name__ == "__main__":
    run()
