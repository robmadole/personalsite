from operator import attrgetter


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
