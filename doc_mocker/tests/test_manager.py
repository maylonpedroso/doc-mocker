from unittest import TestCase
from unittest.mock import patch

from doc_mocker.manager import Manager
from doc_mocker.models import PageType
from doc_mocker.seeders import PageSeeder


class ManagerTests(TestCase):

    MANAGER_OPTIONS = {"seeder": PageSeeder.BASIC.name, "type_": PageType.A4.name}

    def test_run_invalid_command(self) -> None:
        with self.assertRaises(ValueError):
            Manager(**self.MANAGER_OPTIONS).run("invalid_command")

    def test_run_generate_command(self) -> None:
        with patch("doc_mocker.manager.Manager._generate") as generate:
            Manager(**self.MANAGER_OPTIONS).run("generate")
            generate.assert_called_once()
