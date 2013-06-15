from flask import render_template

from personalsite.web import app


@app.route("/")
def root():
    return render_template('base.html')


@app.route("/article/<slug>")
def article(slug):
    return render_template('article.html')
