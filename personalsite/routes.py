from flask import render_template, abort

from personalsite.web import app
from personalsite.parser.article import loader
from personalsite.presenters import ArticlePresenter, NotFound

articles = loader.find(app.config.get('ARTICLES_DIRECTORY'))


@app.route('/')
def root():
    return render_template(
        'article.html',
        article=ArticlePresenter(articles).latest())


@app.route('/articles')
def articles_list():
    try:
        return render_template(
            'article_list.html',
            articles=ArticlePresenter(articles))
    except NotFound:
        abort()


@app.route('/articles/<slug>')
def article_detail(slug):
    try:
        return render_template(
            'article.html',
            article=ArticlePresenter(articles).by_slug(slug))
    except NotFound:
        abort()


@app.template_filter('article_date')
def article_date(date):
    return date.strftime('%b {}, %Y'.format(date.day))
