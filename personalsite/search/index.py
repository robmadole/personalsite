from tempfile import mkdtemp
from contextlib import contextmanager
from functools import partial

from whoosh.fields import Schema, ID, KEYWORD, NGRAM, TEXT
from whoosh.index import create_in
from whoosh.qparser import MultifieldParser

from personalsite.parser.bookmark import Bookmark, Category, Location
from personalsite.search.utils import boost

bookmark_schema = Schema(
    type=ID(stored=True),
    slug=NGRAM(stored=True),
    title=NGRAM(stored=True),
    description=TEXT(stored=True),
    categories=KEYWORD())


def get_bookmark_parser():
    """
    Get a query parser for searching bookmark content.
    """
    return MultifieldParser(
        ['title', 'slug', 'description'],
        bookmark_schema)


class SearchResult(object):

    """
    Wrap search results and make the original objects accessible.

    """
    def __init__(self, results):
        self._results = results

        lookups = [
            Bookmark.lookup_by_slug,
            Category.lookup_by_slug,
            Location.lookup_by_url]

        self._lookup_map = {unicode(i.im_self): i for i in lookups}

    def __len__(self):
        return len(self._results)

    def __iter__(self):
        results = iter(self._results)

        while True:
            yield self._transform(results.next())

    def _transform(self, result):
        return self._lookup_map[result.get('type')](result.get('slug'))


def extract_documents(bookmarks):
    """
    Convert bookmark content into search index documents.
    """
    for bookmark in bookmarks:
        category_names = [i.name for i in bookmark.categories]

        yield {
            'type': unicode(bookmark.__class__),
            'slug': unicode(bookmark.slug),
            'title': unicode(bookmark.title),
            'categories': u', '.join(category_names)
        }

        for category in bookmark.categories:
            yield {
                'type': unicode(category.__class__),
                'slug': unicode(category.slug),
                'title': unicode(category.name),
                'description': unicode(category.description)
            }

        for location in bookmark.locations:
            yield {
                'type': unicode(location.__class__),
                'slug': unicode(location.url),
                'title': unicode(location.title),
                'description': unicode(location.description)
            }


class SearchIndex(object):
    def __init__(self, bookmarks):
        self.bookmarks = bookmarks

        self._index = create_in(mkdtemp(), bookmark_schema)

        bookmark_writer = self._index.writer()
        for document in extract_documents(bookmarks):
            bookmark_writer.add_document(**document)
        bookmark_writer.commit()

    @contextmanager
    def search(self, query_string):
        searcher = self._index.searcher()

        try:
            parser = get_bookmark_parser()

            query = parser.parse(query_string)
            query.apply(partial(boost, fields=['title', 'slug'], value=2.0))

            yield SearchResult(searcher.search(query))
        finally:
            searcher.close()
