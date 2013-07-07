import datetime
from os.path import join, dirname
from unittest import TestCase

from personalsite.parser.article import Article, loader
from personalsite.tests.testcases import LoaderTestCase


class ArticleTestCase(TestCase):

    """
    Base test case for article loader and parser tests.

    """
    def setUp(self):
        self.fixture_directory = join(
            dirname(__file__), 'fixtures', 'articles')


class ArticleLoaderTest(LoaderTestCase, ArticleTestCase):

    """
    Article loader tests.

    """
    loader = loader
    object_class = Article


class ArticleTest(ArticleTestCase):

    """
    Article parser provides access to an individual article.

    """
    def setUp(self):
        super(ArticleTest, self).setUp()

        self.article = loader.find(self.fixture_directory).next()

    def test_article_date_and_slug_information(self):
        """
        Parses the date and slug from the filename.
        """
        article = Article('/some/path/2000-01-02-slug.html')

        self.assertEqual(2000, article.year)
        self.assertEqual(1, article.month)
        self.assertEqual(2, article.day)
        self.assertEqual('slug', article.slug)

    def test_article_created_date(self):
        """
        A datetime.date is created from the date information.
        """
        article = Article('/some/path/2000-01-02-slug.html')

        self.assertEqual(article.created_date, datetime.date(2000, 1, 2))

    def test_article_bad_filename(self):
        """
        Bad file names raise an exception.
        """
        with self.assertRaises(ValueError):
            Article('/some/path/bad-filename-111.html')

    def test_article_front_matter(self):
        """
        Will parse the front matter.
        """
        self.assertTrue(self.article.meta)

    def test_article_body(self):
        """
        Will parse the body.
        """
        self.assertTrue(self.article.body)
