from os.path import join, dirname

from personalsite.tests.testcases import PersonalSiteTestCase
from personalsite.web import app
from personalsite import routes
from personalsite.parser import article, bookmark


class ViewTest(PersonalSiteTestCase):
    def setUp(self):
        self._original_articles = routes.articles
        self._original_bookmarks = routes.bookmarks

        routes.articles = article.loader.find(
            join(dirname(__file__), 'fixtures', 'articles'))

        routes.bookmarks = bookmark.loader.find(
            join(dirname(__file__), 'fixtures', 'bookmarks'))

        self.app = app.test_client()

    def tearDown(self):
        routes.articles = self._original_articles
        routes.bookmarks = self._original_bookmarks

    def test_entry_page_latest_article(self):
        """
        Get the latest article.
        """
        response = self.app.get('/')

        self.assertEqual(200, response.status_code)

        self.assertEqual(
            'Jan 1, 2001',
            self.element_by_role(response, 'article-date').text)

    def test_article_list(self):
        """
        List of articles.
        """
        response = self.app.get('/articles')

        self.assertEqual(200, response.status_code)

    def test_no_articles(self):
        """
        If no articles are available.
        """
        routes.articles = []

        response = self.app.get('/')

        self.assertEqual(404, response.status_code)

    def test_article_by_slug(self):
        """
        Get article by slug.
        """
        response = self.app.get('/articles/old')

        self.assertEqual(200, response.status_code)

    def test_article_by_slug_not_found(self):
        """
        Article by slug not found.
        """
        response = self.app.get('/articles/notaslug')

        self.assertEqual(404, response.status_code)

    def test_bookmark_list(self):
        """
        List of bookmarks.
        """
        response = self.app.get('/bookmarks')

        self.assertEqual(200, response.status_code)
