from flask import render_template
from twython import Twython
from twython.exceptions import TwythonRateLimitError


def get_latest_tweet(app):
    """
    Get the latest tweet in HTML format adding the user profile image.

    :param Flask app:
    :rtype: unicode
    """
    twitter = Twython(
        app.config.get('TWITTER_CONSUMER_KEY'),
        app.config.get('TWITTER_CONSUMER_SECRET'),
        app.config.get('TWITTER_ACCESS_TOKEN'),
        app.config.get('TWITTER_ACCESS_TOKEN_SECRET')
    )

    # Latest tweet
    try:
        user_timeline = twitter.get_user_timeline()

        latest_id = user_timeline[0]['id']

        tweet_response = twitter.request(
            '/statuses/show', params={
                'id': latest_id
            }
        )

        oembed_response = twitter.request(
            '/statuses/oembed', params={
                'id': latest_id,
                'hide_media': False,
                'hide_thread': True,
                'omit_script': True
            }
        )
    except TwythonRateLimitError:
        return u''

    return render_template(
        'latest_tweet.html',
        tweet=tweet_response,
        oembed=oembed_response
    )
