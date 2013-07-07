from tempfile import mkdtemp
from contextlib import contextmanager
from functools import partial

from whoosh.fields import Schema, ID, KEYWORD, NGRAM, TEXT
from whoosh.index import create_in
from whoosh.qparser import MultifieldParser
from whoosh.query import Term


bookmark_schema = Schema(
    type=ID(stored=True),
    slug=NGRAM(stored=True),
    title=NGRAM(),
    description=TEXT(),
    categories=KEYWORD())


def boost(node, fields=[], value=2.0):
    if isinstance(node, Term):
        if node.fieldname in fields:
            boosted_node = node.copy()
            boosted_node.boost = value
            return boosted_node
    return node.apply(boost)


class SearchIndex(object):
    def __init__(self, bookmarks):
        self.bookmarks = bookmarks

        self._index = create_in(mkdtemp(), bookmark_schema)

        bookmark_writer = self._index.writer()
        for bookmark in self.bookmarks:
            self.add_bookmark(bookmark_writer, bookmark)
        bookmark_writer.commit()

    def add_bookmark(self, writer, bookmark):
        category_names = [i.name for i in bookmark.categories]

        writer.add_document(
            type=unicode(bookmark.__class__),
            slug=unicode(bookmark.slug),
            title=unicode(bookmark.title),
            categories=u', '.join(category_names))

        for category in bookmark.categories:
            writer.add_document(
                type=unicode(category.__class__),
                slug=unicode(category.slug),
                title=unicode(category.name),
                description=unicode(category.description))

    @contextmanager
    def search(self, query_string):
        with self._index.searcher() as searcher:
            parser = MultifieldParser(
                ['title', 'slug', 'description'],
                bookmark_schema)

            query = parser.parse(query_string)
            query.apply(partial(boost, fields=['title', 'slug'], value=2.0))

            yield searcher.search(query)
