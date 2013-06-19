import re
import datetime
from os.path import basename

from personalsite.parser.loader import Loader
from personalsite.parser.meta import separate_meta

ARTICLE_FILENAME_PATTERN = re.compile(r'''
    (?P<year>\d{4})
    \-
    (?P<month>\d{2})
    \-
    (?P<day>\d{2})
    \-(?P<slug>[^\.]+)
    \.html''', re.VERBOSE)


class Article(object):

    """
    A written article containing meta data and an HTML snippet.

    """
    def __init__(self, path):
        self.path = path
        self.basename = basename(path)

        match = ARTICLE_FILENAME_PATTERN.match(self.basename)

        if not match:
            raise ValueError('Invalid filename {}'.format(self.basename))

        parts = match.groupdict()

        self.year = int(parts['year'])
        self.month = int(parts['month'])
        self.day = int(parts['day'])
        self.slug = parts['slug']

        # We will store article contents in here
        self._content_cache = None

    @property
    def created_date(self):
        """
        When the article was created.
        """
        return datetime.date(year=self.year, month=self.month, day=self.day)

    def read_and_separate(self):
        """
        Read the file and cache the meta and body.

        :returns: (meta, body)
        :rtype: tuple
        """
        if not self._content_cache:
            with open(self.path) as fh:
                self._content_cache = separate_meta(fh)

        return self._content_cache

    @property
    def meta(self):
        """
        Meta information about the article, usually title and teaser.

        :rtype: dict or list
        """
        return self.read_and_separate()[0]

    @property
    def body(self):
        """
        Body of the article.

        :rtype: str
        """
        return self.read_and_separate()[1]

loader = Loader(Article)
