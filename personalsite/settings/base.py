from os.path import join, dirname, realpath

from personalsite.settings.utils import from_env

ARTICLES_DIRECTORY = realpath(
    join(dirname(__file__), '..', '..', 'articles'))

BOOKMARKS_DIRECTORY = realpath(
    join(dirname(__file__), '..', '..', 'bookmarks'))

ASSETS_DIRECTORY_NAME = 'bundles'

PARSED_CONTENT_CACHE = realpath(
    join(dirname(__file__), '..', '..', '.locationcache'))

READABILITY_PARSER_API_URL = 'https://readability.com/api/content/v1/parser'
READABILITY_PARSER_API_TOKEN = 'c9d607f73c74cc092e19af6a121b2e942b59c469'

TWITTER_CONSUMER_KEY = 'KLDwUI17b8GZq3mhuU6Ug'
TWITTER_CONSUMER_SECRET = from_env('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = '3013231-5fVLbIrqVEThyzI5XGio3PyIe6PSfgRbt9k1CxfJQ'
TWITTER_ACCESS_TOKEN_SECRET = from_env('TWITTER_ACCESS_TOKEN_SECRET')

TWITTER_CACHE_TIMEOUT = 60 * 60
