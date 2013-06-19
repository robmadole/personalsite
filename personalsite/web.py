from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config.from_object('personalsite.settings.base')
app.config.from_envvar('PERSONALSITE_SETTINGS_FILE')

assets = Environment(app)

assets.register(
    'core_js',
    Bundle(
        'jquery/jquery.js',
        filters='closure_js',
        output='bundles/core.js'))

assets.register(
    'personalsite_css',
    Bundle(
        'personalsite/less/screen.less',
        filters='less',
        output='bundles/personalsite.css'))
