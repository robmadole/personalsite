from os.path import join, dirname

from personalsite.tests.testcases import PersonalSiteTestCase
from personalsite.web import app
from personalsite import routes
from personalsite.parser.article import loader


class ViewTest(PersonalSiteTestCase):
    def setUp(self):
        self._original_articles = routes.articles

        routes.articles = loader.find(
            join(dirname(__file__), 'fixtures', 'articles'))

        self.app = app.test_client()

    def tearDown(self):
        routes.articles = self._original_articles

    def test_entry_page_latest_article(self):
        """
        Get the latest article.
        """
        response = self.app.get('/')

        self.assertEqual(200, response.status_code)

        self.assertEqual(
            'Jan 1, 2001',
            self.element_by_handle(response, 'article_date').text)

    def test_by_slug(self):
        """
        Get article by slug.
        """
        response = self.app.get('/articles/old')

        self.assertEqual(200, response.status_code)

    def test_by_slug_not_found(self):
        """
        Article by slug not found.
        """
        response = self.app.get('/articles/notaslug')

        self.assertEqual(404, response.status_code)
