from enum import Enum

from doc_mocker.seeders.basic import Seeder, BasicSeeder  # noqa: F401
from doc_mocker.seeders.wikipedia import Wikipedia


class PageSeeder(Enum):
    basic = BasicSeeder
    wikipedia = Wikipedia
