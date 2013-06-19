import re

import yaml

META_SEPARATOR_PATTERN = re.compile(r'''
    ^\s*(?:---)
    (.*)
    (?:---)
    (.*)$''', re.VERBOSE | re.MULTILINE | re.DOTALL)


def separate_meta(fileobject):
    """
    Separates the YAML front matter from the body of a file-like object.

    If the file does not contain a YAML section the body is returned.

    When returning the separated contents, a string strip() operation will be
    performed to clean up the results a bit.

    :returns: (object, body) where the object is a dict or list converted from
        the string contents of the front matter using a YAML processor
    :rtype: tuple
    """
    contents = fileobject.read()

    match = META_SEPARATOR_PATTERN.match(contents)

    if not match:
        return None, contents
    else:
        groups = match.groups()

        return yaml.load(groups[0]), groups[1].strip()
