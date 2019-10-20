import argparse
import logging
import sys

from enum import Enum
from typing import List

from doc_mocker.manager import Manager
from doc_mocker.models import PageType
from doc_mocker.seeders import PageSeeder
from doc_mocker.plugin_loader import PluginLoader

logger = logging.getLogger(__name__)


class LoggingLevel(Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warn = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL


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
    seeder_choices_text = ", ".join(seeder.value.arg_name for seeder in PageSeeder)
    parser.add_argument(
        "-s",
        "--page-seeder",
        help=f"choices: {{{seeder_choices_text}}}",
        default=PageSeeder.basic.name,
    )
    parser.add_argument(
        "-o", "--output-path", help="output path (default: current path)", default="."
    )
    parser.add_argument(
        "-l",
        "--logging",
        help="Logging level (default e: error)",
        default=LoggingLevel.error.name,
        choices=[level.name for level in LoggingLevel],
    )

    if "-h" not in sys.argv and "--help" not in sys.argv:
        main_args, argv = parser.parse_known_args()
        validate_seeder(parser, main_args, seeder_choices_text)

    # setting up plugin arguments
    plugins_index = {}
    for name, plugin in PluginLoader.get_all().items():
        for arg_name, arg_config in plugin.arguments:
            parser.add_argument(*arg_name, **arg_config)
            plugins_index[arg_name[0]] = plugin

    parser.parse_args()

    logging.basicConfig(level=LoggingLevel[main_args.logging].value)

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
        if argument.startswith("-"):
            split_args.append([argument])
        else:
            split_args[-1].append(argument)
    return split_args


def validate_seeder(parser, main_args, choices_text):
    if main_args.page_seeder.split(":")[0] not in {seeder.name for seeder in PageSeeder}:
        parser.print_usage()
        sys.stderr.write(
            f"error: argument -s/--seeder: invalid choice: {main_args.page_seeder}"
            f" (choose from {choices_text})\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    run()
