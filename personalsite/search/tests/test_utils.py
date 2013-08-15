from unittest import TestCase
from functools import partial

from personalsite.search.index import get_bookmark_parser
from personalsite.search.utils import boost


def get_boost(query):
    """
    For all terms in a query, yield the boost value.
    """
    for child in query.children():
        yield child.boost

        try:
            for subchild_boost in get_boost(child):
                yield subchild_boost
        except AttributeError:
            pass


class BoostTest(TestCase):

    """
    Boost function for specific fields.

    """
    def test_query(self):
        query = get_bookmark_parser().parse('truck')
        query = query.apply(
            partial(boost, fields=['title', 'slug'], value=2.0)
        )

        boosted_values = list(get_boost(query))

        self.assertIn(2.0, boosted_values)

    def test_complex_query(self):
        query = get_bookmark_parser().parse('truck AND car NOT yellow')
        query = query.apply(
            partial(boost, fields=['title', 'slug'], value=2.0)
        )

        boosted_values = list(get_boost(query))

        self.assertIn(2.0, boosted_values)
