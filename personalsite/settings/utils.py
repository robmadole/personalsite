from os import environ


def from_env(name):
    """
    Get an environment variable or raise a RuntimeError.

    :param string name:
    """
    if name not in environ:
        raise RuntimeError('Could not find environment variable {}'.format(
            name))
    return environ.get(name)
