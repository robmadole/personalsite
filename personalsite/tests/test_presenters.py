from unittest import TestCase
from os.path import join, dirname
from datetime import date

from personalsite.parser import article
from personalsite.parser import bookmark
from personalsite.presenters import (
    ArticlePresenter, BookmarkPresenter, NotFound)


class ArticlePresenterTestCase(TestCase):

    """
    Presenter interface to a list of articles.

    """
    def setUp(self):
        self.articles = article.loader.find(
            join(dirname(__file__), 'fixtures', 'articles'))

        self.presenter = ArticlePresenter(self.articles)

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


class BookmarkPresenterTestCase(TestCase):

    """
    Presenter for a bookmakrs.

    """
    def setUp(self):
        self.bookmarks = bookmark.loader.find(
            join(dirname(__file__), 'fixtures', 'bookmarks'))

        self.presenter = BookmarkPresenter(self.bookmarks)

    def test_ordered_by_name(self):
        """
        Bookmarks are ordered alphabetically.
        """
        self.assertEqual(
            ['Apples', 'Bananas', 'Cars'],
            [i.title for i in self.presenter.to_list()])
