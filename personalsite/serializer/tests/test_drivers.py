from os.path import join, dirname

from personalsite.web import app
from personalsite.tests.testcases import PersonalSiteTestCase
from personalsite.serializer.tool import serialize
from personalsite.injectables.content import get_bookmarks


class DriversTest(PersonalSiteTestCase):
    def setUp(self):
        self.content = self.content_from_fixtures(
            app, join(dirname(__file__), 'fixtures'))

        self.content.__enter__()

    def tearDown(self):
        self.content.__exit__(None, None, None)

    def test_bookmark_serializer(self):
        with app.test_request_context('/'):
            bookmark = get_bookmarks()[0]

            serialized = serialize(bookmark)

        self.assertEqual('bookmark', serialized['type'])
        self.assertEqual(bookmark.slug, serialized['id'])
        self.assertEqual(bookmark.slug, serialized['slug'])
        self.assertEqual(bookmark.title, serialized['title'])
        self.assertEqual(
            [i.slug for i in bookmark.categories],
            serialized['links']['categories'])

    def test_category_serializer(self):
        with app.test_request_context('/'):
            category = get_bookmarks()[0].categories[0]

            serialized = serialize(category)

        self.assertEqual('category', serialized['type'])
        self.assertEqual(category.slug, serialized['id'])
        self.assertEqual(category.slug, serialized['slug'])
        self.assertEqual(category.name, serialized['name'])
        self.assertEqual(category.description, serialized['description'])
        self.assertEqual(
            [i.url for i in category.locations],
            serialized['links']['locations'])

    def test_location_serializer(self):
        with app.test_request_context('/'):
            location = get_bookmarks()[0].locations[0]

            serialized = serialize(location)

        self.assertEqual('location', serialized['type'])
        self.assertEqual(location.url, serialized['id'])
        self.assertEqual(location.url, serialized['slug'])
        self.assertEqual(location.url, serialized['url'])
        self.assertEqual(location.url, serialized['href'])
        self.assertEqual(location.description, serialized['description'])
        self.assertEqual(
            [i.slug for i in location.categories],
            serialized['links']['categories'])
