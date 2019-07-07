from enum import Enum

from doc_mocker.seeders.basic import Seeder, BasicSeeder  # noqa: F401


class PageSeeder(Enum):
    BASIC = BasicSeeder()
