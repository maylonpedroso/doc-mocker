import asyncio
import logging
import random
import wikipedia

from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterator, Generator

from wikipedia import DisambiguationError

from ..models import Page, Text, TextType
from .basic import Seeder

loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor()

logger = logging.getLogger(__name__)


class Wikipedia(Seeder):
    arg_name = "wikipedia[:keyword]"

    def __init__(self, keyword: str = "computer science", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pages_index = self.search_pages(keyword)
        self.pending_pages = len(self.pages_index)
        random.shuffle(self.pages_index)
        self.contents: deque = deque()
        self.seeding = 0

    @staticmethod
    def search_pages(keyword: str) -> List[str]:
        return wikipedia.search(keyword, results=100)

    @staticmethod
    async def get_page_data(title: str) -> wikipedia.WikipediaPage:
        logger.info(f"Pulling [{title}] page data")
        return await loop.run_in_executor(executor, wikipedia.page, title)

    @staticmethod
    def process_page(data: wikipedia.WikipediaPage) -> Generator[Text, None, None]:
        yield Text(data.title, TextType.TITLE)
        current_text = ""
        for line in data.content.split("\n"):
            line = line.strip()
            if line.startswith("==") and line.endswith("=="):
                if current_text:
                    yield Text(current_text)
                    current_text = ""
                yield Text(line.strip("="), TextType.SUBTITLE)
            elif line:
                current_text += f"\n{line.strip()}"
            else:
                if current_text:
                    yield Text(current_text)
                    current_text = ""
        if current_text:
            yield Text(current_text)

    async def get_next_content(self) -> Iterator:
        if not self.contents and self.pages_index:
            try:
                page = await self.get_page_data(self.pages_index.pop())
            except DisambiguationError as e:
                logger.warning(e)
            else:
                self.contents.append(self.process_page(page))
            finally:
                self.pending_pages -= 1

        while not self.contents and (self.pending_pages or self.seeding):
            await asyncio.sleep(0.5)

        return self.contents.popleft() if self.contents else None

    async def seed(self, page: Page) -> None:
        wiki_content = await self.get_next_content()
        logger.info(f"Start seeding {page}")
        self.seeding += 1
        logger.debug(f"Currently seeding {self.seeding} pages")
        while not page.is_full and wiki_content is not None:
            try:
                text = next(wiki_content)
            except StopIteration:
                if page.is_empty:
                    wiki_content = await self.get_next_content()
                else:
                    wiki_content = None
            else:
                await page.write(text, self.font)
        if wiki_content:
            self.contents.appendleft(wiki_content)
        self.seeding -= 1
        logger.debug(f"Currently seeding {self.seeding} pages")
        logger.info(f"Done seeding {page}")
