from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config.from_object('personalsite.settings.base')
app.config.from_envvar('PERSONALSITE_SETTINGS_FILE')

OUTPUT_DIRECTORY = 'bundles'

assets = Environment(app)

assets.register(
    'core_js',
    Bundle(
        'jquery/jquery.js',
        'underscore/underscore.js',
        'backbone/backbone.js',
        'handlebars/js/backbone.js',
        filters='uglifyjs',
        output='{}/core.js'.format(OUTPUT_DIRECTORY)))

assets.register(
    'personalsite_templates',
    Bundle(
        'personalsite/app/**/templates/*.html',
        filters='handlebars',
        output='{}/personalsite_templates.js'.format(OUTPUT_DIRECTORY)))

assets.register(
    'personalsite_js',
    Bundle(
        'personalsite/app/**/*.coffee',
        filters='coffeescript',
        output='{}/personalsite.js'.format(OUTPUT_DIRECTORY)))

assets.register(
    'personalsite_css',
    Bundle(
        'personalsite/less/screen.less',
        filters='less',
        output='{}/personalsite.css'.format(OUTPUT_DIRECTORY)))
