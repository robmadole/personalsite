from os.path import join, dirname, realpath

ARTICLES_DIRECTORY = realpath(
    join(dirname(__file__), '..', '..', 'articles'))

BOOKMARKS_DIRECTORY = realpath(
    join(dirname(__file__), '..', '..', 'bookmarks'))

ASSETS_DIRECTORY_NAME = 'bundles'

PARSED_CONTENT_CACHE = realpath(
    join(dirname(__file__), '..', '..', '.locationcache'))

READABILITY_PARSER_API_URL = 'https://readability.com/api/content/v1/parser'
READABILITY_PARSER_API_TOKEN = 'c9d607f73c74cc092e19af6a121b2e942b59c469'
