from unittest import TestCase

from personalsite.tests.testcases import MockTwitterTestCase
from personalsite.web import app
from personalsite.twitter import get_latest_tweet


class GetLatestTweetTest(MockTwitterTestCase):

    """
    Test fetching the latest tweet for my timeline.

    """
    def test_get_tweet(self):
        with app.test_request_context('/'):
            self.assertIsInstance(get_latest_tweet(app), unicode)
