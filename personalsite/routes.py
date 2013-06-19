from flask import render_template, abort

from personalsite.web import app
from personalsite.parser.article import loader
from personalsite.presenters import ArticlePresenter, NotFound

articles = list(loader.find(app.config.get('ARTICLES_DIRECTORY')))


@app.route('/')
def root():
    return render_template(
        'article_detail.html',
        article=ArticlePresenter(articles).latest())


@app.route('/articles')
def article_list():
    try:
        return render_template(
            'article_list.html',
            articles=ArticlePresenter(articles))
    except NotFound:
        abort(404)


@app.route('/articles/<slug>')
def article_detail(slug):
    try:
        return render_template(
            'article_detail.html',
            article=ArticlePresenter(articles).by_slug(slug))
    except NotFound:
        abort(404)


@app.template_filter('article_date')
def article_date(date):
    return date.strftime('%b {}, %Y'.format(date.day))
