import imp
from os import listdir
from os.path import join, dirname

_drivers = {}


def load_drivers():
    _drivers.clear()

    drivers_path = join(dirname(__file__), 'drivers')
    for filename in listdir(drivers_path):
        if filename.startswith('__'):
            continue

        driver_name = filename.replace('.py', '')
        imp.load_source(
            '{}.{}'.format(__name__, driver_name),
            join(drivers_path, filename)
        )

    return _drivers


def register_for(object_type):
    def wrapper(serializer):
        _drivers[object_type] = serializer
    return wrapper


def serialize(instance):
    return _drivers[instance.__class__](instance).serialize()
