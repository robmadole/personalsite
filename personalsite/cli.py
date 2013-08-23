"""
Location adder.

Usage:
  addloc <url> <category>...
  addloc --version
  addloc (-h | --help)

"""
import sys
import json
from os import listdir
from os.path import join

import yaml
import requests
from docopt import docopt

from personalsite.web import app

try:  # pragma: no cover
    from yaml import CLoader as YamlLoader
    from yaml import CDumper as YamlDumper
except ImportError:  # pragma: no cover
    from yaml import Loader as YamlLoader
    from yaml import Dumper as YamlDumper


class ParseFailed(Exception):

    """
    Parsing a URL using Readability's API failed for some reason.

    """


def parse_location(url):
    """
    Use Readability's API to parse the URL into readable content.
    """
    response = requests.get(
        app.config.get('READABILITY_PARSER_API_URL'),
        params={
            'token': app.config.get('READABILITY_PARSER_API_TOKEN'),
            'url': url
        }
    )

    if response.status_code != 200:
        raise ParseFailed(response)

    return json.loads(response.content)


def find_bookmark(categories):
    """
    Find the bookmark that owns the first category.
    """
    bookmarks_directory = app.config.get('BOOKMARKS_DIRECTORY')

    primary_category = categories[0]

    for basename in listdir(bookmarks_directory):
        filename = join(bookmarks_directory, basename)

        with open(filename) as fh:
            bookmark = yaml.load(fh, Loader=YamlLoader)

        categories = [i['slug'] for i in bookmark['categories']]

        if primary_category in categories:
            return filename, bookmark
    else:
        return None, None


def save_bookmark(filename, bookmark):
    """
    Save a bookmark with new data.
    """
    with open(filename, 'w') as fh:
        yaml.dump(
            bookmark, fh,
            indent=4,
            width=80,
            default_flow_style=False,
            Dumper=YamlDumper)


def fix_ellipsis(string):
    """
    Replaces the &hellips with an actual ellipsis.
    """
    return string.replace(u'&hellip;', u'\u2026')


def main():
    arguments = docopt(__doc__, version='Location adder 1.0')

    url = arguments.get('<url>')
    categories = arguments.get('<category>')

    filename, bookmark = find_bookmark(categories)

    if not bookmark:
        sys.stderr.write('Could not find categories {}\n'.format(categories))
        sys.exit()

    try:
        bookmark_data = parse_location(url)
    except ParseFailed:
        sys.stderr.write('Failed to parse {}\n'.format(url))

    if not 'locations' in bookmark:
        bookmark['locations'] = []

    bookmark['locations'].append({
        'categories': categories,
        'url': url,
        'title': bookmark_data['title'],
        'description': fix_ellipsis(bookmark_data['excerpt'])
    })

    save_bookmark(filename, bookmark)
