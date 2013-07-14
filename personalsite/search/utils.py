from whoosh.query import Term


def boost(node, fields=[], value=2.0):
    if isinstance(node, Term):
        if node.fieldname in fields:
            boosted_node = node.copy()
            boosted_node.boost = value
            return boosted_node
    return node.apply(boost)
