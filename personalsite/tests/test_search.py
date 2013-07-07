from os.path import join, dirname
from unittest import TestCase

from personalsite.parser import bookmark
from personalsite.search import SearchIndex


class SearchTest(TestCase):
    def setUp(self):
        self.bookmarks = list(bookmark.loader.find(
            join(dirname(__file__), 'fixtures', 'bookmarks')))

        self.index = SearchIndex(bookmarks=self.bookmarks)

    def test_can_find_bookmark_results(self):
        with self.index.search(query_string='apple') as results:
            if len(results) == 0:
                self.fail('No results found')

            for result in results:
                self.assertIsInstance(
                    result,
                    [Bookmark, Category, Location])
