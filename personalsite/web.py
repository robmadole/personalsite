from flask import Flask

from personalsite.injector import Injector, Injectables

app = Flask(__name__)
app.config.from_object('personalsite.settings.base')
app.config.from_envvar('PERSONALSITE_SETTINGS_FILE')


class Personalsite(Injector):
    namespace = 'personalsite.injectables'

    injectables = Injectables(
        'routes.inject',
        'assets.inject',
        'filters.inject',
        'content.inject',
        'errorhandlers.inject',
        'cache.inject'
    )

site = Personalsite(app)
