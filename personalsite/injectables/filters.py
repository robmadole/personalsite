def inject(app):
    @app.template_filter('article_date')
    def article_date(date):
        return date.strftime('%b {}, %Y'.format(date.day))
