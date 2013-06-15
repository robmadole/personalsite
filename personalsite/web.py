from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)

assets.register(
    'core_js',
    Bundle(
        'jquery/js/jquery.js',
        filters='closure_js',
        output='bundles/core.js'))

assets.register(
    'core_css',
    Bundle(
        'bootstrap/css/bootstrap.css',
        'fontawesome/css/font-awesome.css',
        filters='yui_css',
        output='bundles/core.css'))

assets.register(
    'personalsite_css',
    Bundle(
        'personalsite/less/screen.less',
        filters='less',
        output='bundles/personalsite.css'))
