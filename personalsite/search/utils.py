from whoosh.query import Term


def boost(node, fields=[], value=2.0):
    def boost_inner(node):
        if isinstance(node, Term):
            if node.fieldname in fields:
                boosted_node = node.copy()
                boosted_node.boost = value
                return boosted_node
        return node.apply(boost_inner)
    return node.apply(boost_inner)
