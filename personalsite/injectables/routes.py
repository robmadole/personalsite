from functools import wraps

from flask import render_template, abort, request, make_response
from flask.json import jsonify

from personalsite.presenters import (
    ArticlePresenter, BookmarkPresenter, SearchResultPresenter,
    CategoryPresenter, NotFound)
from personalsite.injectables.content import (
    get_bookmarks, get_articles, get_search_index)
from personalsite.rest import uri_template

NO_CACHE_HEADERS = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': 0
}


def not_found_raise_404(func):
    """
    Returns a 404 if an article cannot be found.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            abort(404)
    return wrapper


def inject(app):
    @app.route('/')
    @not_found_raise_404
    def root():
        return render_template(
            'article_detail.html',
            article=ArticlePresenter(get_articles()).latest())

    @app.route('/articles')
    @not_found_raise_404
    def article_list():
        return render_template(
            'article_list.html',
            articles=ArticlePresenter(get_articles()).to_list())

    @app.route('/articles/<slug>')
    @not_found_raise_404
    def article_detail(slug):
        return render_template(
            'article_detail.html',
            article=ArticlePresenter(get_articles()).by_slug(slug))

    @app.route('/bookmarks')
    @not_found_raise_404
    def bookmark_list():
        return render_template(
            'bookmark_list.html',
            bookmarks=BookmarkPresenter(get_bookmarks()).to_list())

    @app.route('/bookmarks/<slug>')
    @not_found_raise_404
    def bookmark_detail(slug):
        return render_template(
            'bookmark_detail.html',
            bookmark=BookmarkPresenter(get_bookmarks()).by_slug(slug))

    @app.route('/category/<slug>')
    @not_found_raise_404
    def category_detail(slug):
        return render_template(
            'category_detail.html',
            bookmark=CategoryPresenter(get_bookmarks()).by_category(slug))

    @app.route('/bookmarks/search')
    def bookmark_search():
        links = {
            'search.categories': uri_template(
                app, category_detail={'slug': 'search.categories'})
        }

        query_string = request.args.get('q', '')

        presenter = SearchResultPresenter(
            get_search_index().search(query_string))

        return make_response(
            jsonify({
                'links': links,
                'search': presenter.to_list()
            }),
            200,
            NO_CACHE_HEADERS)
