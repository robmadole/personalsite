from flask.ext.assets import Environment, Bundle


def inject(app):
    output_directory = app.config.get('ASSETS_DIRECTORY_NAME')

    assets = assets = Environment(app)

    assets.register(
        'core_js',
        Bundle(
            'jquery/jquery.js',
            'underscore/underscore.js',
            'backbone/backbone.js',
            'handlebars/dist/handlebars.js',
            filters='uglifyjs',
            output='{}/core.js'.format(output_directory)))

    assets.register(
        'personalsite_templates',
        Bundle(
            'personalsite/app/**/templates/*.html',
            filters='handlebars',
            output='{}/personalsite_templates.js'.format(output_directory)))

    assets.register(
        'personalsite_js',
        Bundle(
            'personalsite/app/**/*Model.coffee',
            'personalsite/app/**/*Collection.coffee',
            'personalsite/app/**/*View.coffee',
            'personalsite/app/**/*Controller.coffee',
            filters='coffeescript',
            output='{}/personalsite.js'.format(output_directory)))

    assets.register(
        'personalsite_css',
        Bundle(
            'personalsite/less/screen.less',
            filters='less',
            output='{}/personalsite.css'.format(output_directory)))
