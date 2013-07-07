from operator import attrgetter
from collections import defaultdict


class NotFound(Exception):

    """
    Raise when an article cannot be found.

    """
    pass


class ArticlePresenter(object):

    """
    Presenter pattern for a list of articles.

    """
    def __init__(self, articles):
        self.articles = sorted(
            articles,
            key=attrgetter('created_date'),
            reverse=True)

    def latest(self):
        """
        Get the latest article.
        """
        try:
            return self.articles[0]
        except IndexError:
            raise NotFound()

    def by_slug(self, slug):
        """
        Get an article by slug.

        :param str slug:
        """
        for article in self.articles:
            if article.slug == slug:
                return article
        else:
            raise NotFound(slug)

    def to_list(self):
        """
        Get an ordered list of articles.
        """
        return self.articles[:]


class BookmarkPresenter(object):

    """
    Presenter pattern for a list of bookmarks.

    """
    def __init__(self, bookmarks):
        self.bookmarks = sorted(
            bookmarks,
            key=attrgetter('title'))

    def to_list(self):
        """
        Get an alphabetized list of bookmarks.
        """
        return self.bookmarks[:]

    def by_category(self):
        """
        Get a dict of bookmarks organized by category.
        """
        categories = defaultdict(list)

        for bookmark in self.bookmarks:
            for category in bookmark.categories:
                categories[category].append(bookmark)

        return categories
