from flask import current_app

from personalsite.parser import article, bookmark
from personalsite.search.index import SearchIndex
from personalsite.serializer.tool import load_drivers


def get_articles():
    return current_app.articles


def get_search_index():
    return current_app.search_index


def get_bookmarks():
    return current_app.bookmarks


def get_bookmark_lookup():
    # Load the bookmarks if they are not available
    get_bookmarks()

    _bookmark = bookmark

    class lookup:
        bookmark = _bookmark.Bookmark.lookup_by_slug
        category = _bookmark.Category.lookup_by_slug
        location = _bookmark.Location.lookup_by_url

    return lookup


def init_content(app, articles_directory, bookmarks_directory):
    app.articles = list(article.loader.find(articles_directory))
    app.bookmarks = list(bookmark.loader.find(bookmarks_directory))
    app.search_index = SearchIndex(bookmarks=app.bookmarks)


def inject(app):
    global _articles_directory
    global _bookmarks_directory

    load_drivers()

    init_content(
        app,
        app.config.get('ARTICLES_DIRECTORY'),
        app.config.get('BOOKMARKS_DIRECTORY')
    )
