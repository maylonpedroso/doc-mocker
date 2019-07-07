from unittest import TestCase

from doc_mocker.fonts import Arial
from doc_mocker.models import Page, PageType, Text


class PageTestCase(TestCase):
    def test_page_get_descriptors(self):
        page = Page(254, 508, 100)
        self.assertEqual(page.height_inches, 10)
        self.assertEqual(page.width_inches, 20)

    def test_page_set_descriptors(self):
        page = Page(*PageType.A4.value, 200)

        page.height_inches = 10
        page.width_inches = 20

        self.assertEqual(page.height, 254)
        self.assertEqual(page.width, 508)

    def test_write(self):
        page = Page(*PageType.A4.value, 200)

        page.write(Text("Text to write"), Arial(10))

        # TODO: assert page changed
