from flask import g

from personalsite.parser import article, bookmark
from personalsite.search.index import SearchIndex
from personalsite.serializer.tool import load_drivers

_articles_directory = None
_bookmarks_directory = None


def get_bookmarks():
    bookmarks = g.get('bookmarks', None)

    if bookmarks is None:
        g.bookmarks = list(bookmark.loader.find(_bookmarks_directory))

    return g.bookmarks


def get_articles():
    articles = g.get('articles', None)

    if articles is None:
        g.articles = list(article.loader.find(_articles_directory))

    return g.articles


def get_search_index():
    search_index = g.get('search_index', None)

    if search_index is None:
        g.search_index = SearchIndex(bookmarks=get_bookmarks())

    return g.search_index


def inject(app):
    global _articles_directory
    global _bookmarks_directory

    _articles_directory = app.config.get('ARTICLES_DIRECTORY')
    _bookmarks_directory = app.config.get('BOOKMARKS_DIRECTORY')

    load_drivers()
