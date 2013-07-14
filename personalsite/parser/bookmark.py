import re
from collections import defaultdict
from operator import attrgetter

import yaml

from personalsite.parser.loader import Loader
from personalsite.parser.matcher import FilenameMatcher

try:  # pragma: no cover
    from yaml import CLoader as YamlLoader
except ImportError:  # pragma: no cover
    from yaml import Loader as YamlLoader

BOOKMARK_FILENAME_PATTERN = re.compile(r'''
    (?P<slug>[^\.]+)
    \.yml''', re.VERBOSE)


class Bookmark(FilenameMatcher):

    """
    A collection of links and notes categorized by subject.

    """
    _cache_by_slug = {}

    filename_pattern = BOOKMARK_FILENAME_PATTERN

    slug = None

    def __init__(self, path):
        super(Bookmark, self).__init__(path)

        # Only read the YAML file once and then cache it
        self._object_cache = self._object

        self._categories_cache = [
            Category(i) for i in self._object_cache.get('categories', [])]
        self._locations_cache = [
            Location(i) for i in self._object_cache.get('locations', [])]

        self.__class__.cache_add(self)

    @classmethod
    def clear_cache(cls):
        """
        Remove any cached data that this or child objects use for lookup.
        """
        cls._cache_by_slug.clear()

        Category.clear_cache()
        Location.clear_cache()

    @classmethod
    def cache_add(cls, instance):
        cls._cache_by_slug[instance.slug] = instance

    @classmethod
    def lookup_by_slug(cls, slug):
        return cls._cache_by_slug[slug]

    @property
    def _object(self):
        with open(self.path) as fh:
            return yaml.load(fh, Loader=YamlLoader)

    @property
    def title(self):
        return self._object_cache.get('title', None)

    @property
    def categories(self):
        return self._categories_cache

    @property
    def locations(self):
        return self._locations_cache

loader = Loader(Bookmark)


class Category(object):

    """
    A grouping of related locations.

    """
    _cache_by_slug = {}

    def __init__(self, category):
        self._category = category
        self.name = category.get('name')
        self.slug = category.get('slug')
        self.description = category.get('description', None)

        # Cache this instance for lookup
        self.__class__.cache_add(self)

    @classmethod
    def clear_cache(cls):
        cls._cache_by_slug.clear()

    @classmethod
    def cache_add(cls, instance):
        cls._cache_by_slug[instance.slug] = instance

    @classmethod
    def lookup_by_slug(cls, slug):
        return cls._cache_by_slug[slug]

    @classmethod
    def lookup_slugs(cls, slugs):
        """
        Find categories by slug.

        :param list slugs:
        """
        return sorted(
            [cls.lookup_by_slug(i) for i in slugs],
            key=attrgetter('name'))

    @property
    def locations(self):
        return Location.lookup_by_category_slug(self.slug)


class Location(object):

    """
    A URL or other location of a resource on the Internet.

    """
    _cache_by_url = {}

    _cache_by_category_slug = defaultdict(list)

    def __init__(self, location):
        self._location = location
        self.url = location.get('url')
        self.description = location.get('description', None)

        self._categories = location.get('categories', [])

        self.__class__.cache_add(self)

    @classmethod
    def clear_cache(cls):
        cls._cache_by_url.clear()
        cls._cache_by_category_slug.clear()

    @classmethod
    def cache_add(cls, instance):
        cls._cache_by_url[instance.url] = instance

        for slug in instance._categories:
            cls._cache_by_category_slug[slug].append(instance)

    @classmethod
    def lookup_by_url(cls, url):
        return cls._cache_by_url[url]

    @classmethod
    def lookup_by_category_slug(cls, category_slug):
        return cls._cache_by_category_slug[category_slug]

    @property
    def categories(self):
        return Category.lookup_slugs(self._categories)
