from unittest import TestCase
from contextlib import contextmanager
from os.path import join

from flask import g, appcontext_pushed
from bs4 import BeautifulSoup
from mock import patch, Mock

from personalsite.parser import article, bookmark
from personalsite.search.index import SearchIndex


class PersonalSiteTestCase(TestCase):
    def element_by_role(self, response, role):
        """
        Get an element with a role attribute.
        """
        soup = BeautifulSoup(response.data)

        return soup.find(attrs={'role': role})

    @contextmanager
    def content_from_fixtures(self, app, fixture_directory):
        """
        Replace the application content with content from fixtures.
        """
        def handler(sender, **kwargs):
            try:
                g.articles = self.articles
            except AttributeError:
                try:
                    g.articles = list(article.loader.find(
                        join(fixture_directory, 'articles')))
                except OSError:
                    g.articles = []

            try:
                g.bookmarks = self.bookmarks
            except AttributeError:
                try:
                    g.bookmarks = list(bookmark.loader.find(
                        join(fixture_directory, 'bookmarks')))
                except OSError:
                    g.bookmarks = []

            try:
                g.search_index = self.search_index
            except AttributeError:
                g.search_index = SearchIndex(bookmarks=g.bookmarks)

        with appcontext_pushed.connected_to(handler, app):
            yield

    @contextmanager
    def content_empty(self, app):
        """
        Replace the application content with all empty values.
        """
        def handler(sender, **kwargs):
            g.articles = None
            g.bookmarks = None
            g.search_index = None

        with appcontext_pushed.connected_to(handler, app):
            yield


class LoaderTestCase(object):

    """
    Test a loader for a specific type of object.

    """
    # This is the type of object that should be created by the loader
    object_class = None

    # The loader function that is capable of finding object_class objects
    loader = None

    # This is the directory where file-based fixtures can be found
    fixture_directory = None

    def test_will_find_objects(self):
        objects = self.loader.find(self.fixture_directory)

        self.assertGreater(len(list(objects)), 0)

    def test_they_are_object_instances(self):
        objects = self.loader.find(self.fixture_directory)

        for obj in objects:
            self.assertIsInstance(obj, self.object_class)


class MockTwitterTestCase(TestCase):

    """
    Since Twitter rate limits, mock out the calls while testing.

    """
    twitter_responses = {
        '/statuses/show': {
            'user': {'profile_image_url': ''},
            'retweeted': False
        },
        '/statuses/oembed': {
            'html': u'<blockquote>Tweet</blockquote>'
        }
    }

    def _get_twitter_response(
            self, endpoint, method='GET', params=None, version='1.1'):
        return self.twitter_responses[endpoint]

    def setUp(self):
        super(MockTwitterTestCase, self).setUp()

        self.twython_patch = patch('personalsite.twitter.Twython')

        self.twitter = self.twython_mock = self.twython_patch.start()

        self.twython_mock().get_user_timeline = Mock(return_value=[{'id': 1}])
        self.twython_mock().request = Mock(
            side_effect=self._get_twitter_response)

    def tearDown(self):
        super(MockTwitterTestCase, self).tearDown()

        self.twython_patch.stop()
