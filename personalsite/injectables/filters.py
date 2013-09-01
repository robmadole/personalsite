from jinja2.utils import Markup

from personalsite.twitter import get_latest_tweet


def inject(app):
    @app.template_filter('article_date')
    def article_date(date):
        return date.strftime('%b {}, %Y'.format(date.day))

    @app.context_processor
    def utility_processor():
        twitter_cache_timeout = app.config.get('TWITTER_CACHE_TIMEOUT')

        @app.cache.cached(
            timeout=twitter_cache_timeout,
            key_prefix='get_latest_tweet'
        )
        def get_latest_tweet_safe():
            return Markup(get_latest_tweet(app))

        return {
            'latest_tweet': get_latest_tweet_safe
        }
