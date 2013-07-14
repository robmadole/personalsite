from unittest import TestCase
from os.path import join, dirname

from personalsite.parser import bookmark
from personalsite.serializer.tool import load_drivers, serialize


class DriversTest(TestCase):
    def setUp(self):
        load_drivers()

        self.bookmarks = bookmark.loader.find(
            join(dirname(__file__), 'fixtures', 'bookmarks'))

    def test_bookmark_serializer(self):
        bookmark = self.bookmarks.next()

        serialized = serialize(bookmark)

        self.assertEqual('bookmark', serialized['type'])
        self.assertEqual(bookmark.slug, serialized['id'])
        self.assertEqual(bookmark.slug, serialized['slug'])
        self.assertEqual(bookmark.title, serialized['title'])
        self.assertEqual(
            [i.slug for i in bookmark.categories],
            serialized['categories'])

    def test_category_serializer(self):
        category = self.bookmarks.next().categories[0]

        serialized = serialize(category)

        self.assertEqual('category', serialized['type'])
        self.assertEqual(category.slug, serialized['id'])
        self.assertEqual(category.slug, serialized['slug'])
        self.assertEqual(category.name, serialized['name'])
        self.assertEqual(category.description, serialized['description'])
        self.assertEqual(
            [i.url for i in category.locations],
            serialized['locations'])

    def test_location_serializer(self):
        location = self.bookmarks.next().locations[0]

        serialized = serialize(location)

        self.assertEqual('location', serialized['type'])
        self.assertEqual(location.url, serialized['id'])
        self.assertEqual(location.url, serialized['slug'])
        self.assertEqual(location.url, serialized['url'])
        self.assertEqual(location.url, serialized['href'])
        self.assertEqual(location.description, serialized['description'])
        self.assertEqual(
            [i.slug for i in location.categories],
            serialized['categories'])
