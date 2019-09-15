import multiprocessing as mp

from pathlib import Path
from typing import Any

from .models import Page, PageType
from .seeders import Seeder, PageSeeder


class Manager:
    def __init__(self, **options: Any):
        self.output_path: Path = Path(options.get("output_path", "."))
        self.seeder: Seeder = PageSeeder[options.get("seeder")].value
        self.height, self.width = PageType[options.get("type_")].value
        self.dpi = options.get("dpi", 200)
        self.pages = options.get("pages", 1)

        self._plugins = options.get("plugins", [])

        self._commands = {"generate": self._generate}

    def _generate_page(self) -> None:
        page = Page(self.height, self.width, self.dpi)
        self.seeder.seed(page)
        for plugin in self._plugins:
            plugin.process_page(page)
        page.save(self.output_path)

    def _generate(self):
        poll = mp.Pool(mp.cpu_count() * 2)
        for _ in range(self.pages):
            poll.apply_async(self._generate_page)
        poll.close()
        poll.join()

    def run(self, command: str) -> None:
        try:
            self._commands[command]()
        except KeyError:
            raise ValueError(f"Invalid command name: {command}")
