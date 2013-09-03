from os.path import join, dirname

from personalsite.tests.testcases import PersonalSiteTestCase
from personalsite.web import app
from personalsite.injectables.content import get_bookmark_lookup
from personalsite.parser.bookmark import Bookmark, Category, Location


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
