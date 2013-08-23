from flask import render_template


def inject(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', exception=e), 404
