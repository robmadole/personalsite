from personalsite.tests.testcases import MockTwitterTestCase
from personalsite.web import app
from personalsite.twitter import get_latest_tweet


class GetLatestTweetTest(MockTwitterTestCase):

    """
    Test fetching the latest tweet for my timeline.

    """
    def test_get_tweet(self):
        """
        Can get a tweet.
        """
        with app.test_request_context('/'):
            self.assertIsInstance(get_latest_tweet(app), unicode)

    def test_handles_rate_limit(self):
        """
        If we happen to be rate limited, it just gives back nothing.
        """
        with app.test_request_context('/'):
            with self.mock_rate_limit():
                self.assertEqual(get_latest_tweet(app), u'')
