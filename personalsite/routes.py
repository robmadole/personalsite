from functools import wraps

from flask import render_template, abort

from personalsite.web import app
from personalsite.parser import article, bookmark
from personalsite.presenters import (
    ArticlePresenter, BookmarkPresenter, NotFound)

articles = list(article.loader.find(
    app.config.get('ARTICLES_DIRECTORY')))

bookmarks = list(bookmark.loader.find(
    app.config.get('BOOKMARKS_DIRECTORY')))


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


@app.route('/')
@not_found_raise_404
def root():
    return render_template(
        'article_detail.html',
        article=ArticlePresenter(articles).latest())


@app.route('/articles')
@not_found_raise_404
def article_list():
    return render_template(
        'article_list.html',
        articles=ArticlePresenter(articles).to_list())


@app.route('/articles/<slug>')
@not_found_raise_404
def article_detail(slug):
    return render_template(
        'article_detail.html',
        article=ArticlePresenter(articles).by_slug(slug))


@app.route('/bookmarks')
@not_found_raise_404
def bookmark_list():
    return render_template(
        'bookmark_list.html',
        bookmarks=BookmarkPresenter(bookmarks).to_list())


@app.route('/bookmarks/search')
def bookmark_search():
    pass


@app.route('/bookmarks/<slug>')
@not_found_raise_404
def bookmark_detail(slug):
    return render_template(
        'bookmark_detail.html',
        bookmark=BookmarkPresenter(bookmarks).by_slug(slug))


@app.template_filter('article_date')
def article_date(date):
    return date.strftime('%b {}, %Y'.format(date.day))
