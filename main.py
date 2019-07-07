import argparse

import sys

from doc_mocker.manager import Manager
from doc_mocker.models import PageType
from doc_mocker.seeders import PageSeeder
from doc_mocker.plugin_loader import PluginLoader


def run():
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

    # setting up plugin arguments
    plugins = PluginLoader.get_all()
    for name, plugin in plugins.items():
        for arg_name, arg_config in plugin.arguments:
            parser.add_argument(*arg_name, **arg_config)

    args = parser.parse_args()

    try:
        plugins = [plugin.cls(args) for plugin in plugins.values()]
    except ValueError as e:
        sys.exit(e)

    Manager(
        pages=args.number_of_pages,
        type_=args.page_type,
        seeder=args.page_seeder,
        output_path=args.output_path,
        plugins=plugins,
    ).run(args.command)


if __name__ == "__main__":
    run()
