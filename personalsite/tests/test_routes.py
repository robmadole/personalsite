import json
from os.path import join, dirname

from personalsite.tests.testcases import (
    PersonalSiteTestCase, MockTwitterTestCase)
from personalsite.web import app


class ViewTest(PersonalSiteTestCase, MockTwitterTestCase):
    def setUp(self):
        super(ViewTest, self).setUp()

        self.client = app.test_client()

        self.content = self.content_from_fixtures(
            app, join(dirname(__file__), 'fixtures'))

        self.content.__enter__()

    def tearDown(self):
        super(ViewTest, self).tearDown()

        self.content.__exit__(None, None, None)

    def test_entry_page_latest_article(self):
        """
        Get the latest article.
        """
        response = self.client.get('/')

        self.assertEqual(200, response.status_code)

        self.assertEqual(
            'Jan 1, 2001',
            self.element_by_role(response, 'article-date').text)

    def test_article_list(self):
        """
        List of articles.
        """
        response = self.client.get('/articles')

        self.assertEqual(200, response.status_code)

    def test_no_articles(self):
        """
        If no articles are available.
        """
        self.articles = []

        response = self.client.get('/')

        self.assertEqual(404, response.status_code)

    def test_article_by_slug(self):
        """
        Get article by slug.
        """
        response = self.client.get('/articles/old')

        self.assertEqual(200, response.status_code)

    def test_article_by_slug_not_found(self):
        """
        Article by slug not found.
        """
        response = self.client.get('/articles/notaslug')

        self.assertEqual(404, response.status_code)

    def test_bookmark_list(self):
        """
        List of bookmarks.
        """
        response = self.client.get('/bookmarks')

        self.assertEqual(200, response.status_code)

    def test_bookmark_detail(self):
        """
        Specific bookmark.
        """
        response = self.client.get('/bookmarks/apples')

        self.assertEqual(200, response.status_code)

    def test_category_detail(self):
        """
        Specific category.
        """
        response = self.client.get('/categories/apples-green')

        self.assertEqual(200, response.status_code)

    def test_search_keyword(self):
        """
        Search for a bookmark.
        """
        response = self.client.get('/bookmarks/search?q=ap')

        data = json.loads(response.data)

        self.assertIn('search', data)
