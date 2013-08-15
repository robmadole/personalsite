from os.path import join, dirname
from contextlib import nested

from mock import patch

from personalsite.tests.testcases import PersonalSiteTestCase
from personalsite.web import app
from personalsite.injectables.content import (
    get_articles, get_bookmarks, get_search_index, get_bookmark_lookup)
from personalsite.parser.bookmark import Bookmark, Category, Location


class ContentTest(PersonalSiteTestCase):

    """
    Content injectable tests.

    """
    def setUp(self):
        self.client = app.test_client()

        self.content = self.content_empty(app)

        self.content.__enter__()

    def tearDown(self):
        self.content.__exit__(None, None, None)

    def test_missing_content_initializes_from_config(self):
        """
        Missing content will initialize using the app config.
        """
        with app.test_request_context('/'):
            self.assertTrue(get_articles())
            self.assertTrue(get_bookmarks())
            self.assertTrue(get_search_index())

    def test_caches_the_content(self):
        """
        Repeated calls to get content are cached.
        """
        def assert_called_once(*mocks):
            self.assertTrue(
                all([i.call_count == 1 for i in mocks]))

        with nested(
            patch('personalsite.injectables.content.bookmark'),
            patch('personalsite.injectables.content.article'),
            patch('personalsite.injectables.content.SearchIndex')
        ) as (bookmark, article, SearchIndex):
            with app.test_request_context('/'):
                # Call it once to initialize the cache
                get_articles()
                get_bookmarks()
                get_search_index()

                assert_called_once(
                    bookmark.loader.find,
                    article.loader.find,
                    SearchIndex)

                # Call them a second time, these should be cached
                get_bookmarks()
                get_articles()
                get_search_index()

                # It still has only been called once
                assert_called_once(
                    bookmark.loader.find,
                    article.loader.find,
                    SearchIndex)


class LookupTest(PersonalSiteTestCase):

    """
    Lookup functions for content.

    """
    def setUp(self):
        self.content = self.content_from_fixtures(
            app, join(dirname(__file__), '..', '..', 'tests', 'fixtures'))

        self.content.__enter__()

    def tearDown(self):
        self.content.__exit__(None, None, None)

    def test_lookups(self):
        """
        Test bookmark, category, and location lookups.
        """
        with app.test_request_context('/'):
            self.assertIsInstance(
                get_bookmark_lookup().bookmark('apples'),
                Bookmark)

            self.assertIsInstance(
                get_bookmark_lookup().category('apples-green'),
                Category)

            self.assertIsInstance(
                get_bookmark_lookup().location('http://apples.com/tasty1.jpg'),
                Location)
