from flask.ext.cache import Cache


def inject(app):
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    app.cache = cache
