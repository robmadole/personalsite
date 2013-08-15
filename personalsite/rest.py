from urlparse import urljoin

from flask import request


def uri_template(app, **kwargs):
    """
    Convert Flask URL mapped Rules into URI templates.

    Only one keyword argument is allowed. This function will map the key to
    a Flask route and the value will be a map of parameters to convert
    Flask paramaters to URI template variables.

    :param flask.Flask app: Flask application object
    """
    assert len(kwargs) == 1

    endpoint = kwargs.keys()[0]
    parameters = kwargs.values()[0]

    for url in app.url_map.iter_rules():
        if url.endpoint == endpoint:
            break
    else:
        return ''

    ut = url.rule

    for param, replacement in parameters.items():
        ut = ut.replace(
            '<{}>'.format(param), '{' + replacement + '}')

    return urljoin(request.url_root, ut)
