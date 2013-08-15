class Injectables(object):

    """
    A list of callable objects that will receive an app injection.

    """
    def __init__(self, *args):
        self.to_inject = args

    def inject_all(self, app, namespace=''):
        for injectable in self.to_inject:
            fullname = '{}.{}'.format(namespace, injectable)

            module_name, to_call = fullname.rsplit('.', 1)

            module = __import__(module_name, globals(), locals(), [to_call], 0)

            getattr(module, to_call)(app)


class Injector(object):

    """
    Implementation of dependency injection for a Flask application.

    """
    namespace = ''

    injectables = Injectables()

    def __init__(self, app):
        self.app = app

        self.injectables.inject_all(self.app, self.namespace)
