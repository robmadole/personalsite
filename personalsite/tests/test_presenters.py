from unittest import TestCase
from os.path import join, dirname
from datetime import date

from personalsite.web import app
from personalsite.parser import article
from personalsite.parser import bookmark
from personalsite.tests.testcases import PersonalSiteTestCase
from personalsite.injectables.content import get_bookmarks
from personalsite.search.index import SearchIndex
from personalsite.presenters import (
    ArticleListPresenter, BookmarkListPresenter,
    BookmarkPresenter, CategoryPresenter, SearchResultPresenter, NotFound)


class ArticleListPresenterTest(TestCase):

    """
    Presenter interface to a list of articles.

    """
    def setUp(self):
        self.articles = article.loader.find(
            join(dirname(__file__), 'fixtures', 'articles'))

        self.presenter = ArticleListPresenter(self.articles)

    def test_latest_article(self):
        """
        Can get the latest article.
        """
        latest = self.presenter.latest()

        self.assertEqual(date(2001, 1, 1), latest.created_date)

    def test_by_slug(self):
        """
        Can get an article by slug.
        """
        article = self.presenter.by_slug('old')

        self.assertEqual('old', article.slug)

    def test_by_slug_not_found(self):
        """
        Getting a slug for an article that is not found.
        """
        with self.assertRaises(NotFound):
            self.presenter.by_slug('notaslug')

    def test_latest_not_found(self):
        """
        If the list of articles is empty.
        """
        self.presenter.articles = []

        with self.assertRaises(NotFound):
            self.presenter.latest()

    def test_to_list(self):
        """
        Can get a list of articles.
        """
        self.assertEqual(3, len(self.presenter.to_list()))


class BookmarkListPresenterTest(TestCase):

    """
    Presenter for a bookmarks.

    """
    def setUp(self):
        self.bookmarks = bookmark.loader.find(
            join(dirname(__file__), 'fixtures', 'bookmarks'))

        self.presenter = BookmarkListPresenter(self.bookmarks)

    def test_ordered_by_name(self):
        """
        Bookmarks are ordered alphabetically.
        """
        self.assertEqual(
            ['Apples', 'Bananas', 'Cars'],
            [i.title for i in self.presenter.to_list()])

    def test_by_category(self):
        categories = self.presenter.by_category()

        for category in categories:
            self.assertIsInstance(category, bookmark.Category)


class BookmarkPresenterTest(TestCase):

    """
    Presenter for individual bookmarks.

    """
    def setUp(self):
        self.bookmarks = bookmark.loader.find(
            join(dirname(__file__), 'fixtures', 'bookmarks'))

        self.presenter = BookmarkPresenter(
            self.bookmarks.next())

    def test_to_object(self):
        self.assertIsInstance(self.presenter.to_object(), bookmark.Bookmark)


class CategoryPresenterTest(TestCase):

    """
    Presenter for individual categories.

    """
    def setUp(self):
        self.bookmarks = bookmark.loader.find(
            join(dirname(__file__), 'fixtures', 'bookmarks'))

        self.presenter = CategoryPresenter(
            self.bookmarks.next().categories[0])

    def test_to_object(self):
        self.assertIsInstance(self.presenter.to_object(), bookmark.Category)


class SearchResultPresenterTest(PersonalSiteTestCase):

    """
    Presenter for search results.

    """

    def setUp(self):
        self.content = self.content_from_fixtures(
            app, join(dirname(__file__), 'fixtures'))

        self.content.__enter__()

    def tearDown(self):
        self.content.__exit__(None, None, None)

    def test_convert_to_plain_object(self):
        """
        Converts search results to a plain Python object.
        """
        with app.test_request_context('/'):
            results = SearchIndex(bookmarks=get_bookmarks()).search('ap')

            presenter = SearchResultPresenter(results)

            result_list = presenter.to_list()

        self.assertGreater(len(result_list), 0)
