from os.path import join, dirname
from unittest import TestCase

from personalsite.parser.bookmark import Bookmark, Category, Location, loader
from personalsite.tests.testcases import LoaderTestCase


class BookmarkTestCase(TestCase):

    """
    Base test case for article loader and parser tests.

    """
    def setUp(self):
        self.fixture_directory = join(
            dirname(__file__), 'fixtures', 'bookmarks')


class BookmarkLoaderTest(LoaderTestCase, BookmarkTestCase):

    """
    Bookmark loader tests.

    """
    loader = loader
    object_class = Bookmark


class BookmarkTest(BookmarkTestCase):

    """
    Bookmark data tests.

    """
    def setUp(self):
        super(BookmarkTest, self).setUp()

        self.bookmark = loader.find(self.fixture_directory).next()

    def test_get_basic_attributes(self):
        """
        Can get basic attribute.
        """
        self.assertEqual('Trucks', self.bookmark.title)
        self.assertEqual('trucks', self.bookmark.slug)

    def test_get_bookmark_by_slug(self):
        """
        Can get a bookmark by its slug.
        """
        self.assertIsInstance(
            Bookmark.lookup_by_slug('trucks'),
            Bookmark)

    def test_get_categories(self):
        """
        Can get categories.
        """
        self.assertGreater(len(self.bookmark.categories), 0)

        for category in self.bookmark.categories:
            self.assertIsInstance(category, Category)

    def test_get_category_by_slug(self):
        """
        Can get a category by its slug.
        """
        self.assertIsInstance(
            Category.lookup_by_slug('yellow-ones'),
            Category)

    def test_get_locations(self):
        """
        Can get locations.
        """
        for location in self.bookmark.locations:
            self.assertIsInstance(location, Location)

        if not self.bookmark.locations:
            self.fail('No locations found')

    def test_get_location_by_url(self):
        """
        Can get a location by its URL.
        """
        self.assertIsInstance(
            Location.lookup_by_url('http://oldtrucks.com/truck1.jpg'),
            Location)

    def test_category_attributes(self):
        """
        Attributes on the category.
        """
        category = self.bookmark.categories[0]

        self.assertEqual('Yellow ones', category.name)
        self.assertEqual('yellow-ones', category.slug)
        self.assertEqual(
            'Information about yellow trucks',
            category.description)

    def test_category_location_relationship(self):
        """
        Category has a lookup relationship to Location objects.
        """
        category = Category.lookup_slugs(['old-ones'])[0]

        for location in category.locations:
            self.assertIsInstance(location, Location)

        if not category.locations:
            self.fail('No locations found')

    def test_location_attributes(self):
        """
        Attributes on the location.
        """
        location = self.bookmark.locations[0]

        self.assertTrue(location.url)
        self.assertTrue(location.categories)
        self.assertTrue(location.description)

    def test_location_category_relationship(self):
        """
        Location has a lookup relationship to Category objects.
        """
        location = self.bookmark.locations[0]

        for category in location.categories:
            self.assertIsInstance(category, Category)

        if not location.categories:
            self.fail('No categories found')
