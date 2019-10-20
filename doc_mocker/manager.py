import asyncio
import logging
import time

from pathlib import Path
from typing import Any

from doc_mocker.models.pages import EmptyPageException
from .models import Page, PageType
from .seeders import Seeder, PageSeeder

logger = logging.getLogger(__name__)


class Manager:
    def __init__(self, **options: Any):
        self.output_path: Path = Path(options.get("output_path", "."))
        seeder, *seeder_args = options.get("seeder").split(":")
        self.seeder: Seeder = PageSeeder[seeder].value(*seeder_args)
        self.height, self.width = PageType[options.get("type_")].value
        self.dpi = options.get("dpi", 200)
        self.pages = options.get("pages", 1)

        self._plugins = options.get("plugins", [])

        self._commands = {"generate": self._generate}

    async def _generate_page(self) -> None:
        page = Page(self.height, self.width, self.dpi)
        await self.seeder.seed(page)
        for plugin in self._plugins:
            plugin.process_page(page)
        try:
            await page.save(self.output_path)
        except EmptyPageException as e:
            logger.warning(e)

    def _generate(self):
        start_time = time.time()
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[self._generate_page() for _ in range(self.pages)])
        )
        logger.info(f"Total running time: {time.time() - start_time}")

    def run(self, command: str) -> None:
        try:
            self._commands[command]()
        except KeyError:
            raise ValueError(f"Invalid command name: {command}")
